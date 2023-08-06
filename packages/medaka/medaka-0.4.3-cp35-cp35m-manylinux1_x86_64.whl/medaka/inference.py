from collections import Counter
from copy import copy
import functools
import inspect
import itertools
import logging
import os
from timeit import default_timer as now

import h5py
import numpy as np
import pysam

from medaka import vcf
from medaka.common import (_label_counts_path_, get_regions,
                           _label_decod_path_, decoding,
                           get_sample_index_from_files, grouper,
                           load_sample_from_hdf, load_yaml_data,
                           _model_opt_path_, mkdir_p, Sample,
                           write_sample_to_hdf, write_yaml_data,
                           yield_from_feature_files, gen_train_batch,
                           _label_batches_path_, _feature_batches_path_,
                           yield_batches_from_hdfs, _gap_,
                           _feature_decoding_path_, _feature_opt_path_)
from medaka.features import SampleGenerator


def weighted_categorical_crossentropy(weights):
    """
    A weighted version of keras.objectives.categorical_crossentropy
    @url: https://gist.github.com/wassname/ce364fddfc8a025bfab4348cf5de852d
    @author: wassname

    Variables:
        weights: numpy array of shape (C,) where C is the number of classes

    Usage:
        weights = np.array([0.5,2,10]) # Class one at 0.5, class 2 twice the normal weights, class 3 10x.
        loss = weighted_categorical_crossentropy(weights)
        model.compile(loss=loss,optimizer='adam')
    """

    from keras import backend as K
    weights = K.variable(weights)

    def loss(y_true, y_pred):
        # scale predictions so that the class probas of each sample sum to 1
        y_pred /= K.sum(y_pred, axis=-1, keepdims=True)
        # clip to prevent NaN's and Inf's
        y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
        # calc
        loss = y_true * K.log(y_pred) * weights
        loss = -K.sum(loss, -1)
        return loss

    return loss


def build_model(chunk_size, feature_len, num_classes, gru_size=128, input_dropout=0.0,
                inter_layer_dropout=0.0, recurrent_dropout=0.0):
    """Builds a bidirectional GRU model
    :param chunk_size: int, number of pileup columns in a sample.
    :param feature_len: int, number of features for each pileup column.
    :param num_classes: int, number of output class labels.
    :param gru_size: int, size of each GRU layer.
    :param input_dropout: float, fraction of the input feature-units to drop.
    :param inter_layer_dropout: float, fraction of units to drop between layers.
    :param recurrent_dropout: float, fraction of units to drop within the recurrent state.
    :returns: `keras.models.Sequential` object.
    """

    from keras.models import Sequential
    from keras.layers import Dense, GRU, Dropout
    from keras.layers.wrappers import Bidirectional

    model = Sequential()

    input_shape=(chunk_size, feature_len)
    for i in [1, 2]:
        name = 'gru{}'.format(i)
        gru = GRU(gru_size, activation='tanh', return_sequences=True, name=name,
                  dropout=input_dropout, recurrent_dropout=recurrent_dropout)
        model.add(Bidirectional(gru, input_shape=input_shape))

    if inter_layer_dropout > 0:
        model.add(Dropout(inter_layer_dropout))

    # see keras #10417 for why we specify input shape
    model.add(Dense(
        num_classes, activation='softmax', name='classify',
        input_shape=(chunk_size, 2 * feature_len)
    ))

    return model


def qscore(y_true, y_pred):
    from keras import backend as K
    error = K.cast(K.not_equal(
        K.max(y_true, axis=-1), K.cast(K.argmax(y_pred, axis=-1), K.floatx())),
        K.floatx()
    )
    error = K.sum(error) / K.sum(K.ones_like(error))
    return -10.0 * 0.434294481 * K.log(error)


