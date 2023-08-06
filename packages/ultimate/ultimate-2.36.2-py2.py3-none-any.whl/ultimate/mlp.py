# coding: utf-8
from __future__ import print_function, division, unicode_literals, absolute_import

import sys
import os
import math
import numpy

try:
    from .mesh import Mesh
except:
    from mesh import Mesh

class MLP(Mesh):
    def __init__(self, params={}, initialize=True, **kwargs):
        self._libc = None
        self.initialized_ = False
        self.rate_ = None
        self.loss_ = None
        self.feature_importances_ = None
        self.params_ = {}
        self.params_.update(params)
        self.params_.update(kwargs)

        if initialize:
            self.mlp_init(**self.params_)
            self.run_filler()

    def get_params(self, deep=False):
        return self.params_

    def set_params(self, **kwargs):
        # print("set_params", kwargs)
        self.params_.update(kwargs)

        if self.initialized_:
            self.mlp_init(**self.params_)
        return self

    def mlp_init(self,
                 dtype='float64',
                 op='fc',
                 exf=[],
                 activation=[],
                 layer_size=[],
                 input_type='pointwise',
                 loss_type='mse',
                 output_range=(0, 1),
                 output_shrink=0.001,               # 0.1
                 importance_mul=0.001,
                 leaky=-0.001,
                 dropout=0,
                 bias_rate=[0.005],
                 weight_rate=[],
                 regularization=1,

                 weight_filler={'Type': 'gsfi', 'Adj': (0, 0.8)},
                 bias_filler={'Type': 'zero', 'Adj': (0, 1)},

                 epoch_train=5,
                 epoch_decay=1,
                 rate_init=0.06,
                 rate_decay=0.9,
                 importance_out=False,
                 loss_mul=0.001,
                 shuffle=True,

                 verbose=1,
                 verbose_feed=0,
                 iteration_log=100,
                 ):

        if not self.initialized_:
            self.initialized_ = True
            self.mesh_init(dtype=dtype)

        self.epoch_train = epoch_train
        self.epoch_decay = epoch_decay
        self.rate_init = rate_init
        self.rate_decay = rate_decay
        self.importance_out = importance_out
        self.loss_mul = loss_mul
        self.shuffle = shuffle

        self.verbose = verbose
        self.verbose_feed = verbose_feed
        self.iteration_log = iteration_log

        self.set_conf({})

        for idx, shape in enumerate(layer_size):
            if isinstance(shape, int):
                shape = (1, 1, shape)

            assert isinstance(shape, tuple)

            arg = {'Shape': shape}
            if idx == 0:
                arg['InputType'] = input_type
                arg['ImportanceMul'] = importance_mul
            if idx == len(layer_size) - 1:
                arg['Regularization'] = regularization
                arg['LossType'] = loss_type
                arg['OutputRange'] = output_range
                arg['OutputShrink'] = output_shrink

            self.set_tensor(idx, arg)

        for idx in range(max(len(layer_size) - 1, len(exf))):
            arg = {'Tin': idx, 'Tout': idx+1}

            kv = {
                'BiasRate': bias_rate,
                'Dropout': dropout,
                'Leaky': leaky,
                'WeightRate': weight_rate,
                'Activation': activation,
                'Op': op,
                'WeightFiller': weight_filler,
                'BiasFiller': bias_filler,
            }

            for k in kv:
                if not isinstance(kv[k], list):
                    if kv[k] is not None:
                        arg[k] = kv[k]
                elif idx < len(kv[k]) and kv[k][idx] is not None:
                    arg[k] = kv[k][idx]

            if isinstance(exf, dict):
                arg.update(exf)
            elif idx < len(exf) and isinstance(exf[idx], dict):
                arg.update(exf[idx])

            self.set_filter(idx, arg)

    def check_arr(self, arr):
        if hasattr(arr, 'toarray'):
            arr = arr.toarray()

        if not isinstance(arr, numpy.ndarray):
            arr = numpy.array(arr, self.DTYPE)

        if len(arr.shape) == 1:
            arr = arr.reshape((-1, 1))
        if arr.dtype != self.DTYPE:
            arr = arr.astype(self.DTYPE)
        if not arr.flags['C_CONTIGUOUS']:
            arr = numpy.ascontiguousarray(arr)
        return arr

    def fit(self, in_arr, target_arr):
        if not self.initialized_:
            self.mlp_init(**self.params_)
            self.run_filler()

        self.set_conf({'IsTrain': True})

        in_arr = self.check_arr(in_arr)
        target_arr = self.check_arr(target_arr)

        SIZE = len(in_arr)
        assert SIZE == len(target_arr)

        pos = numpy.arange(SIZE, dtype=numpy.int32)
        self.rate_ = self.rate_init

        for epoch in range(self.epoch_train):
            if epoch > 0 and epoch % self.epoch_decay == 0:
                self.rate_ *= self.rate_decay

            if self.shuffle:
                self.shuffle_array(pos)
            for idx in range(SIZE):
                idx_ = pos[idx]
                loss = self.train_one(
                    in_arr[idx_], target_arr[idx_], self.rate_, self.importance_out)
                if self.loss_ is None:
                    self.loss_ = loss
                else:
                    self.loss_ += (loss - self.loss_) * self.loss_mul

                if (idx + 1) % self.iteration_log == 0:
                    if math.isnan(self.loss_): 
                        print("loss is nan")
                        sys.exit() 

                    if self.verbose > 1:
                        print("Iteration %d/%d Epoch %d/%d\n    rate: %g loss: %g" %
                              (idx+1, SIZE, epoch, self.epoch_train, self.rate_, self.loss_))
                        sys.stdout.flush()

            if self.verbose > 0:
                print("Epoch %d/%d\n    rate: %g loss: %g" %
                      (epoch+1, self.epoch_train, self.rate_, self.loss_))
                sys.stdout.flush()

        if self.importance_out:
            self.feature_importances_ = numpy.zeros(
                (numpy.prod(self.tensors[0]['Shape']),), dtype=self.DTYPE)
            self.read_tensor(0, self.feature_importances_, self.FLAG_EX)

        return self

    def feed(self, in_arr, out_arr=None):
        self.set_conf({'IsTrain': False})

        in_arr = self.check_arr(in_arr)

        if out_arr is None:
            out_arr = numpy.zeros(
                (len(in_arr), numpy.prod(self.tensors[-1]['Shape'])), dtype=self.DTYPE)
        else:
            out_arr = self.check_arr(out_arr)

        SIZE = len(in_arr)
        assert SIZE == len(out_arr)

        for idx in range(SIZE):
            self.predict_one(in_arr[idx], out_arr[idx])

            if self.verbose_feed > 1:
                if (idx + 1) % self.iteration_log == 0:
                    print("Iteration %d/%d" % (idx+1, SIZE))

        return out_arr

    def predict_proba(self, in_arr, out_arr=None):
        out_arr = self.feed(in_arr, out_arr)

        return out_arr

    def predict(self, in_arr, out_arr=None):
        out_arr = self.feed(in_arr, out_arr)

        loss_type = self.tensors[-1]['LossType']
        if loss_type in ["softmax", "hardmax"]:
            return out_arr.argmax(axis=1)

        if len(out_arr.shape) == 2 and out_arr.shape[1] == 1:
            out_arr = out_arr.reshape(-1)

        return out_arr

    def train_one(self, in_buf, target_buf, rate, importance_out):
        self.clear_tensor(-1, self.FLAG_V | self.FLAG_DV)
        self.clear_filter(-1, self.FLAG_DV)
        self.input(0, in_buf)

        self.forward()

        loss = self.cal_loss(len(self.tensors) - 1, target_buf)

        # if loss_range[1] is not None and loss > loss_range[1]:
        #     return loss
        # if loss_range[0] is not None and loss < loss_range[0]:
        #     return loss

        self.backward()
        self.renew(rate)

        if importance_out:
            self.importance(0)

        return loss

    def predict_one(self, in_buf, out_buf):
        self.clear_tensor(-1, self.FLAG_V)
        self.input(0, in_buf)
        self.forward()

        flag = self.FLAG_V
        loss_type = self.tensors[-1]['LossType']
        if loss_type in ["softmax", "hardmax"]:
            flag = self.FLAG_EX

        self.read_tensor(len(self.tensors) - 1, out_buf, flag)


if __name__ == '__main__':
    m = MLP(layer_size=[2, 1],  op="conv", initialize=True)

    print("appname:", m.info("appname"))
    sys.stdout.flush()

    m.set_tensor(0,
                 {'Shape': [1, 2], 'Regularization': 0.1})

    m.show_conf()
    m.show_tensor()
    m.show_filter()
    m.destroy()
