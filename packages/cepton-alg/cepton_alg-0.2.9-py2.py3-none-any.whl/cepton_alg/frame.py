import collections
import copy
import ctypes
import enum
import itertools
import json

import numpy

import cepton_alg.c
import cepton_alg.common.c
import cepton_alg.common.geometry
import cepton_alg.common.transform
import cepton_sdk
import cepton_sdk.c
import cepton_util.common
from cepton_alg.common import *

_all_builder = AllBuilder(__name__)


class ListEnum:
    """List of enums supporting lookup by name/index."""

    def __init__(self, fields):
        super().__init__()

        self._fields = fields
        self._fields_by_name = {x.name: x for x in self._fields}
        self._indices = {x.name: i for i, x in enumerate(self._fields)}

    def __getitem__(self, key):
        return self._fields_by_name[key]

    def __iter__(self):
        return iter(self._fields)

    def get_by_index(self, i):
        return self._fields[i]

    def get_index(self, value):
        return self._indices[value.name]


def combine_enums(enum_types):
    fields = list(itertools.chain.from_iterable(enum_types))
    return ListEnum(fields)


class PointFlag(enum.IntEnum):
    IS_CEILING = 0
    IS_CURB = 1
    IS_DEBUG_1 = 2
    IS_DEBUG_2 = 3
    IS_DOWNSAMPLED_COARSE = 4
    IS_DOWNSAMPLED_FINE = 5
    IS_FILTERED = 6
    IS_GROUND = 7
    IS_INVALID = 8
    IS_OCCLUDED = 9
    IS_STATIONARY = 10


CombinedPointFlag = combine_enums([cepton_sdk.point.PointFlag, PointFlag])


class Points(cepton_sdk.Points):
    def __init__(self, n=0):
        super().__init__(n)
        self.serial_numbers = numpy.zeros(n, dtype=int)
        self.segment_indices = numpy.zeros(n, dtype=int)
        self.scanline_labels = numpy.zeros(n, dtype=int)
        self.surface_indices = numpy.zeros([n], dtype=int)
        self.object_indices = numpy.zeros([n], dtype=int)
        self.alg_flags = numpy.zeros([n, 32], dtype=bool)
        self.shading = numpy.ones([n])

    @classmethod
    def _get_c_class(cls):
        return cepton_alg.c.C_Point

    @classmethod
    def _get_array_member_names(cls):
        return super()._get_array_member_names() + [
            "serial_numbers", "segment_indices", "scanline_labels",
            "surface_indices", "object_indices",  "alg_flags", "shading"]

    def _from_c_impl(self, data):
        super()._from_c_impl(data["image_point"])
        self.serial_numbers[:] = data["serial_number"]
        self.segment_indices[:] = data["segment_idx"]
        self.positions[:, :] = data["position"]
        self.scanline_labels[:] = data["scanline_label"]
        self.surface_indices[:] = data["surface_idx"]
        self.object_indices[:] = data["object_idx"]
        self.alg_flags[:, :] = cepton_alg.common.c.unpack_bits(data["flags"])

    def get_flag(self, flag):
        if isinstance(flag, cepton_sdk.point.PointFlag):
            return self.flags[:, flag]
        elif isinstance(flag, PointFlag):
            return self.alg_flags[:, flag]
        else:
            return super().get_flag(flag)

    @property
    def is_ceiling(self):
        return self.alg_flags[:, PointFlag.IS_CEILING]

    @property
    def is_curb(self):
        return self.alg_flags[:, PointFlag.IS_CURB]

    @property
    def is_debug_1(self):
        return self.alg_flags[:, PointFlag.IS_DEBUG_1]

    @property
    def is_debug_2(self):
        return self.alg_flags[:, PointFlag.IS_DEBUG_2]

    @property
    def is_downsampled_coarse(self):
        return self.alg_flags[:, PointFlag.IS_DOWNSAMPLED_COARSE]

    @property
    def is_downsampled_fine(self):
        return self.alg_flags[:, PointFlag.IS_DOWNSAMPLED_FINE]

    @property
    def is_filtered(self):
        return self.alg_flags[:, PointFlag.IS_FILTERED]

    @property
    def is_ground(self):
        return self.alg_flags[:, PointFlag.IS_GROUND]

    @property
    def is_invalid(self):
        return self.alg_flags[:, PointFlag.IS_INVALID]

    @property
    def is_occluded(self):
        return self.alg_flags[:, PointFlag.IS_OCCLUDED]

    @property
    def is_stationary(self):
        return self.alg_flags[:, PointFlag.IS_STATIONARY]