def run_training(train_name, sample_gen, valid_gen, n_batch_train, n_batch_valid, feature_meta,
                 timesteps, feat_dim, model_fp=None, epochs=5000, batch_size=100, class_weight=None, n_mini_epochs=1):
    """Run training."""
    from keras.callbacks import ModelCheckpoint, CSVLogger, TensorBoard, EarlyStopping

    logger = logging.getLogger('Training')
    logger.info("Got {} batches for training, {} for validation.".format(n_batch_train, n_batch_valid))

    num_classes = len(feature_meta[_label_decod_path_])

    if model_fp is None:
        model_kwargs = { k:v.default for (k,v) in inspect.signature(build_model).parameters.items()
                         if v.default is not inspect.Parameter.empty}
    else:
        model_kwargs = load_yaml_data(model_fp, _model_opt_path_)
        assert model_kwargs is not None

    opt_str = '\n'.join(['{}: {}'.format(k,v) for k, v in model_kwargs.items()])
    logger.info('Building model with: \n{}'.format(opt_str))
    model = build_model(timesteps, feat_dim, num_classes, **model_kwargs)

    if model_fp is not None and os.path.splitext(model_fp)[-1] != '.yml':
        logger.info("Loading weights from {}".format(model_fp))
        model.load_weights(model_fp)

    logger.info("feat_dim: {}, timesteps: {}, num_classes: {}".format(feat_dim, timesteps, num_classes))
    model.summary()

    model_details = feature_meta.copy()
    model_details[_model_opt_path_] = model_kwargs
    write_yaml_data(os.path.join(train_name, 'training_config.yml'), model_details)

    opts = dict(verbose=1, save_best_only=True, mode='max')

    # define class here to avoid top-level keras import
    class ModelMetaCheckpoint(ModelCheckpoint):
        """Custom ModelCheckpoint to add medaka-specific metadata to model files"""
        def __init__(self, medaka_meta, *args, **kwargs):
            super(ModelMetaCheckpoint, self).__init__(*args, **kwargs)
            self.medaka_meta = medaka_meta

        def on_epoch_end(self, epoch, logs=None):
            super(ModelMetaCheckpoint, self).on_epoch_end(epoch, logs)
            filepath = self.filepath.format(epoch=epoch + 1, **logs)
            write_yaml_data(filepath, self.medaka_meta)

    callbacks = [
        # Best model according to training set accuracy
        ModelMetaCheckpoint(model_details, os.path.join(train_name, 'model.best.hdf5'),
                            monitor='acc', **opts),
        # Best model according to validation set accuracy
        ModelMetaCheckpoint(model_details, os.path.join(train_name, 'model.best.val.hdf5'),
                        monitor='val_acc', **opts),
        # Best model according to validation set qscore
        ModelMetaCheckpoint(model_details, os.path.join(train_name, 'model.best.val.qscore.hdf5'),
                        monitor='val_qscore', **opts),
        # Checkpoints when training set accuracy improves
        ModelMetaCheckpoint(model_details, os.path.join(train_name, 'model-acc-improvement-{epoch:02d}-{acc:.2f}.hdf5'),
                        monitor='acc', **opts),
        ModelMetaCheckpoint(model_details, os.path.join(train_name, 'model-val_acc-improvement-{epoch:02d}-{val_acc:.2f}.hdf5'),
                        monitor='val_acc', **opts),
        # Stop when no improvement, patience is number of epochs to allow no improvement
        EarlyStopping(monitor='val_loss', patience=20),
        # Log of epoch stats
        CSVLogger(os.path.join(train_name, 'training.log')),
        # Allow us to run tensorboard to see how things are going. Some
        #   features require validation data, not clear why.
        #TensorBoard(log_dir=os.path.join(train_name, 'logs'),
        #            histogram_freq=5, batch_size=100, write_graph=True,
        #            write_grads=True, write_images=True)
    ]

    if class_weight is not None:
        loss = weighted_categorical_crossentropy(class_weight)
        logger.info("Using weighted_categorical_crossentropy loss function")
    else:
        loss = 'sparse_categorical_crossentropy'
        logger.info("Using {} loss function".format(loss))

    model.compile(
       loss=loss,
       optimizer='rmsprop',
       metrics=['accuracy', qscore],
    )

    if n_mini_epochs == 1:
        logging.info("Not using mini_epochs, an epoch is a full traversal of the training data")
    else:
        logging.info("Using mini_epochs, an epoch is a traversal of 1/{} of the training data".format(n_mini_epochs))

    # fit generator
    model.fit_generator(
        sample_gen, steps_per_epoch=n_batch_train//n_mini_epochs,
        validation_data=valid_gen, validation_steps=n_batch_valid,
        max_queue_size=8, workers=8, use_multiprocessing=False,
        epochs=epochs,
        callbacks=callbacks,
        class_weight=class_weight,
    )


