import numpy

from cepton_alg.common import *

_all_builder = AllBuilder(__name__)


class Rate(object):
    def __init__(self, period):
        self.period = period

        self.reset()

    def reset(self):
        self.i = 0

    def next(self, t=None):
        if t is not None:
            self.seek(t)
        self.i += 1
        return self.t

    @property
    def t(self):
        return self.i * self.period

    @t.setter
    def t(self, value):
        self.i = int(numpy.ceil(value / self.period))


__all__ = _all_builder.get()