class Surfaces(StructureOfArrays, ToCArrayMixin):
    def __init__(self, n=0):
        super().__init__(n)
        self.labels = numpy.zeros([n], dtype=int)
        self.planes = cepton_alg.common.geometry.Plane(n)

    @classmethod
    def _get_c_class(cls):
        return cepton_alg.c.C_Surface

    @classmethod
    def _get_array_member_names(cls):
        return ["labels", "planes"]

    def _from_c_impl(self, data):
        self.labels[:] = data["label"]
        self.planes.position[:, :] = data["position"]
        self.planes.normal[:, :] = data["normal"]


@enum.unique
class ObjectType(enum.IntEnum):
    UNKOWN = 0
    SCENERY = 1
    CAR = 2
    BICYCLE = 3
    PERSON = 4


class ObjectFlag(enum.IntEnum):
    IS_VALID = 0
    IS_MOVING = 1


class Objects(StructureOfArrays, ToCArrayMixin):
    def __init__(self, n=0):
        super().__init__(n)
        self.labels = numpy.full([n], -1, dtype=int)
        self.types = numpy.zeros([n], dtype=int)
        self.transforms = cepton_alg.common.transform.Transform3d(n)
        self.velocities_translation = numpy.zeros([n, 3])
        self.trajectory_sizes = numpy.zeros([n], dtype=int)
        self.trajectories = numpy.zeros([n, 10, 3])
        self.boxes = cepton_alg.common.geometry.Box3d(n)
        self.flags = numpy.zeros([n, 8], dtype=bool)

    @classmethod
    def _get_c_class(cls):
        return cepton_alg.c.C_Object

    @classmethod
    def _get_array_member_names(cls):
        return ["labels", "types", "transforms", "velocities_translation",
                "trajectory_sizes", "trajectories", "boxes", "flags"]

    def _from_c_impl(self, data):
        self.labels[:] = data["label"]
        self.types[:] = data["type"]
        self.transforms.translation[:, :] = data["translation"]
        self.velocities_translation[:, :] = data["velocity_translation"]
        self.trajectory_sizes[:] = data["trajectory_size"]
        self.trajectories[:, :, :] = data["trajectory"].reshape([-1, 10, 3])
        for i in range(len(self)):
            self.trajectories[i, self.trajectory_sizes[i]:, :] = numpy.nan
        self.boxes.dimensions[:, :] = data["box_dimensions"]
        self.boxes.transform.translation[:, :] = data["box_translation"]
        self.boxes.transform.rotation.update_from_vector(data["box_rotation"])
        self.flags[:] = cepton_alg.common.c.unpack_bits(data["flags"])

    @property
    def is_valid(self):
        return self.flags[:, ObjectFlag.IS_VALID]

    @property
    def is_moving(self):
        return self.flags[:, ObjectFlag.IS_MOVING]


class OccupancyCellFlag(enum.IntEnum):
    VALID = 0


class OccupancyCells(StructureOfArrays, ToCArrayMixin):
    def __init__(self, n=0):
        super().__init__(n)
        self.flags = numpy.zeros([n, 8], dtype=bool)

    @classmethod
    def _get_c_class(cls):
        return cepton_alg.c.C_OccupancyCell

    @classmethod
    def _get_array_member_names(cls):
        return ["flags"]

    def _from_c_impl(self, data):
        self.flags[:, :] = cepton_alg.common.c.unpack_bits(data["flags"])

    @property
    def is_valid(self):
        return self.flags[:, OccupancyCellFlag.VALID]


