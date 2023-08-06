#!/usr/bin/env python
'''
component
Created by Seria at 25/11/2018 2:58 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-

from functools import partial
import tensorflow as tf

class Pod:
    def __init__(self, comp, symbol, name, msg=[]):
        self.component = comp
        self.symbol = symbol
        self.message = msg
        self.name = name

    def __rshift__(self, other):
        return Pod([self, other], '>', 'CASCADE')

    def __add__(self, other):
        return Pod([self, other], '+', 'ADD')

    def __sub__(self, other):
        return Pod([self, other], '-', 'SUB')

    def __mul__(self, other):
        return Pod([self, other], '*', 'MUL')

    def __matmul__(self, other):
        return Pod([self, other], '@', 'MATMUL')

    def __and__(self, other):
        return Pod([self, other], '&', 'CONCAT')

    def __pow__(self, power, modulo=None):
        assert isinstance(power, int)
        pod = Pod(self.component, self.symbol, self.name + '_0')
        for p in range(1, power):
            pod = pod >> Pod(self.component, self.symbol, self.name + '_' + str(p))
        return pod

    def show(self):
        if isinstance(self.component, list):
            self.component[0].show()
            self.component[1].show()
        else:
            print(self.name)



class Component(object):
    def __init__(self):
        self.warehouse = ['CONV_1D', 'CONV_2D', 'CONV_3D',
                           'SIGMOID', 'TANH', 'SOFTMAX', 'RELU', 'LRELU',
                           'MAX_POOL_2D', 'AVG_POOL_2D']
        # Convolution
        self.CONV_1D = 0
        self.CONV = self.conv_2d
        self.CONV_3D = 2
        self.CONV_TRANS = 3
        self.CONV_SEP = 4
        self.CONV_ATROUS = 5
        # Activation
        self.SIGMOID = self.sigmoid
        self.TANH = self.tanh
        self.SOFTMAX = self.softmax
        self.RELU = self.relu
        self.RELU_LEAKY = self.relu_leaky
        self.RELU_EXP = 15
        # Pooling
        self.MAX_POOL = self.max_pool_2d
        self.AVG_POOL = self.avg_pool_2d
        # Distributing
        self.DROPOUT = self.dropout
        self.BATCH_NORM = self.batch_norm
        self.EMBEDDING = self.embedding
        # Vectorization
        self.FLAT = self.flat
        self.DENSE = self.dense
        # Copy or Rename
        self.DUPLICATE = self.duplicate
        self.CONVERT = self.convert
        # Loss
        self.WEIGHT_DECAY = self.weight_decay
        self.SIGM_XENTROPY = self.sigm_xentropy
        self.SFTM_XENTROPY = self.sftm_xentropy
        self.MSE = self.mse
        self.MAE = self.mae
        # Optimizer
        self.MOMENTUM = self.momentum
        self.NESTEROV = self.nesterov
        self.ADAM = self.adam



    def addComp(self, name, comp, is_complete=False):
        if name in self.warehouse:
            raise Exception('%s is an existing component in warehouse.' % name)
        if is_complete:
            def customizedComp(name):
                return Pod(partial(comp.component, name=name), comp.symbol, name, comp.message)
        else:
            assert not isinstance(comp.component, list)
            def customizedComp(**kwargs):
                symbol = kwargs.get(comp.symbol[1:], comp.symbol)
                return Pod(partial(comp.component, **kwargs), symbol, kwargs['name'], comp.message)
        exec('self.%s = customizedComp' % name.upper())

    # ------------------------------------ Convolution ------------------------------------ #

    def _createVar(self, name, shape, initializer, param, regularizer=None):
        init_err = Exception('%s initializer is not defined or supported.' % initializer)
        # with tf.device('/gpu:0'):
        if initializer == 'xavier':
            if param is None:
                param = False
            var = tf.get_variable(name, shape, initializer=tf.contrib.layers.xavier_initializer(uniform=param))
        elif initializer == 'trunc_norm':
            if param is None:
                param = [0, 0.1]
            var = tf.get_variable(name, shape,
                                  initializer=tf.truncated_normal_initializer(mean=param[0], stddev=param[1]))
        elif initializer == 'rand_norm':
            if param is None:
                param = [0, 0.1]
            var = tf.get_variable(name,
                                  initializer=tf.random_normal(shape, mean=param[0], stddev=param[1]))
        elif initializer == 'zero':
            var = tf.get_variable(name, shape, initializer=tf.zeros_initializer())
        elif initializer == 'one':
            var = tf.get_variable(name, shape, initializer=tf.ones_initializer())
        else:
            raise init_err

        if regularizer == 'l2':
            weight_decay = tf.nn.l2_loss(var, name=name+'/regularizer')
            tf.add_to_collection(tf.GraphKeys.REGULARIZATION_LOSSES, weight_decay)
        elif regularizer is None:
            pass
        else:
            raise Exception('%s regularizer is not defined or supported.' % regularizer)

        return var

    def conv_2d(self, **kwargs):
        if 'input' in kwargs.keys():
            symbol = kwargs['input']
        else:
            symbol = '.input'
        return Pod(partial(self._conv_2d, **kwargs), symbol, kwargs['name'])
    def _conv_2d(self, name, input, k_size, in_out_chs, w_init='xavier', w_param=None,
                 b_init=None, b_param=None, w_reg='l2', b_reg='l2', stride=(1, 1), padding='same'):
        padding = padding.upper()
        w = self._createVar(name+'_w', k_size + in_out_chs, w_init, w_param, w_reg)
        if b_init:
            b = self._createVar(name+'_b', [in_out_chs[-1]], b_init, b_param, b_reg)
            return tf.nn.bias_add(tf.nn.conv2d(input, w, [1, stride[0], stride[1], 1], padding), b, name=name)
        else:
            return tf.nn.conv2d(input, w, [1, stride[0], stride[1], 1], padding, name=name)

    # ------------------------------------ Activation ------------------------------------ #

    def sigmoid(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._sigmoid, **kwargs), symbol, kwargs['name'])
    def _sigmoid(self, name, input):
        return tf.nn.sigmoid(input, name)

    def tanh(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._tanh, **kwargs), symbol, kwargs['name'])
    def _tanh(self, name, input):
        return tf.nn.tanh(input, name)

    def softmax(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._tanh, **kwargs), symbol, kwargs['name'])
    def _softmax(self, name, input):
        return tf.nn.softmax(input, name)

    def relu(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._relu, **kwargs), symbol, kwargs['name'])
    def _relu(self, name, input):
        return tf.nn.relu(input, name)

    def relu_leaky(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._relu_leaky, **kwargs), symbol, kwargs['name'])
    def _relu_leaky(self, name, input):
        return tf.nn.leaky_relu(input, name)

    # ------------------------------------ Distributing ------------------------------------ #

    def dropout(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._dropout, **kwargs), symbol, kwargs['name'])
    def _dropout(self, name, input, p_drop):
        return tf.nn.dropout(input, 1-p_drop, name=name)

    def batch_norm(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._batch_norm, **kwargs), symbol, kwargs['name'])
    def _batch_norm(self, name, input, is_train, beta=False, gamma=False):
        return tf.layers.batch_normalization(input, training=is_train, center=beta, scale=gamma, name=name)

    def embedding(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._embedding, **kwargs), symbol, kwargs['name'])
    def _embedding(self, name, input, vocabulary, vec_dims, w_init='xavier', w_param=None):
        embd_vec = self._createVar(name+'_vec', [vocabulary, vec_dims], w_init, w_param)
        return tf.nn.embedding_lookup(embd_vec, input, name=name)

    # ------------------------------------ Pooling ------------------------------------ #

    def max_pool_2d(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._max_pool_2d, **kwargs), symbol, kwargs['name'])
    def _max_pool_2d(self, name, input, kernel=(2, 2), stride=(2, 2), padding='same'):
        padding = padding.upper()
        return tf.nn.max_pool(input,
                              [1, kernel[0], kernel[1], 1],
                              [1, stride[0], stride[1], 1],
                              padding, name=name)

    def avg_pool_2d(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._avg_pool_2d, **kwargs), symbol, kwargs['name'])
    def _avg_pool_2d(self, name, input, kernel=(2, 2), stride=(2, 2), padding='same'):
        padding = padding.upper()
        return tf.nn.avg_pool(input,
                              [1, kernel[0], kernel[1], 1],
                              [1, stride[0], stride[1], 1],
                              padding, name=name)

    # ------------------------------------ Vectorization ------------------------------------ #

    def flat(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._flat, **kwargs), symbol, kwargs['name'])
    def _flat(self, name, input):
        return tf.layers.flatten(input, name=name)

    def dense(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._dense, **kwargs), symbol, kwargs['name'])
    def _dense(self, name, input, out_chs, w_init='xavier', w_param=None,
               b_init=None, b_param=None, w_reg='l2', b_reg='l2'):
        in_chs = int(input.get_shape()[-1])
        in_out_chs = [in_chs, out_chs]
        w = self._createVar(name + '_w', in_out_chs, w_init, w_param, w_reg)
        if b_init:
            b = self._createVar(name + '_b', [in_out_chs[-1]], b_init, b_param, b_reg)
            return tf.nn.bias_add(tf.matmul(input, w), b, name=name)
        else:
            return tf.matmul(input, w, name=name)

    # ------------------------------------ Redefine or Rename ------------------------------------ #

    def duplicate(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._duplicate, **kwargs), symbol, kwargs['name'])
    def _duplicate(self, name, input):
        return tf.identity(input, name)

    def convert(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._convert, **kwargs), symbol, kwargs['name'])
    def _convert(self, name, input, dtype, trainable=False):
        if isinstance(input, (tf.Tensor, tf.SparseTensor, tf.Variable)):
            return tf.cast(input, tf.as_dtype(dtype), name=name)
        else:
            return tf.Variable(input, trainable=trainable, name=name)

    # ------------------------------------ Loss ------------------------------------ #

    def weight_decay(self, **kwargs):
        if 'penalty' in kwargs.keys():
            message = [kwargs['penalty']]
        else:
            message = []
        return Pod(partial(self._weight_decay, **kwargs), '.penalty', kwargs['name'], message)
    def _weight_decay(self, name, input, decay_scope=None):
        if decay_scope is None:
            return tf.multiply(tf.add_n(tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)),
                               input, name=name)
        else:
            return tf.multiply(tf.add_n(tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES, scope=decay_scope)),
                               input, name=name)

    def sigm_xentropy(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._sigm_xentropy, **kwargs), symbol, kwargs['name'], [kwargs['label']])
    def _sigm_xentropy(self, name, input, label):
        labels = tf.cast(label, tf.float32)
        return tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=label, logits=input, name=name))

    def sftm_xentropy(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._sftm_xentropy, **kwargs), symbol, kwargs['name'], [kwargs['label']])
    def _sftm_xentropy(self, name, input, label, one_hot):
        if one_hot:
            labels = tf.cast(label, tf.float32)
            return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=labels, logits=input, name=name))
        else:
            return tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(
                                        labels=label, logits= input, name=name))

    def mse(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._mse, **kwargs), symbol, kwargs['name'], [kwargs['label']])
    def _mse(self, name, input, label):
        return tf.squared_difference(input, label, name)

    def mae(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._mae, **kwargs), symbol, kwargs['name'], [kwargs['label']])
    def _mae(self, name, input, label):
        return tf.abs(input-label, name)

    # ------------------------------------ Optimizer ------------------------------------ #

    def _lrStrategy(self, mile_meter, lr, lr_decay, miles, param):
        if lr_decay == 'exp':
            return tf.train.exponential_decay(lr, mile_meter, miles, param, staircase=False)
        elif lr_decay == 'exp_stair':
            return tf.train.exponential_decay(lr, mile_meter, miles, param, staircase=True)
        elif lr_decay == 'poly':
            return tf.train.polynomial_decay(lr, mile_meter, miles, power=param, cycle=False)
        elif lr_decay == 'poly_cycle':
            return tf.train.polynomial_decay(lr, mile_meter, miles, power=param, cycle=True)
        elif lr_decay == 'stair':
            return tf.train.piecewise_constant(mile_meter, [i*param for i in range(1, len(lr))], lr)
        else:
            raise KeyError('%s decay is not supported or defined.' % lr_decay)

    def _computeGrad(self, optz, cost, update_scope, grad_limit):
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(update_ops):
            if update_scope is None:
                grad_var_pairs = optz.compute_gradients(cost)
            else:
                grad_var_pairs = optz.compute_gradients(cost, var_list=tf.get_collection(
                    tf.GraphKeys.TRAINABLE_VARIABLES, scope=update_scope))
            if grad_limit is None:
                return grad_var_pairs
            else:
                return [(tf.clip_by_value(grad, -grad_limit, grad_limit), var) for grad, var in grad_var_pairs]

    def momentum(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._momentum, **kwargs), symbol, kwargs['name'])
    def _momentum(self, name, input, mile_meter, lr, mmnt=0.9, update_scope=None,
                  lr_decay=None, lr_miles=None, decay_param=None, grad_limit=None):
        if isinstance(lr_decay, str):
            lr = self._lrStrategy(mile_meter, lr, lr_decay, lr_miles, decay_param)
        optz = tf.train.MomentumOptimizer(lr, mmnt)
        grad = self._computeGrad(optz, input, update_scope, grad_limit)
        train_op = optz.apply_gradients(grad, mile_meter, name=name)
        return train_op

    def nesterov(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._nesterov, **kwargs), symbol, kwargs['name'])
    def _nesterov(self, name, input, mile_meter, lr, mmnt=0.9, update_scope=None,
                  lr_decay=None, lr_miles=None, decay_param=None, grad_limit=None):
        if isinstance(lr_decay, str):
            lr = self._lrStrategy(mile_meter, lr, lr_decay, lr_miles, decay_param)
        optz = tf.train.MomentumOptimizer(lr, mmnt, use_nesterov=True)
        grad = self._computeGrad(optz, input, update_scope, grad_limit)
        train_op = optz.apply_gradients(grad, mile_meter, name=name)
        return train_op

    def adam(self, **kwargs):
        symbol = kwargs.get('input', '.input')
        return Pod(partial(self._adam, **kwargs), symbol, kwargs['name'])
    def _adam(self, name, input, mile_meter, lr, mmnt1=0.9, mmnt2=0.999, update_scope=None,
                  lr_decay=None, lr_miles=None, decay_param=None, grad_limit=None):
        if isinstance(lr_decay, str):
            lr = self._lrStrategy(mile_meter, lr, lr_decay, lr_miles, decay_param)
        optz = tf.train.AdamOptimizer(lr, beta1=mmnt1, beta2=mmnt2)
        grad = self._computeGrad(optz, input, update_scope, grad_limit)
        train_op = optz.apply_gradients(grad, mile_meter, name=name)
        return train_op