class VarQueue(list):

    @property
    def last_pos(self):
        if len(self) == 0:
            return None
        else:
            return self[-1].pos

    def write(self, vcf_fh):
        if len(self) > 1:
            are_dels = all(len(x.ref) == 2 for x in self)
            are_same_ref = len(set(x.chrom for x in self)) == 1
            if are_dels and are_same_ref:
                name = self[0].chrom
                pos = self[0].pos
                ref = ''.join((x.ref[0] for x in self))
                ref += self[-1].ref[-1]
                alt = ref[0]

                merged_var = vcf.Variant(name, pos, ref, alt, info=info)
                vcf_fh.write_variant(merged_var)
            else:
                raise ValueError('Cannot merge variants: {}.'.format(self))
        elif len(self) == 1:
            vcf_fh.write_variant(self[0])
        del self[:]


class VCFChunkWriter(object):
    def __init__(self, fname, chrom, start, end, reference_fasta, label_decoding):
        vcf_region_str = '{}:{}-{}'.format(chrom, start, end) #is this correct?
        self.label_decoding = label_decoding
        self.logger = logging.getLogger('VCFWriter')
        self.logger.info("Writing variants for {}".format(vcf_region_str))

        vcf_meta = ['region={}'.format(vcf_region_str)]
        self.writer = vcf.VCFWriter(fname, meta_info=vcf_meta)
        self.ref_fasta = pysam.FastaFile(reference_fasta)

    def __enter__(self):
        self.writer.__enter__()
        self.ref_fasta.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer.__exit__(exc_type, exc_val, exc_tb)
        self.ref_fasta.__exit__(exc_type, exc_val, exc_tb)

    def add_chunk(self, sample, pred):
        # Write consensus alts to vcf
        cursor = 0
        var_queue = list()
        ref_seq = self.ref_fasta.fetch(sample.ref_name)
        for pos, grp in itertools.groupby(sample.positions['major']):
            end = cursor + len(list(grp))
            alt = ''.join(self.label_decoding[x] for x in pred[cursor:end]).replace(_gap_, '')
            # For simple insertions and deletions in which either
            #   the REF or one of the ALT alleles would otherwise be
            #   null/empty, the REF and ALT Strings must include the
            #   base before the event (which must be reflected in
            #   the POS field), unless the event occurs at position
            #   1 on the contig in which case it must include the
            #   base after the event
            if alt == '':
                # deletion
                if pos == 0:
                    # the "unless case"
                    ref = ref_seq[1]
                    alt = ref_seq[1]
                else:
                    # the usual case
                    pos = pos - 1
                    ref = ref_seq[pos:pos+2]
                    alt = ref_seq[pos]
            else:
                ref = ref_seq[pos]

            # Merging of variants produced by considering major.{minor} positions
            # These are of the form:
            #    X -> Y          - subs
            #    prev.X -> prev  - deletion
            #    X -> Xyy..      - insertion
            # In the second case we may need to merge variants from consecutive
            # major positions.
            if alt == ref:
                self.write(var_queue)
                var_queue = list()
            else:
                var = vcf.Variant(sample.ref_name, pos, ref, alt)
                if len(var_queue) == 0 or pos - var_queue[-1].pos == 1:
                    var_queue.append(var)
                else:
                    self.write(var_queue)
                    var_queue = [var]
            cursor = end
        self.write(var_queue)


    def write(self, var_queue):
        if len(var_queue) > 1:
            are_dels = all(len(x.ref) == 2 for x in var_queue)
            are_same_ref = len(set(x.chrom for x in var_queue)) == 1
            if are_dels and are_same_ref:
                name = var_queue[0].chrom
                pos = var_queue[0].pos
                ref = ''.join((x.ref[0] for x in var_queue))
                ref += var_queue[-1].ref[-1]
                alt = ref[0]

                merged_var = vcf.Variant(name, pos, ref, alt)
                self.writer.write_variant(merged_var)
            else:
                raise ValueError('Cannot merge variants: {}.'.format(var_queue))
        elif len(var_queue) == 1:
            self.writer.write_variant(var_queue[0])


