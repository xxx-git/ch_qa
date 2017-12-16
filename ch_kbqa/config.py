# -*- coding:utf-8 -*-


class LargeConfig(object):
    learning_rate = 1.0
    init_scale = 0.5
    learning_rate_decay_factor = 0.99
    max_gradient_norm = 5.0
    num_samples = 4096  # Sampled Softmax
    batch_size = 256
    size = 256  # Number of Node of each layer
    num_layers = 1
    max_vocab_size = 50000
    src_vocab_size = 17422
    dest_vocab_size = 3100


class MediumConfig(object):
    learning_rate = 0.5
    init_scale = 0.04
    learning_rate_decay_factor = 0.99
    max_gradient_norm = 5.0
    num_samples = 2048  # Sampled Softmax
    batch_size = 64
    size = 64  # Number of Node of each layer
    num_layers = 2
    src_vocab_size = 17943
    dest_vocab_size = 3126