class Frame:
    def __init__(self, n_points=0, n_surfaces=0, n_objects=0, n_occupancy_cells=0):
        super().__init__()
        self.idx = 0
        self.timestamp = 0.0
        self.timestamp_min = 0.0
        self.timestamp_max = 0.0
        self.motion_state = cepton_alg.common.transform.MotionState3d()
        self.ground_plane = cepton_alg.common.geometry.Plane()
        self.ceiling_plane = cepton_alg.common.geometry.Plane()
        self.points = Points(n_points)
        self.surfaces = Surfaces(n_surfaces)
        self.objects = Objects(n_objects)
        self.occupancy_grid = cepton_alg.common.geometry.Grid(2)
        self.occupancy_cells = OccupancyCells(n_occupancy_cells)
        self.debug_message = {}

    def update_from_c_frame_data(self, c_frame_data):
        if isinstance(c_frame_data, ctypes._Pointer):
            c_frame_data = c_frame_data.contents
        self.idx = c_frame_data.idx
        self.timestamp = cepton_util.common.from_usec(c_frame_data.timestamp)

        self.motion_state.timestamp[:] = self.timestamp
        self.motion_state.transform.translation[:, :] = c_frame_data.position
        self.motion_state.transform.rotation.update_from_vector(
            c_frame_data.orientation)
        self.motion_state.velocity.translation[:] = \
            c_frame_data.velocity_translation
        self.motion_state.velocity.rotation_vector = \
            c_frame_data.velocity_rotation

        self.ground_plane.normal[:, :] = c_frame_data.ground_plane_normal
        self.ground_plane.position[:, :] = c_frame_data.ground_plane_position
        self.ceiling_plane.normal[:, :] = c_frame_data.ceiling_plane_normal
        self.ceiling_plane.position[:, :] = \
            c_frame_data.ceiling_plane_position

        self.occupancy_grid.shape[:] = c_frame_data.occupancy_grid_shape
        self.occupancy_grid.lb[:] = c_frame_data.occupancy_grid_lb
        self.occupancy_grid.spacing[:] = c_frame_data.occupancy_grid_spacing

    @classmethod
    def from_c(cls, c_frame_data, n_points, c_points, n_surfaces, c_surfaces,
               n_objects, c_objects, n_occupancy_cells, c_occupancy_cells,
               c_debug_message):
        self = cls(n_points=n_points, n_surfaces=n_surfaces,
                   n_objects=n_objects, n_occupancy_cells=n_occupancy_cells)
        self.update_from_c_frame_data(c_frame_data)
        self.points = self.points.from_c(n_points, c_points)
        self.surfaces = self.surfaces.from_c(n_surfaces, c_surfaces)
        self.objects = self.objects.from_c(n_objects, c_objects)
        self.occupancy_cells = self.occupancy_cells.from_c(
            n_occupancy_cells, c_occupancy_cells)
        debug_message = json.loads(c_debug_message.decode("utf-8"))
        if debug_message:
            self.debug_message = debug_message

        self.timestamp_min = numpy.amin(self.points.timestamps)
        self.timestamp_max = numpy.amax(self.points.timestamps)

        # HACK
        self.timestamp = self.timestamp_max
        self.motion_state.timestamp[:] = self.timestamp
        # assert(self.timestamp >= self.timestamp_min)
        # assert(self.timestamp <= self.timestamp_max)

        return self


class AccumulatedObject:
    def __init__(self, label, time_span=0.3):
        # Object label.
        self.label = label

        # Point positions of the object.
        # The positions from different times are all projected
        # into the latest time before store in this field.
        self.point_positions = numpy.zeros([0, 3])

        # The timestamp of positions stored.
        self.timestamp = 0

        # The original time stamps of all the points.
        self.raw_timestamps = numpy.array([])

        # Time span of points to accumulate
        self.time_span = time_span

        # Transform speed.
        self.transform_speed = cepton_alg.common.transform.Transform3d()

    def add_observation(self, timestamp, positions, transform_speed):
        """
        Add point positions to the object
        :param timestamp: timestamp of the incoming points.
        :param positions: point positions in XYZ.
        :param transform_speed: new transform speed.
        :return: updated object instance.
        """
        assert(timestamp >= self.timestamp)
        self.transform_speed = transform_speed
        self.advance_to(timestamp)
        self.raw_timestamps = numpy.append(self.raw_timestamps,
                                           timestamp * numpy.ones(positions.shape[0]))
        self.point_positions = numpy.append(
            self.point_positions, positions, axis=0)
        return self

    def advance_to(self, timestamp):
        """
        Project stored positions to given timestamp.
        The points older than time span are discarded.
        :param timestamp: target timestamp.
        :return: updated object.
        """
        assert(timestamp >= self.timestamp)

        # Discard very old points.
        index = timestamp - self.raw_timestamps < self.time_span
        self.raw_timestamps = self.raw_timestamps[index]
        self.point_positions = self.point_positions[index, :]

        # Project points to given timestamp.
        transform = self._get_transform((timestamp - self.timestamp))
        self.point_positions = transform.apply(self.point_positions)
        self.timestamp = timestamp
        return self

    def _get_transform(self, t):
        """
        Get transform by time duration.
        :param t: time duration in seconds.
        :return: the 3d transform.
        """
        transform = self.transform_speed
        transform.translation[:] *= t
        transform.rotation[:] = cepton_alg.common.transform.Quaternion()
        return transform


