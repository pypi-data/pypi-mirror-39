import ctypes
import enum
import json

import numpy
import pynmea2

import cepton_alg.c
import cepton_alg.frame
import cepton_sdk
import cepton_sdk.c
import cepton_sdk.core
import cepton_util
from cepton_alg.common import *

_all_builder = AllBuilder(__name__)


class Verbosity(enum.IntEnum):
    QUIET = -1
    INFO = 0
    DEBUG = 1


def deserialize_alg_settings(options):
    options["model"] = cepton_util.common.parse_enum(
        options.get("model"), cepton_sdk.SensorModel)
    options["verbosity"] = cepton_util.common.parse_enum(
        options.get("verbosity"), Verbosity)
    return cepton_util.common.process_options(options)


def get_options():
    options = json.loads(cepton_alg.c.c_get_options().decode("utf-8"))
    return deserialize_alg_settings(options)


def get_profiler_report():
    return json.loads(cepton_alg.c.c_get_profiler_report().decode("utf-8"))


def is_empty():
    return bool(cepton_alg.c.c_is_empty())


def is_full():
    return bool(cepton_alg.c.c_is_full())


def initialize_sdk(**kwargs):
    options = {
        "control_flags": cepton_sdk.ControlFlag.ENABLE_MULTIPLE_RETURNS,
        "frame_length": 0.01,
        "frame_mode": cepton_sdk.core.FrameMode.TIMED,
    }
    options.update(kwargs)
    cepton_sdk.initialize(**options)
    cepton_sdk.c.c_unlisten_image_frames()


def _on_sdk_frame(sensor_handle, n_points, c_image_points, c_user_data):
    c_sensor_info = cepton_sdk.c.C_SensorInformation()
    cepton_sdk.c.c_get_sensor_information(sensor_handle, c_sensor_info)
    timestamp = int(1e6 * cepton_sdk.get_time())
    cepton_alg.c.c_add_points(
        c_sensor_info, timestamp, n_points, c_image_points)


class _Manager(object):
    def initialize(self, sensor_serial_numbers=None, sensor_clips_path=None,
                   sensor_transforms_path=None, **kwargs):
        options = {}
        if sensor_serial_numbers is None:
            options["cost_scale"] = cepton_sdk.get_n_sensors()
        else:
            options["cost_scale"] = len(sensor_serial_numbers)
            options["serial_numbers"] = numpy.array(
                sensor_serial_numbers).tolist()
        if sensor_clips_path is not None:
            options["clips_path"] = sensor_clips_path
        if sensor_transforms_path is not None:
            options["transforms_path"] = sensor_transforms_path
        options.update(kwargs)
        cepton_alg.c.c_initialize(
            cepton_alg.c.ALG_VERSION, json.dumps(options).encode("UTF-8"))

        # Listen
        self._c_on_sdk_frame = \
            cepton_sdk.c.C_SensorImageDataCallback(_on_sdk_frame)
        cepton_sdk.c.c_listen_image_frames(self._c_on_sdk_frame, None)

    def deinitialize(self):
        try:
            cepton_sdk.c.c_unlisten_image_frames()
        except cepton_sdk.C_Error:
            pass
        try:
            cepton_alg.c.c_deinitialize()
        except cepton_sdk.C_Error:
            pass


_manager = _Manager()


def is_initialized():
    return bool(cepton_alg.c.c_is_initialized())


class GridMask:
    def __init__(self):
        self.enabled = False
        self.relative = False
        self.inverted = False
        self.grid = None
        self.indices = numpy.array([], dtype=int)


class GridMaskId(enum.Enum):
    ABSOLUTE_2D = 0
    ABSOLUTE_3D = 1
    RELATIVE_2D = 2
    RELATIVE_3D = 3


def is_grid_mask_relative(mask_id):
    return mask_id in [GridMaskId.RELATIVE_2D, GridMaskId.RELATIVE_3D]


def get_grid_mask_ids():
    c_n_masks = ctypes.c_int()
    c_mask_ids = cepton_alg.c.c_get_grid_mask_ids(ctypes.byref(c_n_masks))
    n_masks = c_n_masks.value
    return [GridMaskId[c_mask_ids[i].decode("utf-8")]
            for i in range(n_masks)]


def has_grid_mask(mask_id):
    return mask_id in get_grid_mask_ids()


def get_grid_mask(mask_id):
    if not has_grid_mask(mask_id):
        return None
    c_mask_id = mask_id.name.encode("utf-8")
    c_mask = cepton_alg.c.c_get_grid_mask(c_mask_id).contents
    header = json.loads(c_mask.header_json.decode("utf-8"))
    mask = GridMask()
    mask.enabled = header["enabled"]
    mask.relative = header["relative"]
    mask.inverted = header["inverted"]
    mask.grid = cepton_alg.common.geometry.Grid.deserialize(header["grid"])
    if c_mask.n_indices == 0:
        mask.indices = numpy.array([], dtype=int)
    else:
        mask.indices = cepton_alg.c.convert_c_array_to_ndarray(
            c_mask.n_indices, c_mask.indices).astype(int)
    return mask


def get_grid_masks():
    return {mask_id: get_grid_mask(mask_id) for mask_id in mask_ids}


def set_grid_mask(mask_id, mask):
    c_mask_id = mask_id.name.encode("utf-8")
    c_header = json.dumps({
        "enabled": mask.enabled,
        "relative": mask.relative,
        "inverted": mask.inverted,
        "grid": mask.grid.serialize(),
    }).encode("utf-8")
    c_indices = cepton_alg.c.get_c_ndarray(mask.indices, dtype=ctypes.c_int)
    cepton_alg.c.c_set_grid_mask(
        c_mask_id, c_header, c_indices.size, c_indices)


def disable_grid_mask(mask_id):
    mask = get_grid_mask(mask_id)
    mask.enabled = False
    set_grid_mask(mask)


class _FramesCallback(cepton_sdk.core._Callback):
    def __del__(self):
        self.deinitialize()

    def initialize(self):
        self.deinitialize()

        def on_frame(*args):
            frame = cepton_alg.frame.Frame.from_c(*args[:-1])
            self._on_callback(frame)
        self._c_on_frame = cepton_alg.c.C_FrameCallback(on_frame)
        cepton_alg.c.c_listen_frames(self._c_on_frame, None)

    def deinitialize(self):
        try:
            cepton_alg.c.c_unlisten_frames()
        except:
            pass
        self.clear()


_manager.frames_callback = _FramesCallback()

__all__ = _all_builder.get()
