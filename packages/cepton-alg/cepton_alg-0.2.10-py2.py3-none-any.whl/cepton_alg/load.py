import binascii
import ctypes
import glob
import json
import os
import os.path
import pkgutil
import pprint

import numpy
import pynmea2
import serial

import cepton_alg.api
import cepton_alg.core
import cepton_sdk.common.c
import cepton_sdk.load
import cepton_util.common
from cepton_alg.common import *

_all_builder = AllBuilder(__name__)

from cepton_util.common import InputDataDirectory, OutputDataDirectory  # noqa isort:skip


def clean_json(s):
    """Very basic json cleaning. Each key/item must be on a separate line.

    - Removes lines starting with `//`.
    - Removes trailing commas in objects and lists.
    """
    # Remove comments/whitespace
    lines = s.splitlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if not line.startswith("//")]
    s = "".join(lines)

    # Remove trailing commas
    s = s.replace(",]", "]")
    s = s.replace(",}", "}")

    return s


def load_alg_settings(path=None):
    if path is None:
        return {}
    with open(path, "r") as f:
        options = json.loads(clean_json(f.read()))
        return cepton_alg.core.deserialize_alg_settings(options)


def create_gps_measurement(line):
    KNOT_TO_M_PER_S = 0.51444444444

    nmea = pynmea2.parse(line)
    if nmea.sentence_type not in ["RMA", "RMC"]:
        return
    timestamp = nmea.datetime.timestamp()
    speed = nmea.spd_over_grnd
    if speed is None:
        return None
    return {
        "timestamp": int(1e6 * timestamp),
        "speed_translation": speed * KNOT_TO_M_PER_S,
    }


def load_gps(path=None):
    if path is None:
        return
    with open(path, "r") as f:
        for line in f:
            measurement = create_gps_measurement(line)
            if measurement is None:
                continue
            cepton_alg.c.c_add_gps_measurement(
                json.dumps(measurement).encode("utf-8"))


def find_gps():
    devices = {}
    for device in serial.tools.list_ports.comports():
        port = device.device
        try:
            devices[port] = serial.Serial(port, timeout=1)
        except:
            continue
    for port, device in devices.items():
        try:
            device.readline()
            line = device.readline().decode("utf-8")
            pynmea2.parse(line)
        except:
            continue
        return port
    return None


def run_gps(device):
    def run(shutdown_event=None):
        device.readline()
        while True:
            if shutdown_event is not None:
                if shutdown_event.is_set():
                    break

            line = device.readline().decode("utf-8")
            measurement = create_gps_measurement(line)
            if measurement is None:
                continue
            cepton_alg.c.c_add_gps_measurement(
                json.dumps(measurement).encode("utf-8"))
    return cepton_util.common.run_background(run)


def load_imu(path=None):
    if path is None:
        return

    # Check format
    with open(imu_path, "r") as f:
        header = f.readline().strip()
        assert(header ==
               "# timestamp_usec,velocity_rotation_x,velocity_rotation_y,velocity_rotation_z")

    # Load
    dtype = [
        ("timestamp_usec", int),
        ("velocity_rotation_x", float),
        ("velocity_rotation_y", float),
        ("velocity_rotation_z", float),
    ]
    options = {
        "dtype": dtype,
        "delimiter": ",",
    }
    data = numpy.loadtxt(imu_path, **options)
    velocity_rotation = numpy.zeros([len(data), 3])
    velocity_rotation[:, 0] = data["velocity_rotation_x"]
    velocity_rotation[:, 1] = data["velocity_rotation_y"]
    velocity_rotation[:, 2] = data["velocity_rotation_z"]

    # HACK
    velocity_rotation = numpy.radians(velocity_rotation)

    # velocity_rotation -= velocity_rotation_offset

    # Create measurements
    for i in range(len(data)):
        measurement = {
            "timestamp": int(data["timestamp_usec"][i]),
            "velocity_rotation": velocity_rotation[i, :].tolist(),
        }
        cepton_alg.c.c_add_imu_measurement(
            json.dumps(measurement).encode("utf-8"))


