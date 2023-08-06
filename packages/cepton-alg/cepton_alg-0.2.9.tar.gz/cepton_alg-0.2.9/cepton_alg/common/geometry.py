import numpy

from cepton_alg.common import *
import cepton_alg.common.transform

_all_builder = AllBuilder(__name__)


class Grid:
    def __init__(self, n_dims=3):
        self.lb = numpy.zeros([n_dims])
        self.spacing = numpy.zeros([n_dims])
        self.shape = numpy.zeros([n_dims], dtype=int)

    @property
    def n_dims(self):
        return len(self.shape)

    def check(self):
        if (len(self) > (numpy.iinfo(numpy.int32).max >> 1)):
            return False
        return True

    def __len__(self):
        if self.n_dims == 0:
            return 0
        return numpy.prod(self.shape)

    def __eq__(self, other):
        return (self.n_dims == other.n_dims) and \
            numpy.allclose(self.lb, other.lb) and \
            numpy.all(self.shape == other.shape) and \
            numpy.allclose(self.spacing, other.spacing)

    @property
    def ub(self):
        return self.lb + self.spacing * self.shape

    @property
    def ptp(self):
        return self.spacing * self.shape

    def set_shape_by_ub(self, ub):
        self.shape[:] = numpy.around((ub - self.lb) / self.spacing)

    def serialize(self):
        return {
            "n_dims": self.n_dims,
            "lb": self.lb.astype(float).tolist(),
            "shape": self.shape.astype(int).tolist(),
            "spacing": self.spacing.astype(float).tolist(),
        }

    @classmethod
    def deserialize(cls, d):
        self = cls(d["n_dims"])
        self.lb[:] = d["lb"]
        self.shape[:] = d["shape"]
        self.spacing[:] = d["spacing"]
        return self

    def find_valid_indices(self, indices):
        return numpy.logical_and(
            numpy.all(indices >= 0, axis=1),
            numpy.all(indices < self.shape, axis=-1)
        )

    def find_valid_flat_indices(self, flat_indices):
        return numpy.logical_and(flat_indices >= 0, flat_indices < len(self))

    def get_indices(self, positions, nearest=True):
        positions = numpy.reshape(positions, [-1, self.n_dims])
        indices = (positions - self.lb) / self.spacing
        if nearest:
            indices = numpy.around(indices).astype(int)
        else:
            indices = numpy.floor(indices).astype(int)
        is_invalid = numpy.logical_not(self.find_valid_indices(indices))
        indices[is_invalid, :] = -1
        return indices

    def to_flat_indices(self, indices):
        flat_indices = numpy.ravel_multi_index(
            indices.transpose(), self.shape, mode="clip")
        is_invalid = numpy.logical_not(self.find_valid_indices(indices))
        flat_indices[is_invalid] = -1
        return flat_indices

    def from_flat_indices(self, flat_indices):
        indices = numpy.stack(numpy.unravel_index(
            flat_indices, self.shape), axis=-1)
        is_invalid = numpy.logical_not(
            self.find_valid_flat_indices(flat_indices))
        indices[is_invalid] = -1
        return indices

    def get_flat_indices(self, positions, **kwargs):
        return self.to_flat_indices(self.get_indices(positions, **kwargs))

    def get_positions(self, indices):
        return indices * self.spacing + self.lb

    def get_flat_positions(self, flat_indices):
        return self.get_positions(self.from_flat_indices(flat_indices))


class Line(StructureOfArrays):
    def __init__(self, n=1, n_dims=3):
        super().__init__(n)
        self.direction = numpy.zeros([n, n_dims])
        self.position = numpy.zeros([n, n_dims])

    @classmethod
    def _get_array_member_names(cls):
        return ["direction", "position"]

    @property
    def n_dims(self):
        return self.direction.shape[1]


class Plane(StructureOfArrays):
    def __init__(self, n=1, n_dims=3):
        super().__init__(n)
        self.normal = numpy.zeros([n, n_dims])
        self.position = numpy.zeros([n, n_dims])

        self.normal[:, -1] = 1

    @classmethod
    def _get_array_member_names(cls):
        return ["normal", "position"]

    @property
    def n_dims(self):
        return self.normal.shape[1]


class Ball(StructureOfArrays):
    def __init__(self, n=1):
        self.center = numpy.zeros([n, 3])
        self.radius = numpy.zeros([n])

    @classmethod
    def _get_array_member_names(cls):
        return ["center", "radius"]


def create_box(n_dims):
    class Box(StructureOfArrays):
        def __init__(self, n=1):
            super().__init__(n)
            self.dimensions = numpy.zeros([n, n_dims])
            self.transform = cepton_alg.common.transform.Transform3d(n)

        @property
        def n_dims(self):
            return n_dims

        @classmethod
        def _get_array_member_names(cls):
            return ["dimensions", "transform"]

        # def serialize(self):
        #     rotation = self.transform.rotation.to_vector()
        #     return [{
        #         "dimensions": self.dimensions[i, :].astype(float).tolist(),
        #         "translation": self.transform.translation[i, :].astype(float).tolist(),
        #         "rotation": rotation[i, :].astype(float).tolist(),
        #     } for i in range(len(self))]

        # @classmethod
        # def deserialize(cls, l):
        #     self = cls(len(l))
        #     rotations = numpy.zeros([len(l), 4])
        #     for i, d in enumerate(l):
        #         self.dimensions[:, i] = d["dimensions"]
        #         self.transform.translation[:, i] = d["translation"]
        #         rotations[:, i] = d["rotation"]
        #     self.transform.rotation[:].update_from_vector(rotations)
    return Box


# Box2d = create_box(2)
Box3d = create_box(3)


def distance_to_plane(plane, positions):
    return vector_dot(positions - plane.position, plane.normal)


def distance_to_line(line, positions):
    d = vector_dot(positions - line.position, line.direction)
    projected_positions = line.position + d * line.direction
    return vector_norm(positions - projected_positions)


def plane_line_intersection(plane, line):
    # https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
    # TODO: vectorize
    scale = vector_dot(line.direction, plane.normal)
    if scale == 0:
        # Parallel
        return numpy.full([1, 3], numpy.NaN)
    offset = plane.position - line.position
    d = vector_dot(offset, plane.normal) / scale
    return d * line.direction + line.position


def compute_ground_transform(ground_plane):
    ground_transform = cepton_alg.common.transform.Transform3d()
    ground_transform.translation[:, 2] = distance_to_plane(
        ground_plane, [0, 0, 0])
    ground_transform.rotation.update_from_two_vectors(
        ground_plane.normal, [0, 0, 1])
    return ground_transform


__all__ = _all_builder.get()
