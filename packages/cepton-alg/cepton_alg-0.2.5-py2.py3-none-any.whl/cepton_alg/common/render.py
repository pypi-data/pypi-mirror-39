import enum

import imageio
import numpy
import scipy.interpolate
import seaborn

import cepton_alg.common.time
import cepton_util.common
from cepton_alg.common import *

_all_builder = AllBuilder(__name__)


def create_color_lut(palette):
    palette = numpy.array(palette)
    color_lut = numpy.ones([palette.shape[0], 4])
    color_lut[:, :palette.shape[1]] = palette
    return color_lut


def get_categorical_color_lut():
    return create_color_lut(seaborn.color_palette("Set1", n_colors=8))


def get_circular_color_lut():
    return create_color_lut(seaborn.hls_palette(s=1, n_colors=16))


def get_constant_color_lut():
    return numpy.ones([2, 4])


def get_diverging_color_lut():
    return create_color_lut(
        seaborn.diverging_palette(255, 140, s=100, l=30, n=8))


def get_sequential_color_lut():
    return create_color_lut(seaborn.color_palette("YlGnBu_r", n_colors=8))


@enum.unique
class ColorMap(enum.IntEnum):
    CATEGORICAL = 0
    CIRCULAR = 1
    CONSTANT = 2
    DIVERGING = 3
    SEQUENTIAL = 4


def get_color_lut(color_map):
    return {
        ColorMap.CATEGORICAL: get_categorical_color_lut,
        ColorMap.CIRCULAR: get_circular_color_lut,
        ColorMap.CONSTANT: get_constant_color_lut,
        ColorMap.DIVERGING: get_diverging_color_lut,
        ColorMap.SEQUENTIAL: get_sequential_color_lut,
    }[color_map]()


def get_categorical_colors(color_values, color_lut):
    n_colors = color_lut.shape[0]
    color_values = color_values.astype(int)
    color_values = numpy.mod(color_values, n_colors)
    return color_lut[color_values, :]


def get_colors(color_values, color_lut):
    n = color_lut.shape[0]

    x = numpy.linspace(0, 1, n)
    options = {
        "assume_sorted": True,
        "axis": 0,
        "kind": "linear",
    }
    func = scipy.interpolate.interp1d(x, color_lut, **options)
    colors = func(color_values)
    return colors


class VideoReplay:
    def __init__(self, path, frame_rate=20):
        self._rate = cepton_alg.common.time.Rate(1 / frame_rate)
        options = {
            "fps": frame_rate,
        }
        self._reader = imageio.get_reader(path, "ffmpeg", **options)

    def __del__(self):
        self.close()

    def close(self):
        try:
            self._reader.close()
        except:
            pass

    @property
    def t(self):
        return self._rate.t

    def get_frame(self, t):
        self._rate.t = t
        self._reader.set_image_index(self._rate.i)
        return self._reader.get_next_data()


class VideoExporter:
    def __init__(self, path, frame_rate=30, t_start=0):
        self.frame_rate = frame_rate
        self.path = path

        self._dimensions = None
        self._previous_frame = None
        self._rate = cepton_alg.common.time.Rate(1 / self.frame_rate)
        self._writer = None

    def __del__(self):
        self.close()

    @property
    def t(self):
        return self._rate.t

    def close(self):
        try:
            self._writer.release()
        except:
            pass

    def save_frame(self, frame, t=None):
        # Check frame dimensions
        frame_dimensions = numpy.array(frame.shape[:2])
        if self._dimensions is None:
            dimensions = numpy.floor(frame_dimensions / 16) * 16
            self._dimensions = dimensions.astype(int)
        if numpy.any(frame_dimensions < self._dimensions):
            raise RuntimeError("window was resized")
        frame = frame[:self._dimensions[0], :self._dimensions[1], ...]

        if t is None:
            self._save_frame_impl(frame)
        else:
            # Append duplicate frames or drop frames
            while True:
                t_ideal = self._rate.get_t()
                t_offset = t_ideal - t
                if t_offset < 0:
                    if self._previous_frame is None:
                        break
                    # Duplicate previous frame
                    self._save_frame_impl(self._previous_frame)
                elif t_offset > self._rate.period:
                    # Drop frame
                    break
                else:
                    # Use frame
                    self._save_frame_impl(frame)
                    break

        self._previous_frame = frame

    def _save_frame_impl(self, frame):
        # Create writer
        if self._writer is None:
            options = {
                "format": "ffmpeg",
                "fps": self.frame_rate,
                "quality": 10,
            }
            self._writer = \
                imageio.get_writer(self.path, **options)
        self._writer.append_data(frame)

        self._rate.next()


class Exporter(cepton_util.common.ArgumentParserMixin):
    def __init__(self, frame_rate=30, image_dir=None, video_path=None):
        self.frame_rate = frame_rate
        self.image_dir = image_dir
        self.video_path = video_path

        if self.image_dir is not None:
            cepton_util.common.create_directory(self.image_dir)

        self.video = None
        if self.video_path is not None:
            options = {
                "frame_rate": self.frame_rate,
            }
            self.video = VideoExporter(self.video_path, **options)

        self._rate = cepton_alg.common.time.Rate(1 / self.frame_rate)

    @classmethod
    def add_arguments(cls, parser):
        group = parser.add_argument_group("Exporter")
        group.add_argument("--image_dir")
        group.add_argument("--video_path")
        return group

    @classmethod
    def parse_arguments(cls, args):
        options = {}
        options.update({
            "image_dir": cepton_util.common.fix_path(args.image_dir),
            "video_path": cepton_util.common.set_extension(
                cepton_util.common.fix_path(args.video_path), ".mp4"),
        })
        return cepton_util.common.process_options(options)

    def close():
        try:
            self.video.close()
        except:
            pass

    def save_frame(self, frame, t=None):
        if self.video is not None:
            self.video.save_frame(frame, t=t)

        if self.image_dir is not None:
            image_path = os.path.join(
                self.image_dir, "{}.png".format(self._rate.i))
            imageio.imwrite(image_path, frame)

        self._rate.next()


def clear_queue(queue):
    n = queue.qsize()
    for i in range(n):
        try:
            queue.get_nowait()
        except queue.Empty:
            break


__all__ = _all_builder.get()