class AccumulatedFrame(Frame):
    """ This class generates point cloud by accumulating a bunch of frames.
    """

    def __init__(self, time_span=0.3):
        super().__init__()
        self.time_span = time_span  # time span to accumulate in seconds.
        self.accumulated_objects = {}  # dictionary of accumulated objects.

    def update_accumulated_objects(self, frame):
        """
        Update accumulated objects with the latest object list.

        :param frame: the new frame.
        :return: updated frame.
        """
        self.timestamp = frame.timestamp
        self.objects = frame.objects
        self.points = frame.points
        self.ground_plane = frame.ground_plane
        self.ceiling_plane = frame.ceiling_plane
        self.surfaces = frame.surfaces

        for i in range(len(frame.objects)):
            label = frame.objects.labels[i]
            if label not in self.accumulated_objects:
                self.accumulated_objects[label] = AccumulatedObject(
                    label, self.time_span)
            positions = self.points.positions[
                self.points.object_indices == i, :]
            transform_speed = cepton_alg.common.transform.Transform3d()
            transform_speed.translation[:] = frame.objects.velocities_translation[i]
            self.accumulated_objects[label].add_observation(
                frame.timestamp, positions, transform_speed)

        # clean very old object
        for label in list(self.accumulated_objects.keys()):
            if self.timestamp - self.accumulated_objects[label].timestamp > self.time_span:
                del self.accumulated_objects[label]

    def get_frame(self):
        pass
        # for label in frame.accumulated_objects:
        #     cur_points = frame.accumulated_objects[label].point_positions
        #     positions = numpy.append(positions, cur_points, axis=0)
        #     color_values = numpy.append(
        #         color_values, label * numpy.ones(cur_points.shape[0]))


def _find(a, values):
    indices = numpy.searchsorted(a, values)
    is_valid = indices < len(a)
    indices[numpy.logical_not(is_valid)] = -1

    indices_tmp = indices[is_valid]
    is_invalid_tmp = a[indices_tmp] != values[is_valid]
    indices_tmp[is_invalid_tmp] = -1
    indices[is_valid] = indices_tmp

    return indices


class SimpleFrameAccumulator:
    """Accumulates frames by ego motion only (ignores object speed)."""

    def __init__(self):
        self.frames = collections.deque([], 10)

    def clear(self):
        self.frames.clear()

    def add_frame(self, frame):
        self.frames.appendleft(frame)

    @property
    def timestamp_min(self):
        if len(self.frames) == 0:
            return 0
        return self.frames[-1].timestamp_min

    @property
    def timestamp_max(self):
        if len(self.frames) == 0:
            return 0
        return self.frames[0].timestamp_max

    def has_frame(self, timestamp=None):
        if len(self.frames) == 0:
            return False
        if timestamp is None:
            timestamp = self.timestamp_max
        elif timestamp > self.timestamp_max:
            return False
        return True

    def get_frame(self, timestamp=None, frame_length=0.1, interpolate=False, relative=True):
        if not self.has_frame(timestamp):
            return None

        if timestamp is None:
            timestamp = self.timestamp_max
            i_frame_0 = 0
        else:
            i_frame_0 = None
            for i in range(len(self.frames)):
                if self.frames[i].timestamp_min < timestamp:
                    i_frame_0 = i
                    break
            if i_frame_0 is None:
                return None
        timestamp_min = timestamp - frame_length

        frame = self.frames[i_frame_0]
        result_frame = copy.deepcopy(frame)
        if interpolate:
            result_frame.motion_state.transform[:] = \
                result_frame.motion_state.integrate(timestamp)

        # HACK: unmatched objects
        result_frame.objects = Objects(len(frame.objects) + 1)
        result_frame.objects[:-1] = frame.objects
        result_frame.objects.flags[-1, ObjectFlag.IS_VALID] = True

        points_list = []
        for i in range(i_frame_0, len(self.frames)):
            frame = self.frames[i]
            if frame.timestamp_max < timestamp_min:
                break
            points = copy.deepcopy(frame.points)

            points.positions[:, :] = frame.motion_state.transform.apply(
                points.positions)

            # Update surface indices
            points.surface_indices[:] = -1

            # Update object indices
            is_valid = points.object_indices >= 0
            object_labels = frame.objects.labels[points.object_indices[is_valid]]
            object_indices = _find(result_frame.objects.labels, object_labels)

            # HACK: unmatched objects
            is_valid_object = frame.objects.is_valid[points.object_indices[is_valid]]
            is_unmatched = object_indices < 0
            is_unmatched[numpy.logical_not(is_valid_object)] = False
            object_indices[is_unmatched] = len(result_frame.objects) - 1

            points.object_indices[is_valid] = object_indices

            points_list.append(points)
        if len(points_list) == 0:
            return None
        points = cepton_sdk.combine_points(points_list)
        is_valid = numpy.logical_and(
            points.timestamps >= timestamp_min, points.timestamps <= timestamp)
        points = points[is_valid]
        if relative:
            transform = result_frame.motion_state.transform.inverse()
            points.positions[:, :] = transform.apply(points.positions)
        result_frame.points = points
        return result_frame


__all__ = _all_builder.get()