def load_grid_mask(path=None):
    if path is None:
        return

    with open(path, "r") as f:
        data = json.load(f)
    for mask_id, mask_json in data.items():
        mask_id = cepton_alg.core.GridMaskId[mask_id]
        mask = cepton_alg.core.GridMask()
        mask.enabled = mask_json["enabled"]
        mask.relative = mask_json["relative"]
        mask.inverted = mask_json["inverted"]
        mask.grid = cepton_alg.common.geometry.Grid.deserialize(
            mask_json["grid"])
        mask.indices = numpy.frombuffer(
            binascii.unhexlify(mask_json["indices"]), dtype=numpy.int32).astype(int)
        cepton_alg.core.set_grid_mask(mask_id, mask)


def save_grid_mask(mask_id, mask, path):
    mask_json = {
        "enabled": mask.enabled,
        "relative": mask.relative,
        "inverted": mask.inverted,
        "grid": mask.grid.serialize(),
        "indices": binascii.hexlify(mask.indices.astype(
            numpy.int32).tobytes()).decode("utf-8"),
    }
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data[mask_id.name] = mask_json
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def parse_dir(path):
    capture = InputDataDirectory(path)
    alg_options = {
        "transforms_path": capture.transforms_path,
        "clips_path": capture.clips_path,
    }
    return cepton_util.common.process_options(alg_options)


def load_dir(path):
    capture = InputDataDirectory(path)
    load_gps(capture.gps_path)
    # load_imu(capture.imu_path)
    load_grid_mask(capture.grid_mask_path)


def start(alg_options=None, settings_dir=None):
    options = {}
    if settings_dir is not None:
        options.update(parse_dir(settings_dir))
    if alg_options is not None:
        options.update(alg_options)
    cepton_alg.api.initialize(**options)

    if settings_dir is not None:
        load_dir(settings_dir)

    if "gps" in options:
        gps_device = serial.Serial(**options["gps"])
        run_gps(gps_device)


stop = cepton_alg.api.deinitialize


def path_to_label(path):
    return cepton_util.common.remove_extension(os.path.basename(path))


def get_presets_path(category):
    cepton_alg_path = cepton_util.common.get_package_path("cepton_alg")
    return os.path.join(cepton_alg_path, "settings", category)


def get_preset(category, name):
    return os.path.join(get_presets_path(category), name + ".json")


def get_presets(category):
    presets_path = get_presets_path(category)
    return {path_to_label(x): os.path.join(presets_path, x)
            for x in os.listdir(presets_path) if x.endswith(".json")}


class Loader(cepton_util.common.ArgumentParserMixin):
    def __init__(self, alg_options={}, sdk_options={}, settings_dir=None):
        cepton_alg.core.initialize_sdk(**sdk_options)
        start(alg_options=alg_options, settings_dir=settings_dir)

    @classmethod
    def add_arguments(cls, parser):
        group = parser.add_argument_group("Loader")
        all_alg_presets = sorted(get_presets("alg").keys())
        group.add_argument("--alg_preset", choices=all_alg_presets)
        group.add_argument("--alg_settings_path")
        group.add_argument("--capture_path")
        group.add_argument("--capture_seek")
        group.add_argument("--debug")
        group.add_argument("--settings_dir",
                           help="Load settings from directory.")
        group.add_argument("--sensors")
        return group

    @classmethod
    def parse_arguments(cls, args):
        capture_path = cepton_util.common.fix_path(args.capture_path)
        settings_dir = cepton_util.common.fix_path(args.settings_dir)
        if (settings_dir is None) and (capture_path is not None):
            settings_dir = os.path.dirname(capture_path)

        sdk_options = {
            "capture_path": capture_path,
            "capture_seek": cepton_util.common.parse_time_hms(args.capture_seek),
        }
        sdk_options = cepton_util.common.process_options(sdk_options)

        alg_options = {
            "sensor_serial_numbers": cepton_util.common.parse_list(
                args.sensors, dtype=int),
        }
        if args.alg_settings_path is not None:
            alg_settings_path = cepton_util.common.fix_path(
                args.alg_settings_path)
        elif args.alg_preset is not None:
            alg_settings_path = get_preset("alg", args.alg_preset)
        else:
            alg_settings_path = get_preset("alg", "default")
        alg_options.update(load_alg_settings(alg_settings_path))
        if args.debug:
            alg_options["verbosity"] = cepton_alg.core.Verbosity.DEBUG
        alg_options = cepton_util.common.process_options(alg_options)

        options = {
            "alg_options": alg_options,
            "sdk_options": sdk_options,
            "settings_dir": settings_dir,
        }
        return cepton_util.common.process_options(options)


__all__ = _all_builder.get()
