import numpy
import numpy.linalg

from cepton_alg.common import *

_all_builder = AllBuilder(__name__)


def vector_norm(a, axis=-1, **kwargs):
    return numpy.linalg.norm(a, axis=axis, **kwargs)


def vector_normalize(a, axis=-1):
    a_norm = numpy.linalg.norm(a, axis=axis, keepdims=True)
    a_norm[a_norm == 0] = 1
    return (a / a_norm)


def vector_dot(a1, a2, axis=-1):
    return numpy.sum(a1 * a2, axis=axis)


def vector_outer(a1, a2, axis=-1):
    a1 = numpy.expand_dims(a1, axis)
    a2 = numpy.expand_dims(a2, axis - 1)
    return a1 * a2


def matrix_multiply(m1, m2):
    return numpy.matmul(m1, m2)


def vector_matrix_multiply(v, m):
    return numpy.squeeze(numpy.matmul(numpy.expand_dims(v, axis=-2), m), axis=-2)
    # return numpy.sum(numpy.expand_dims(v, axis=-1) * m, axis=-2)


def matrix_vector_multiply(m, v):
    return numpy.squeeze(numpy.matmul(m, numpy.expand_dims(v, axis=-1)), axis=-1)
    # return numpy.sum(m * numpy.expand_dims(v, axis=-2), axis=-1)


__all__ = _all_builder.get()