def run_prediction(output, bam, regions, model, model_file, rle_ref, read_fraction, chunk_len, chunk_ovlp,
                   batch_size=200):
    """Inference worker."""
    logger = copy(logging.getLogger(__package__))
    logger.name = 'PWorker'

    def sample_gen():
        # chain all samples whilst dispensing with generators when done
        #   (they hold the feature vector in memory until they die)
        for region in regions:
            data_gen = SampleGenerator(
                bam, region, model_file, rle_ref, read_fraction,
                chunk_len=chunk_len, chunk_overlap=chunk_ovlp)
            yield from data_gen.samples
    batches = grouper(sample_gen(), batch_size)

    total_region_mbases = sum(r.size for r in regions) / 1e6
    logger.info("Running inference for {:.1f}M draft bases.".format(total_region_mbases))

    with h5py.File(output, 'a') as pred_h5:
        mbases_done = 0

        t0 = now()
        tlast = t0
        for data in batches:
            x_data = np.stack((x.features for x in data))
            # TODO: change to predict_on_batch?
            class_probs = model.predict(x_data, batch_size=batch_size, verbose=0)
            mbases_done += sum(x.span for x in data) / 1e6
            mbases_done = min(mbases_done, total_region_mbases)  # just to avoid funny log msg
            t1 = now()
            if t1 - tlast > 10:
                tlast = t1
                msg = '{:.1%} Done ({:.1f}/{:.1f} Mbases) in {:.1f}s'
                logger.info(msg.format(mbases_done / total_region_mbases, mbases_done, total_region_mbases, t1 - t0))

            best = np.argmax(class_probs, -1)
            for sample, prob, pred in zip(data, class_probs, best):
                # write out positions and predictions for later analysis
                if pred_h5 is not None:
                    sample_d = sample._asdict()
                    sample_d['label_probs'] = prob
                    sample_d['features'] = None  # to keep file sizes down
                    write_sample_to_hdf(Sample(**sample_d), pred_h5)

    logger.info('All done')
    return None


def predict(args):
    """Inference program."""
    os.environ["TF_CPP_MIN_LOG_LEVEL"]="2"
    from keras.models import load_model
    from keras import backend as K

    args.regions = get_regions(args.bam, region_strs=args.regions)
    logger = copy(logging.getLogger(__package__))
    logger.name = 'Predict'
    logger.info('Processing region(s): {}'.format(' '.join(str(r) for r in args.regions)))

    # write class names to output
    label_decoding = load_yaml_data(args.model, _label_decod_path_)
    write_yaml_data(args.output, {_label_decod_path_: label_decoding})

    logger.info("Setting tensorflow threads to {}.".format(args.threads))
    K.tf.logging.set_verbosity(K.tf.logging.ERROR)
    K.set_session(K.tf.Session(
        config=K.tf.ConfigProto(
            intra_op_parallelism_threads=args.threads,
            inter_op_parallelism_threads=args.threads)
    ))

    def _rebuild_model(model, chunk_len):
        time_steps = model.get_input_shape_at(0)[1]
        if chunk_len is None or time_steps != chunk_len:
            logger.info("Rebuilding model according to chunk_size: {}->{}".format(time_steps, chunk_len))
            feat_dim = model.get_input_shape_at(0)[2]
            num_classes = model.get_output_shape_at(-1)[-1]
            model = build_model(chunk_len, feat_dim, num_classes)
            logger.info("Loading weights from {}".format(args.model))
            model.load_weights(args.model)

        if logger.level == logging.DEBUG:
            model.summary()
        return model

    model = load_model(args.model, custom_objects={'qscore': qscore})

    # Split overly long regions to maximum size so as to not create
    #   massive feature matrices, then segregate those which cannot be
    #   batched.
    MAX_REGION_SIZE = int(1e6)  # 1Mb
    long_regions = []
    short_regions = []
    for region in args.regions:
        if region.size > MAX_REGION_SIZE:
            regs = region.split(MAX_REGION_SIZE, args.chunk_ovlp)
        else:
            regs = [region]
        for r in regs:
            if r.size > args.chunk_len:
                long_regions.append(r)
            else:
                short_regions.append(r)
    logger.info("Found {} long and {} short regions.".format(
        len(long_regions), len(short_regions)))

    if len(long_regions) > 0:
        logger.info("Processing long regions.")
        model = _rebuild_model(model, args.chunk_len)
        run_prediction(
            args.output, args.bam, long_regions, model, args.model, args.rle_ref, args.read_fraction,
            args.chunk_len, args.chunk_ovlp,
            batch_size=args.batch_size
        )

    # short regions must be done individually since they have differing lengths
    #   TODO: consider masking (it appears slow to apply wholesale), maybe 
    #         step down args.chunk_len by a constant factor until nothing remains.
    if len(short_regions) > 0:
        logger.info("Processing short regions")
        model = _rebuild_model(model, None)
        for region in short_regions:
            chunk_len = region.size // 2
            chunk_ovlp = chunk_len // 10 # still need overlap as features will be longer
            run_prediction(
                args.output, args.bam, [region], model, args.model, args.rle_ref, args.read_fraction,
                chunk_len, chunk_ovlp,
                batch_size=args.batch_size
            )
    logger.info("Finished processing all regions.")


