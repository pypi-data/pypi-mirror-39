import os
from ctypes import *

import cepton_sdk.c
from cepton_alg.common import *
from cepton_sdk.common.c import *

_all_builder = AllBuilder(__name__)

from cepton_sdk.c import C_Error, C_ErrorCode, C_Warning  # noqa isort:skip

ALG_VERSION = 2


_module_dir = os.path.dirname(os.path.abspath(__file__))
lib = load_c_library(_module_dir, "cepton_alg")

# ------------------------------------------------------------------------------
# General
# ------------------------------------------------------------------------------
c_get_version_string = lib.cepton_alg_get_version_string
c_get_version_string.restype = c_char_p

c_get_version_major = lib.cepton_alg_get_version_major
c_get_version_major.restype = c_int

c_get_version_minor = lib.cepton_alg_get_version_minor
c_get_version_minor.restype = c_int


def get_version_string():
    return c_get_version_string().decode("utf-8")


def get_version_major():
    return c_get_version_major()


def get_version_minor():
    return c_get_version_minor()

# ------------------------------------------------------------------------------
# Errors
# ------------------------------------------------------------------------------


c_get_error = lib.cepton_alg_get_error
c_get_error.argtypes = [POINTER(c_char_p)]
c_get_error.restype = c_int


def get_error():
    error_msg = c_char_p()
    error_code = c_get_error(byref(error_msg))
    return C_Error(error_code, error_msg.value.decode("UTF-8"))


def _c_error_check(error_code, func, args):
    cepton_sdk.c.check_error(get_error())


def add_c_error_check(c_func):
    c_func.restype = c_int
    c_func.errcheck = _c_error_check

# ------------------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------------------


c_is_initialized = lib.cepton_alg_is_initialized
c_is_initialized.restype = c_int

c_initialize = lib.cepton_alg_initialize
c_initialize.argtypes = [c_int, c_char_p]
add_c_error_check(c_initialize)

c_deinitialize = lib.cepton_alg_deinitialize
c_deinitialize.argtypes = []
add_c_error_check(c_deinitialize)

c_get_options = lib.cepton_alg_get_options
c_get_options.restype = c_char_p

c_get_profiler_report = lib.cepton_alg_get_profiler_report
c_get_profiler_report.restype = c_char_p

# ------------------------------------------------------------------------------
# Inputs
# ------------------------------------------------------------------------------
c_is_empty = lib.cepton_alg_is_empty
c_is_empty.argtypes = []
c_is_empty.restype = c_int

c_is_full = lib.cepton_alg_is_full
c_is_full.argtypes = []
c_is_full.restype = c_int

c_add_points = lib.cepton_alg_add_points
c_add_points.argtypes = [
    POINTER(cepton_sdk.c.C_SensorInformation), c_int64, c_int,
    POINTER(cepton_sdk.c.C_SensorImagePoint)]
add_c_error_check(c_add_points)

c_add_gps_measurement = lib.cepton_alg_add_gps_measurement
c_add_gps_measurement.argtypes = [c_char_p]
add_c_error_check(c_add_gps_measurement)

c_add_imu_measurement = lib.cepton_alg_add_imu_measurement
c_add_imu_measurement.argtypes = [c_char_p]
add_c_error_check(c_add_imu_measurement)


class C_GridMask(Structure):
    _fields_ = [
        ("header_json", c_char_p),
        ("n_indices", c_int),
        ("indices", POINTER(c_int)),
    ]


check_c_size(lib, C_GridMask, "cepton_alg_grid_mask_size")

c_get_grid_mask_ids = lib.cepton_alg_get_grid_mask_ids
c_get_grid_mask_ids.argtypes = [POINTER(c_int)]
c_get_grid_mask_ids.restype = POINTER(c_char_p)

c_get_grid_mask = lib.cepton_alg_get_grid_mask
c_get_grid_mask.argtypes = [c_char_p]
c_get_grid_mask.restype = POINTER(C_GridMask)

