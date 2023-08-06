# coding: utf-8
from __future__ import print_function, division, unicode_literals, absolute_import

import os
import sys
import ctypes
import platform
import numpy

try:
    from . import conlib
except:
    import conlib


class Mesh(object):
    __version__ = 4

    FLAG_V = 1
    FLAG_DV = 2
    FLAG_EX = 4

    MESH_LEN = 0

    def __init__(self, dtype="float64"):
        self.mesh_init(dtype=dtype)

    def mesh_init(self, dtype):
        self.mi_ = Mesh.MESH_LEN
        Mesh.MESH_LEN += 1

        self.conf_ = {}
        self.tensors = []
        self.filters = []

        if dtype == numpy.float64 or dtype in ["float64", "double"]:
            self.DTYPE = numpy.float64
            self.C_FLOAT = ctypes.c_double

            _basedir = os.path.dirname(os.path.abspath(__file__))
            if platform.system() == "Windows":
                self._libc = ctypes.cdll.LoadLibrary(
                    os.path.join(_basedir, 'mesh.dll.2'))
            elif platform.system() == "Linux":
                self._libc = ctypes.cdll.LoadLibrary(
                    os.path.join(_basedir, 'mesh.so.2'))
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()

        self._libc.mesh_cal_loss.restype = self.C_FLOAT
        self._libc.mesh_random.restype = self.C_FLOAT

        if isinstance(Mesh.__version__, int):
            Mesh.__version__ = self.info(
                "version") + '.' + str(Mesh.__version__)
            print(self.info("appname"), Mesh.__version__)

        # print('mesh init', self.mi_)
        sys.stdout.flush()

    def save_model(self, filepath="model.bin"):
        ret = self._libc.mesh_save_model(self.mi_, filepath.encode())
        if ret <= 0:
            raise ValueError()

    def load_model(self, filepath="model.bin"):
        ret = self._libc.mesh_load_model(self.mi_, filepath.encode())
        if ret <= 0:
            raise ValueError()

    def set_conf(self, con={}):
        if not isinstance(con, dict):
            raise NotImplementedError()

        self.conf_.update(con)

        con = conlib.dumps(con).encode()
        self._libc.mesh_set_conf(self.mi_, con)

    def set_tensor(self, ti, con={}):
        if not isinstance(con, dict):
            raise NotImplementedError()

        while ti >= len(self.tensors):
            self.tensors.append({})

        self.tensors[ti].update(con)

        con = conlib.dumps(con).encode()
        self._libc.mesh_set_tensor(self.mi_, ti, con)

    def set_filter(self, fi, con={}):
        if isinstance(fi, dict):
            con = fi
            fi = len(self.filters)

        if not isinstance(con, dict):
            raise NotImplementedError()

        while fi >= len(self.filters):
            self.filters.append({})

        self.filters[fi].update(con)

        con = conlib.dumps(con).encode()
        self._libc.mesh_set_filter(self.mi_, fi, con)

    def clear_tensor(self, ti=-1, flag=FLAG_V | FLAG_DV):
        self._libc.mesh_clear_tensor(self.mi_, ti, flag)

    def clear_filter(self, fi=-1, flag=FLAG_DV):
        self._libc.mesh_clear_filter(self.mi_, fi, flag)

    def importance(self, ti=-1):
        self._libc.mesh_importance(self.mi_, ti)

    def input(self, ti, buf):
        self._libc.mesh_input(self.mi_, ti, numpy.ctypeslib.as_ctypes(buf))

    def cal_loss(self, ti, buf=None):
        return self._libc.mesh_cal_loss(self.mi_, ti, numpy.ctypeslib.as_ctypes(buf))

    def read_tensor(self, ti, buf, flag):
        self._libc.mesh_read_tensor(
            self.mi_, ti, numpy.ctypeslib.as_ctypes(buf), flag)

    def run_filler(self, fi=-1):
        self._libc.mesh_run_filler(self.mi_, fi)

    def forward(self):
        self._libc.mesh_forward(self.mi_)

    def backward(self):
        self._libc.mesh_backward(self.mi_)

    def renew(self, rate):
        self._libc.mesh_renew(self.mi_, self.C_FLOAT(rate))

    def destroy(self):
        self._libc.mesh_destroy(self.mi_)

    def random(self):
        return self._libc.mesh_random()

    def shuffle_array(self, buf):
        if buf.dtype != numpy.int32:
            raise NotImplementedError()
        self._libc.mesh_shuffle(numpy.ctypeslib.as_ctypes(buf), buf.shape[0])

    def info(self, info_type=None, buf_size=1024):
        if self._libc is None:
            return
        if not conlib.is_str(info_type):
            info_type = None
        else:
            info_type = info_type.encode()

        str_buf = ctypes.create_string_buffer(buf_size)
        self._libc.mesh_info(info_type, str_buf)

        return str_buf.value.decode()

    def show_conf(self):
        if self._libc is None:
            return
        self._libc.mesh_show_conf(self.mi_)

    def show_tensor(self, ti=-1):
        if self._libc is None:
            return
        self._libc.mesh_show_tensor(self.mi_, ti)

    def show_filter(self, fi=-1):
        if self._libc is None:
            return
        self._libc.mesh_show_filter(self.mi_, fi)


if __name__ == '__main__':
    pass