def process_labels(label_counts, max_label_len=10):
    """Create map from full labels to (encoded) truncated labels."""
    logger = logging.getLogger('Labelling')

    old_labels = [k for k in label_counts.keys()]
    if type(old_labels[0]) == tuple:
        new_labels = (l[1] * decoding[l[0]].upper() for l in old_labels)
    else:
        new_labels = [l for l in old_labels]

    if max_label_len < np.inf:
        new_labels = [l[:max_label_len] for l in new_labels]

    old_to_new = dict(zip(old_labels, new_labels))
    label_decoding = list(sorted(set(new_labels)))
    label_encoding = { l: label_decoding.index(old_to_new[l]) for l in old_labels}
    logger.info("Label encoding dict is:\n{}".format('\n'.join(
        '{}: {}'.format(k, v) for k, v in label_encoding.items()
    )))

    new_counts = Counter()
    for l in old_labels:
        new_counts[label_encoding[l]] += label_counts[l]
    logger.info("New label counts {}".format(new_counts))

    return label_encoding, label_decoding, new_counts


def train(args):
    """Training program."""
    train_name = args.train_name
    mkdir_p(train_name, info='Results will be overwritten.')

    logger = logging.getLogger('Training')
    logger.debug("Loading datasets:\n{}".format('\n'.join(args.features)))

    # get feature meta data
    feature_meta = {k: load_yaml_data(args.features[0], k)
                    for k in (_feature_opt_path_, _feature_decoding_path_)}

    # get counts of labels in training samples
    label_counts = Counter()
    for f in args.features:
        label_counts.update(load_yaml_data(f, _label_counts_path_))

    logger.info("Total labels {}".format(sum(label_counts.values())))


    is_batched = True
    batches = []
    for fname in args.features:
        with h5py.File(fname, 'r') as h5:
            has_batches = _label_batches_path_ in h5 and _feature_batches_path_ in h5
            msg = 'Found batches in {}.' if has_batches else 'No batches in {}.'
            logger.info(msg.format(fname))
            batches.extend(((fname, batch) for batch in h5[_feature_batches_path_]))

    if is_batched:
        logger.info("Got {} batches.".format(len(batches)))
        # check batch size using first batch
        test_fname, test_batch = batches[0]
        with h5py.File(test_fname, 'r') as h5:
            batch_shape = h5['{}/{}'.format(_feature_batches_path_, test_batch)].shape
            label_shape = h5['{}/{}'.format(_label_batches_path_, test_batch)].shape

        logger.info("Got {} batches with feat shape {}, label shape {}".format(len(batches), batch_shape, label_shape))
        batch_size, timesteps, feat_dim = batch_shape
        if not sum(label_counts.values()) != len(batches) * timesteps:
            raise ValueError('Label counts not consistent with number of batches')

        n_batch_train = int((1 - args.validation_split) * len(batches))
        train_batches = batches[:n_batch_train]
        valid_batches = batches[n_batch_train:]
        n_batch_valid = len(valid_batches)

        if args.balanced_weights:
            sparse_labels = False
        else:
            sparse_labels = True

        gen_train = yield_batches_from_hdfs(
            train_batches, sparse_labels=sparse_labels, n_classes=len(label_counts))
        gen_valid = yield_batches_from_hdfs(
            valid_batches, sparse_labels=sparse_labels, n_classes=len(label_counts))
        label_decoding = load_yaml_data(args.features[0], _label_decod_path_)

    else:
        sample_index = get_sample_index_from_files(args.features, max_samples=args.max_samples)
        refs = [k for k in sample_index.keys()]
        logger.info("Got the following references for training:\n{}".format('\n'.join(refs)))
        n_samples = sum([len(sample_index[k]) for k in sample_index])
        logger.info("Got {} pileup chunks for training.".format(n_samples))
        # get label encoding, given max_label_len
        logger.info("Max label length: {}".format(args.max_label_len if args.max_label_len is not None else 'inf'))
        label_encoding, label_decoding, label_counts = process_labels(label_counts, max_label_len=args.max_label_len)

        # create seperate generators of x,y for training and validation
        # shuffle samples before making split so each ref represented in training
        # and validation and batches are not biased to a particular ref.
        samples = [(d['key'], d['filename']) for ref in sample_index.values() for d in ref]
        np.random.shuffle(samples)  # shuffle in place
        n_samples_train = int((1 - args.validation_split) * len(samples))
        samples_train = samples[:n_samples_train]
        samples_valid = samples[n_samples_train:]
        # all batches need to be the same size, so pad samples_train and samples_valid
        n_extra_train = args.batch_size - len(samples_train) % args.batch_size
        n_extra_valid = args.batch_size - len(samples_valid) % args.batch_size
        samples_train += [samples_train[i] for i in np.random.choice(len(samples_train), n_extra_train)]
        samples_valid += [samples_valid[i] for i in np.random.choice(len(samples_valid), n_extra_valid)]

        msg = '{} training samples padded to {}, {} validation samples padded to {}'
        logger.info(msg.format(len(set(samples_train)), len(samples_train),
                                len(set(samples_valid)), len(samples_valid)))

        # load one sample to figure out timesteps and data dim
        key, fname = samples_train[0]
        with h5py.File(fname) as h5:
            first_sample = load_sample_from_hdf(key, h5)
        timesteps = first_sample.features.shape[0]
        feat_dim = first_sample.features.shape[1]

        if not sum(label_counts.values()) // timesteps == n_samples:
            raise ValueError('Label counts not consistent with number of samples')

        gen_train_samples = yield_from_feature_files(args.features, samples=itertools.cycle(samples_train))
        gen_valid_samples = yield_from_feature_files(args.features, samples=itertools.cycle(samples_valid))
        s2xy = functools.partial(sample_to_x_y, encoding=label_encoding)
        gen_train = gen_train_batch(map(s2xy, gen_train_samples), args.batch_size, name='training')
        gen_valid = gen_train_batch(map(s2xy, gen_valid_samples), args.batch_size, name='validation')
        n_batch_train = len(samples_train) // args.batch_size
        n_batch_valid = len(samples_valid) // args.batch_size

    if args.balanced_weights:
        n_samples = sum(label_counts.values())
        n_classes = len(label_counts)
        class_weight = {k: float(n_samples)/(n_classes * count) for (k, count) in label_counts.items()}
        class_weight = np.array([class_weight[c] for c in sorted(class_weight.keys())])
    else:
        class_weight = None

    h = lambda d, i: d[i] if d is not None else 1
    logger.info("Label statistics are:\n{}".format('\n'.join(
        '{}: {} ({}, {:9.6f})'.format(i, l, label_counts[i], h(class_weight, i)) for i, l in enumerate(label_decoding)
    )))

    feature_meta[_label_decod_path_] = label_decoding
    feature_meta[_label_counts_path_] = label_counts

    run_training(train_name, gen_train, gen_valid, n_batch_train, n_batch_valid, feature_meta,
                 timesteps, feat_dim, model_fp=args.model, epochs=args.epochs, batch_size=args.batch_size,
                 class_weight=class_weight, n_mini_epochs=args.mini_epochs)