c_set_grid_mask = lib.cepton_alg_set_grid_mask
c_set_grid_mask.argtypes = [c_char_p, c_char_p, c_int,
                            get_c_ndpointer_type(c_int)]
add_c_error_check(c_set_grid_mask)

# ------------------------------------------------------------------------------
# Outputs
# ------------------------------------------------------------------------------


class C_FrameData(Structure):
    _fields_ = [
        ("idx", c_int),
        ("timestamp", c_int64),

        ("position", 3 * c_float),
        ("orientation", 4 * c_float),
        ("velocity_translation", 3 * c_float),
        ("velocity_rotation", 3 * c_float),

        ("ground_plane_normal", 3 * c_float),
        ("ground_plane_position", 3 * c_float),
        ("ceiling_plane_normal", 3 * c_float),
        ("ceiling_plane_position", 3 * c_float),

        ("occupancy_grid_shape", 2 * c_int),
        ("occupancy_grid_lb", 2 * c_float),
        ("occupancy_grid_spacing", 2 * c_float),
    ]


check_c_size(lib, C_FrameData, "cepton_alg_frame_data_size")


class C_Point(Structure):
    _fields_ = [
        ("serial_number", c_uint64),
        ("image_point", cepton_sdk.c.C_SensorImagePoint),
        ("position", 3 * c_float),

        ("segment_idx", c_int),
        ("scanline_label", c_int),
        ("surface_idx", c_int),
        ("object_idx", c_int),

        ("flags", c_uint32),
    ]


check_c_size(lib, C_Point, "cepton_alg_point_size")


class C_Surface(Structure):
    _fields_ = [
        ("label", c_int),
        ("position", 3 * c_float),
        ("normal", 3 * c_float),
    ]


check_c_size(lib, C_Surface, "cepton_alg_surface_size")


class C_Object(Structure):
    _fields_ = [
        ("label", c_int),
        ("type", c_int),

        ("translation", 3 * c_float),
        ("velocity_translation", 3 * c_float),
        ("trajectory_size", c_int),
        ("trajectory", 10 * 3 * c_float),

        ("box_dimensions", 3 * c_float),
        ("box_translation", 3 * c_float),
        ("box_rotation", 4 * c_float),

        ("flags", c_uint8),
    ]


check_c_size(lib, C_Object, "cepton_alg_object_size")


class C_OccupancyCell(Structure):
    _fields_ = [
        ("flags", c_uint8),
    ]


check_c_size(lib, C_OccupancyCell, "cepton_alg_occupancy_cell_size")

C_FrameCallback = \
    CFUNCTYPE(None,
              POINTER(C_FrameData),
              c_int, POINTER(C_Point),
              c_int, POINTER(C_Surface),
              c_int, POINTER(C_Object),
              c_int, POINTER(C_OccupancyCell),
              c_char_p, c_void_p)

c_listen_frames = lib.cepton_alg_listen_frames
c_listen_frames.argtypes = [C_FrameCallback, c_void_p]
add_c_error_check(c_listen_frames)

c_unlisten_frames = lib.cepton_alg_unlisten_frames
add_c_error_check(c_unlisten_frames)

# ------------------------------------------------------------------------------
# Other
# ------------------------------------------------------------------------------
c_compute_shading = lib.cepton_alg_compute_shading
c_compute_shading.argtypes = [
    c_int, get_c_ndpointer_type(c_float, ndim=2),
    get_c_ndpointer_type(c_float), get_c_ndpointer_type(c_float)]
add_c_error_check(c_compute_shading)


def compute_shading(image_positions, distances):
    n = image_positions.shape[0]
    image_positions = get_c_ndarray(image_positions, dtype=c_float)
    distances = get_c_ndarray(distances, dtype=c_float)
    shading = create_c_ndarray(n, c_float)
    c_compute_shading(n, image_positions, distances, shading)
    return shading.astype(float)


__all__ = _all_builder.get()
