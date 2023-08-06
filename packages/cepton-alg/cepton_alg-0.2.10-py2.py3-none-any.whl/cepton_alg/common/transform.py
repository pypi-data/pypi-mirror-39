import copy

import numpy

from cepton_alg.common import *

_all_builder = AllBuilder(__name__)


class Quaternion(StructureOfArrays):
    def __init__(self, n=1):
        super().__init__(n)
        self.s = numpy.ones([n])
        self.v = numpy.zeros([n, 3])

    @classmethod
    def _get_array_member_names(cls):
        return ["s", "v"]

    @property
    def norm(self):
        return numpy.sqrt(numpy.sum(self.v**2, axis=-1) + self.s**2)

    def normalize(self):
        norm = self.norm
        is_valid = norm != 0
        self.s[is_valid] /= norm[is_valid]
        self.v[is_valid, :] /= norm[is_valid, numpy.newaxis]

    @property
    def is_normalized(self):
        return numpy.abs(self.norm - 1) < 1e-10

    def inverse(self):
        obj = copy.deepcopy(self)
        obj.v[:, :] *= -1
        return obj

    def update_from_two_vectors(self, v1, v2):
        # http://lolengine.net/blog/2013/09/18/beautiful-maths-quaternion-from-vectors
        v1 = numpy.reshape(v1, [-1, 3])
        v2 = numpy.reshape(v2, [-1, 3])
        self.v[:, :] = numpy.cross(v1, v2)
        self.s[:] = vector_dot(v1, v2)
        self.s[:] += self.norm
        self.normalize()

    @classmethod
    def from_two_vectors(cls, v1, v2):
        n1 = numpy.reshape(v1, [-1, 3]).shape[0]
        n2 = numpy.reshape(v2, [-1, 3]).shape[0]
        n = max(n1, n2)
        self = cls(n)
        self.update_from_two_vectors(v1, v2)
        return self

    def update_from_vector(self, v, scalar_first=False):
        v = numpy.reshape(v, [-1, 4])
        if scalar_first:
            self.s[:] = v[:, 0]
            self.v[:, :] = v[:, 1:]
        else:
            self.v[:, :] = v[:, :3]
            self.s[:] = v[:, 3]
        self.normalize()

    @classmethod
    def from_vector(cls, v, **kwargs):
        n = numpy.reshape(v, [-1, 4]).shape[0]
        self = cls(n)
        self.update_from_vector(v, **kwargs)
        return self

    def to_vector(self, scalar_first=False):
        v = numpy.zeros([len(self), 4])
        if scalar_first:
            v[:, 0] = self.s
            v[:, 1:] = self.v
        else:
            v[:, :3] = self.v
            v[:, 3] = self.s
        return v

    def to_matrix(self):
        wv = 2.0 * self.s[:, numpy.newaxis] * self.v
        xv = 2.0 * self.v[:, [0]] * self.v
        yv = 2.0 * self.v[:, [1]] * self.v
        zv = 2.0 * self.v[:, [2]] * self.v

        result = numpy.zeros([len(self), 3, 3])
        result[:, 0, 0] = 1 - (yv[:, 1] + zv[:, 2])
        result[:, 0, 1] = xv[:, 1] - wv[:, 2]
        result[:, 0, 2] = xv[:, 2] + wv[:, 1]
        result[:, 1, 1] = 1 - (xv[:, 0] + zv[:, 2])
        result[:, 1, 2] = yv[:, 2] - wv[:, 0]
        result[:, 2, 2] = 1 - (xv[:, 0] + yv[:, 1])

        result[:, 1, 0] = xv[:, 1] + wv[:, 2]
        result[:, 2, 0] = xv[:, 2] - wv[:, 1]
        result[:, 2, 1] = yv[:, 2] + wv[:, 0]

        return result

    def update_from_angle_axis(self, angle, axis):
        angle = numpy.reshape(angle, [-1])
        axis = numpy.reshape(axis, [-1, 3])
        self.s[:] = numpy.cos(angle / 2)
        self.v[:, :] = axis * numpy.sin(angle / 2)[:, numpy.newaxis]

    @classmethod
    def from_angle_axis(cls, angle, axis):
        n = numpy.reshape(angle, [-1]).shape[0]
        self = cls(n)
        self.update_from_angle_axis(angle, axis)
        return self

    def to_angle_axis(self):
        assert(self.is_normalized)

        angle = numpy.zeros([len(self)])
        axis = numpy.zeros([len(self), 3])
        scale = vector_norm(self.v)
        if scale == 0:
            axis[:, 2] = 1
        else:
            angle[:] = 2 * numpy.arctan2(scale, self.s)
            axis[:, :] = self.v / scale[:, numpy.newaxis]
        return angle, axis

    def apply(self, v):
        v = numpy.reshape(v, [-1, 3, 1])
        return numpy.matmul(self.to_matrix(), v)[:, :, 0]

    def product(self, other):
        assert(isinstance(other, Quaternion))

        n = max(len(self), len(other))
        cls = type(self)
        result = cls(n)
        result.s[:] = self.s * other.s - vector_dot(self.v, other.v)
        result.v[:, :] = self.s[:, numpy.newaxis] * other.v + \
            other.s[:, numpy.newaxis] * self.v + numpy.cross(self.v, other.v)
        return result

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return self.product(other)
        else:
            return self.apply(other)


