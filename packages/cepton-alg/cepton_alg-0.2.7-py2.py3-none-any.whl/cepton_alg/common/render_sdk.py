import enum
import queue

import cepton_sdk
import cepton_sdk.load
import cepton_util.common
import numpy

from cepton_alg.common import *

_all_builder = AllBuilder(__name__)


from cepton_alg.common.render_vispy import *  # noqa isort:skip


class AllPointsVisual(PointsVisual):
    def set_data(self, points, selected_points_flag=None, **kwargs):
        colors = numpy.ones([len(points), 4])
        sizes = numpy.full([len(points)], 2)
        if selected_points_flag is not None:
            colors[:, :] = [1, 1, 1, 0.5]
            is_selected = points.flags[:, selected_points_flag]
            colors[is_selected, :] = [1, 0, 0, 1]
            sizes[is_selected] = 2 * self.point_size
        options = {
            "face_color": colors,
            "size": sizes,
        }
        options.update(kwargs)
        super().set_data(points.positions, **options)


class InvalidPointsVisual(PointsVisual):
    def set_data(self, points, **kwargs):
        colors = numpy.ones([len(points), 4])
        colors[:, :] = [0.5, 0.5, 0.5, 0.5]

        options = {
            "face_color": colors,
        }
        options.update(kwargs)
        super().set_data(points.positions, **options)


class SDKRenderer(PointsRenderer):
    def __init__(self, **kwargs):
        self._new_points_list = queue.Queue(maxsize=10)
        self._fast = True

        super().__init__(**kwargs)

        self.load_settings()

        self.clear_cache()

    @property
    def fast(self):
        if cepton_sdk.is_live():
            return True
        return self._fast

    @fast.setter
    def fast(self, value):
        self._fast = value

    @property
    def points_selector_enabled(self):
        return self.points_selector.enabled

    @points_selector_enabled.setter
    def points_selector_enabled(self, value):
        if value:
            self.disable_interactive_widgets()
        self.points_selector.enabled = value
        self.refresh()

    @property
    def get_options(self):
        options = super().get_options()
        options.update({
            "fast": self.fast,
            "selected_points_flag": self.selected_points_flag,
            "show_all_points": self.show_all_points,
            "show_invalid_points": self.show_invalid_points,
        })
        return options

    def set_options(self, **kwargs):
        super().set_options(**kwargs)
        self.fast = kwargs.get("fast", False)
        self.points_visual.set_options(**kwargs.get("points_visual", {}))
        self.selected_points_flag = kwargs.get("selected_points_flag", None)
        self.show_all_points = kwargs.get("show_all_points", False)
        self.show_invalid_points = kwargs.get("show_invalid_points", False)

    def load_settings(self, path=None):
        self.settings_dir = cepton_util.common.InputDataDirectory(path)
        self.sensor_transform_manager = cepton_sdk.load.load_transforms(
            self.settings_dir.transforms_path)
        self.sensor_clip_manager = cepton_sdk.load.load_clips(
            self.settings_dir.clips_path)

    def resume_animation(self):
        if not cepton_sdk.is_initialized():
            warnings.warn("Not started!", RuntimeWarning)
            return
        if self.is_running:
            return
        if cepton_sdk.is_live():
            cepton_sdk.disable_control_flags(
                cepton_sdk.ControlFlag.DISABLE_NETWORK)
        super().resume_animation()

    def pause_animation(self):
        if not self.is_running:
            return
        cepton_sdk.enable_control_flags(
            cepton_sdk.ControlFlag.DISABLE_NETWORK)
        super().pause_animation()

    def clear_cache(self):
        clear_queue(self._new_points_list)
        self._points_dict = {}
        self.points = None

    def add_points(self, sensor_info, points):
        try:
            self._new_points_list.put_nowait(
                (sensor_info.serial_number, points))
        except queue.Full:
            pass

    def init_plots(self):
        super().init_plots()

        self.all_points_visual = AllPointsVisual()
        self.add_visual(self.all_points_visual.visual)

        self.points_visual = SDKPointsVisual()
        self.add_visual(self.points_visual.visual)

        self.invalid_points_visual = InvalidPointsVisual()
        self.add_visual(self.invalid_points_visual.visual)

        self.points_selector = PointsSelector()
        self.add_visual(self.points_selector.visual)
        self.add_interactive_widget(self.points_selector)

        def update():
            if len(self.points_selector.selected_indices) > 0:
                self.pause_animation()
        self.points_selector.update_callbacks.append(update)

    def process_points(self, serial_number, points):
        self.sensor_transform_manager.process_sensor_points(
            serial_number, points)
        self.sensor_clip_manager.process_sensor_points(serial_number, points)

    def update(self):
        super().update()

        if not cepton_sdk.is_initialized():
            return

        if cepton_sdk.capture_replay.is_open():
            cepton_sdk.capture_replay.resume_blocking(self.period)
        while True:
            try:
                serial_number, points = self._new_points_list.get_nowait()
            except queue.Empty:
                break
            self.process_points(serial_number, points)
            self._points_dict[serial_number] = points
        # TODO: remove old points from dict
        if len(self._points_dict) == 0:
            return False
        points = cepton_sdk.combine_points(list(self._points_dict.values()))
        self.points = points

        self.points_selector.points = self.points[self.points.valid]
        self.refresh()
        self.save_frame()
        return True

    def refresh(self):
        super().refresh()

        if self.points is None:
            return

        self.update_points_plots(self.points)

    def update_points_plots(self, points):
        # Clear
        self.all_points_visual.clear()
        self.points_visual.clear()
        self.invalid_points_visual.clear()

        # Update
        if self.show_all_points or (self.selected_points_flag is not None):
            self.update_all_points(points)
        else:
            self.update_points(points)
            if self.show_invalid_points:
                self.update_invalid_points(points)

    def update_all_points(self, points):
        self.all_points_visual.set_data(
            points, selected_points_flag=self.selected_points_flag)

    def update_points(self, points):
        is_valid = points.valid
        points = points[is_valid]
        self.points_visual.set_data(points)

    def update_invalid_points(self, points):
        is_valid = numpy.logical_not(points.valid)
        points = points[is_valid]
        self.invalid_points_visual.set_data(points)

    def on_key_press(self, event):
        if super().on_key_press(event):
            return True
        elif event.key == "S":
            self.points_selector_enabled = not self.points_selector_enabled
            return True
        return False


__all__ = _all_builder.get()