class Transform3d(StructureOfArrays):
    def __init__(self, n=1):
        super().__init__(n)
        self.rotation = Quaternion(n)
        self.translation = numpy.zeros([n, 3])

    @classmethod
    def _get_array_member_names(cls):
        return ["rotation", "translation"]

    def inverse(self):
        obj = copy.deepcopy(self)
        obj.rotation[:] = self.rotation.inverse()
        obj.translation[:, :] = obj.rotation.apply(-self.translation)
        return obj

    def to_matrix(self):
        result = numpy.zeros([len(self), 4, 4])
        result[:, :3, :3] = self.rotation.to_matrix()
        result[:, :3, 3] = self.translation
        result[:, 3, 3] = 1
        return result

    def inverse(self, return_copy=True):
        cls = type(self)
        result = cls(len(self))
        result.rotation[:] = self.rotation.inverse()
        result.translation[:, :] = result.rotation.apply(-self.translation)
        return result

    def apply(self, v):
        return self.rotation.apply(v) + self.translation

    def product(self, other):
        assert(isinstance(other, Transform3d))

        n = max(len(self), len(other))
        cls = type(self)
        result = cls(n)
        result.rotation[:] = self.rotation.product(other.rotation)
        result.translation[:, :] = self.translation + \
            self.rotation.apply(other.translation)
        return result

    def __mul__(self, other):
        if isinstance(other, Transform3d):
            return self.product(other)
        else:
            return self.apply(other)


class Velocity3d(StructureOfArrays):
    def __init__(self, n=1):
        super().__init__(n)
        self.translation = numpy.zeros([n, 3])
        self.rotation_angle = numpy.zeros([n])
        self.rotation_axis = numpy.zeros([n, 3])

    @classmethod
    def _get_array_member_names(cls):
        return ["translation", "rotation_angle", "rotation_axis"]

    @property
    def rotation_vector(self):
        return self.rotation_angle[:, numpy.newaxis] * self.rotation_axis

    @rotation_vector.setter
    def rotation_vector(self, v):
        self.rotation_angle[:] = vector_norm(v)
        self.rotation_axis[:, :] = vector_normalize(v)

    def integrate(self, t_diff):
        t_diff = numpy.reshape(t_diff, [-1])
        result = Transform3d(len(self))
        result.translation[:, :] = self.translation * t_diff[:, numpy.newaxis]
        result.rotation[:] = Quaternion.from_angle_axis(
            self.rotation_angle * t_diff, self.rotation_axis)
        return result


class MotionState3d(StructureOfArrays):
    def __init__(self, n=1):
        super().__init__(n)
        self.timestamp = numpy.zeros([n])
        self.transform = Transform3d(n)
        self.velocity = Velocity3d(n)

    @classmethod
    def _get_array_member_names(cls):
        return ["timestamp", "transform", "velocity"]

    def integrate(self, timestamp):
        transform_diff = self.velocity.integrate(timestamp - self.timestamp)
        return self.transform * transform_diff


__all__ = _all_builder.get()
