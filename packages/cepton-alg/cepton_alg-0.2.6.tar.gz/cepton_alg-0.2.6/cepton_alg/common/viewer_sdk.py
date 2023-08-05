import collections
import glob
import json
import os.path
import queue
import shutil
import sys
import warnings

import cepton_sdk
import cepton_sdk.export
import numpy
import parse

import cepton_alg.common.capture
import cepton_alg.common.render_sdk
from cepton_alg.common import *

_all_builder = AllBuilder(__name__)

from cepton_alg.common.gui import *  # noqa isort:skip
from cepton_alg.common.render_sdk import *  # noqa isort:skip
from cepton_util.common import *  # noqa isort:skip


def create_viewer_renderer(cls=cepton_alg.common.render_sdk.SDKRenderer):
    class Renderer(cls):
        def __init__(self, **kwargs):
            kwargs["standalone"] = False
            super().__init__(**kwargs)
    return Renderer


ViewerRenderer = create_viewer_renderer()


class Viewer(MainWindow):
    def __init__(self, renderer=None):
        if renderer is None:
            renderer = ViewerRenderer()
        self.renderer = renderer
        self.pcap_capture = None
        self.camera_captures = {}

        super().__init__()

        self.video_replay_windows = {}

        self.window.setWindowTitle("Cepton Player")
        self.window.setCentralWidget(self.renderer_widget)
        self.renderer.canvas.show()

        def pause_resume():
            if self.is_running:
                self.pause()
            else:
                self.resume()
        spacebar = QShortcut(QKeySequence(Qt.Key_Space), self.window)
        spacebar.activated.connect(pause_resume)

        self.create_menu()
        self.create_toolbox()
        self.refresh()

        self.window.show()

    @property
    def renderer_widget(self):
        return self.renderer.canvas.native

    @property
    def is_running(self):
        return self.renderer.is_running

    @property
    def settings_dir(self):
        return self.renderer.settings_dir

    def get_drop_path(self, event):
        if not event.mimeData().hasUrls:
            return None
        path = event.mimeData().urls()[0]
        path = QDir.toNativeSeparators(path.toLocalFile())
        return path

    def is_valid_drop_path(self, path):
        if os.path.isdir(path):
            return True
        name = os.path.basename(path)
        if name.lower().endswith(".pcap"):
            return True
        return False

    def on_drag(self, event):
        path = self.get_drop_path(event)
        if path is None:
            event.ignore()
            return
        if self.is_valid_drop_path(path):
            event.accept()
        else:
            event.ignore()

    def on_drop(self, event):
        path = self.get_drop_path(event)
        if path is None:
            event.ignore()
            return
        if not self.is_valid_drop_path(path):
            event.ignore()
            return

        if os.path.isdir(path):
            self.open_dir(path)
        else:
            name = os.path.basename(path)
            if name.lower().endswith(".pcap"):
                self.open_replay(path)
            else:
                assert(False)
        event.accept()

    def refresh(self):
        super().refresh()
        self.renderer.refresh()

    def resume(self):
        if self.is_running:
            return
        self.renderer.resume_animation()
        self.refresh()

    def pause(self):
        if not self.is_running:
            return
        self.renderer.pause_animation()
        self.refresh()

    def load_settings(self, path):
        self.renderer.load_settings(path)
        self.refresh()

    def load_render_settings(self, path):
        with open(path, "r") as f:
            render_settings = json.load(f)
        self.renderer.set_options(**render_settings.get("renderer", {}))
        self.refresh()

    def save_render_settings(self, path):
        render_settings = {
            "renderer": self.renderer.get_options(),
        }
        with open(path, "w") as f:
            json.dump(render_settings, f, indent=4, sort_keys=True)

    def open_replay(self, path):
        self.load_settings(os.path.dirname(path))
        cepton_sdk.open_replay(path)
        cepton_sdk.capture_replay.set_enable_loop(True)
        self.renderer.clear_cache()
        self.resume()

    def close_replay(self):
        if not cepton_sdk.capture_replay.is_open():
            return
        cepton_sdk.close_replay()
        self.renderer.clear_cache()
        self.resume()

    def open_dir(self, path):
        settings_dir = InputDataDirectory(path)
        pcap_path = settings_dir.pcap_path
        if pcap_path is not None:
            self.open_replay(pcap_path)
            return
        self.load_settings(path)

    def create_menu(self):
        menu_bar = super().create_menu()

        file_menu = menu_bar.addMenu("File")
        self.create_menu_file(file_menu)

        tools_menu = menu_bar.addMenu("Tools")
        self.create_menu_tools(tools_menu)

        view_menu = menu_bar.addMenu("View")
        self.create_menu_view(view_menu)

        return menu_bar

    def create_menu_file(self, menu):
        # Load settings
        load_settings = menu.addAction("Load Settings Directory")

        def on_load_settings():
            options = {
                "caption": "Load Settings Directory",
                "options": QFileDialog.ShowDirsOnly,
            }
            path = QFileDialog.getExistingDirectory(self.window, **options)
            if not path:
                return
            self.load_settings(path)
        load_settings.triggered.connect(on_load_settings)

        # menu.addSeparator()

        # # Load render settings
        # load_render_settings = menu.addAction("Load Render Settings")

        # def on_load_render_settings():
        #     options = {
        #         "caption": "Load Render Settings",
        #         "filter": "JSON (*.json)",
        #     }
        #     path = QFileDialog.getOpenFileName(self.window, **options)[0]
        #     if not path:
        #         return
        #     self.load_render_settings(path)
        # load_render_settings.triggered.connect(on_load_render_settings)

        # # Save render settings
        # save_render_settings = menu.addAction("Save Render Settings")

        # def on_save_render_settings():
        #     if not self.settings_dir:
        #         warnings.warn("No settings directory!")
        #         return
        #     self.save_render_settings(
        #         self.settings_dir.default_render_settings_path)
        # save_render_settings.triggered.connect(on_save_render_settings)

        # # Save render settings as...
        # save_render_settings_as = menu.addAction("Save Render Settings As...")

        # def on_save_render_settings_as():
        #     options = {
        #         "caption": "Save Render Settings",
        #         "directory": fix_path("~/cepton_render_config.json"),
        #         "filter": "JSON (*.json)",
        #     }
        #     path = QFileDialog.getSaveFileName(self.window, **options)[0]
        #     if not path:
        #         return
        #     path = set_extension(path, ".json")
        #     self.save_render_settings(path)
        # save_render_settings_as.triggered.connect(on_save_render_settings_as)

        # def update():
        #     save_render_settings.setEnabled(bool(self.settings_dir))
        # self.update_callbacks.append(update)

    def export_points(self, path, **kwargs):
        points = self.renderer.points
        if points is None:
            return
        points = points[points.valid]
        cepton_sdk.export.save_points(points, path, **kwargs)

    def create_menu_tools(self, menu):
        # Export points
        export_points = menu.addAction("Export Points")

        def on_export_points():
            def get_pattern(file_type):
                ext = cepton_sdk.export.get_points_file_type_extension(
                    file_type)
                return "{} (*{})".format(file_type.name, ext)
            options = {
                "caption": "Export Points",
                "directory": os.path.join(get_default_captures_path(), "cepton_{}".format(get_timestamp_str())),
                "filter": ";;".join([get_pattern(x) for x in cepton_sdk.export.PointsFileType]),
            }
            path, file_type_str = QFileDialog.getSaveFileName(
                self.window, **options)
            if not path:
                return
            file_type_str = parse.parse("{} (*{})", file_type_str).fixed[0]
            file_type = cepton_sdk.export.PointsFileType[file_type_str]
            self.export_points(path, file_type=file_type)
        export_points.triggered.connect(on_export_points)

        menu.addSeparator()

        # Save screenshot
        save_screenshot = menu.addAction("Save Screenshot")

        def on_save_screenshot():
            options = {
                "caption": "Save Screenshot",
                "directory": os.path.join(get_default_images_path(), "cepton_{}.png".format(get_timestamp_str())),
                "filter": "PNG (*.png)",
            }
            path = QFileDialog.getSaveFileName(self.window, **options)[0]
            if not path:
                return
            path = set_extension(path, ".png")
            self.renderer.save_screenshot(path)
        save_screenshot.triggered.connect(on_save_screenshot)

        def update():
            export_points.setEnabled(self.renderer.points is not None)
        self.update_callbacks.append(update)

    def show_cameras(self):
        self.hide_cameras()
        if cepton_sdk.is_live():
            devices = glob.glob("/dev/video[0-9]")
            for device in devices:
                name = "<{}>".format(os.path.basename(device))
                self.video_replay_windows[name] = VideoReplayWindow(name)
        else:
            # HACK
            camera_paths = glob.glob(
                os.path.join(self.settings_dir.path, "camera_[0-9].mkv"))
            for camera_path in camera_paths:
                name = os.path.basename(camera_path)
                try:
                    self.video_replay_windows[name] = VideoReplayWindow(
                        camera_path)
                except:
                    continue
        self.update_cameras()

    def hide_cameras(self):
        for window in self.video_replay_windows.values():
            window.close()
        self.video_replay_windows = {}

    def update_cameras(self):
        for video_replay in self.video_replay_windows.values():
            video_replay.seek(cepton_sdk.capture_replay.get_position())

    def create_menu_view(self, menu):
        # Show toolbox
        show_toolbox = menu.addAction("Show Toolbox")

        def on_show_toolbox():
            self.show_toolbox()
        show_toolbox.triggered.connect(on_show_toolbox)

        menu.addSeparator()

        # Show cameras
        show_cameras = menu.addAction("Show Cameras")

        def on_show_cameras(*args):
            self.show_cameras()
        show_cameras.triggered.connect(on_show_cameras)

        def update():
            show_cameras.setEnabled(not cepton_sdk.is_live())
            # show_cameras.setEnabled(not self.is_capturing)
        self.update_callbacks.append(update)

        def update():
            self.update_cameras()
        self.renderer.update_callbacks.append(update)

    def create_toolbox(self):
        selector, stack = super().create_toolbox()

        def on_key_press(*args):
            pass
        selector.keyPressEvent = on_key_press

        selector.addItem("General")
        general = QWidget()
        stack.addWidget(general)
        self.create_toolbox_general(general)

        selector.addItem("Advanced")
        advanced = QWidget()
        stack.addWidget(advanced)
        self.create_toolbox_advanced(advanced)

        selector.addItem("Selection")
        selection = QWidget()
        stack.addWidget(selection)
        self.create_toolbox_selection(selection)

        selector.addItem("Monitors")
        monitors = QWidget()
        stack.addWidget(monitors)
        self.create_toolbox_monitors(monitors)

        # TODO
        # if sys.platform.startswith("linux"):
        #     selector.addItem("Capture")
        #     capture = QWidget()
        #     stack.addWidget(capture)
        #     self.create_toolbox_capture(capture)

        return selector, stack

    def create_toolbox_general(self, widget):
        layout = QFormLayout()
        widget.setLayout(layout)

        self.create_toolbox_settings(layout)
        self.create_toolbox_replay(layout)
        self.create_toolbox_render(layout)

        return layout

    def create_toolbox_settings(self, parent_layout):
        header = create_toolbox_header("Settings")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        # Pause/Resume
        pause_resume = QPushButton("")
        layout.addRow(pause_resume)

        def on_pause_resume():
            if self.is_running:
                self.pause()
            else:
                self.resume()
        pause_resume.clicked.connect(on_pause_resume)

        def update():
            pause_resume.setText("Pause" if self.is_running else "Resume")
        self.update_callbacks.append(update)

    def create_toolbox_replay(self, parent_layout):
        header = create_toolbox_header("Replay")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        # Close
        close = QPushButton("Close")
        layout.addRow(close)

        def on_close(*args):
            self.close_replay()
        close.clicked.connect(on_close)

        # TODO
        # Filename
        # filename = QLabel()
        # layout.addRow("Filename", filename)

        # Position
        position = QLabel()
        layout.addRow("Position", position)

        # Seek
        seek = QJumpSlider(Qt.Horizontal)
        layout.addRow(seek)
        seek.setMinimum(0)
        seek.setTickPosition(QSlider.NoTicks)

        def on_seek_released():
            t = float(seek.value())
            cepton_sdk.capture_replay.seek(t)
            self.renderer.clear_cache()
            self.resume()
        seek.sliderReleased.connect(on_seek_released)

        # Speed
        # speed = QDoubleSpinBox()
        # layout.addRow("Speed", speed)
        # speed.setMinimum(0)
        # speed.setMaximum(1)
        # speed.setSingleStep(0.1)

        # def on_speed():
        #     if speed.value() <= 0:
        #         return
        #     cepton_sdk.capture_replay.set_speed(speed.value())
        #     self.refresh()
        # speed.valueChanged.connect(on_speed)

        # Loop
        loop = QCheckBox("Loop")
        layout.addRow(loop)

        def on_loop():
            cepton_sdk.capture_replay.set_enable_loop(loop.isChecked())
            self.refresh()
        loop.stateChanged.connect(on_loop)

        def refresh():
            # speed.setValue(cepton_sdk.capture_replay.get_speed())
            loop.setChecked(cepton_sdk.capture_replay.get_enable_loop())
        self.refresh_callbacks.append(refresh)

        def update():
            is_visible = cepton_sdk.capture_replay.is_open()
            widget.setVisible(is_visible)
            if not is_visible:
                return

            # path = cepton_sdk.capture_replay.get_filename()
            # name = os.path.basename(path)
            # if name == "lidar.pcap":
            #     name = os.path.basename(os.path.dirname(path))
            # else:
            #     name = remove_extension(name)
            # filename.setText(name)

            seek.setMaximum(int(cepton_sdk.capture_replay.get_length()))
            if seek.isSliderDown():
                t = seek.value()
            else:
                t = cepton_sdk.capture_replay.get_position()
                # seek.setValue(int(t))
            position.setText("{} / {}".format(
                format_seconds(t),
                format_seconds(cepton_sdk.capture_replay.get_length())))
        self.update_callbacks.append(update)

        return layout

    def create_toolbox_render(self, parent_layout):
        header = create_toolbox_header("Render")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        # Color mode
        color_mode = QComboBox()
        layout.addRow("Color Mode", color_mode)
        color_mode.addItems([enum_to_label(x) for x in SDKPointColorMode])

        def on_color_mode(i):
            self.renderer.points_visual.color_mode = SDKPointColorMode(i)
            self.refresh()
        color_mode.currentIndexChanged.connect(on_color_mode)

        # Color map
        color_map = QComboBox()
        layout.addRow("Color Map", color_map)
        color_map.addItems([enum_to_label(x) for x in ColorMap])

        def on_color_map(i):
            self.renderer.points_visual.color_map = ColorMap(i)
            self.refresh()
        color_map.currentIndexChanged.connect(on_color_map)

        # Color min
        color_min = QDoubleSpinBox()
        layout.addRow("Color Min", color_min)
        color_min.setSingleStep(1)

        def on_color_min():
            self.renderer.points_visual.color_min = color_min.value()
            self.refresh()
        color_min.valueChanged.connect(on_color_min)

        # Color max
        color_max = QDoubleSpinBox()
        layout.addRow("Color Max", color_max)
        color_max.setSingleStep(1)

        def on_color_max():
            self.renderer.points_visual.color_max = color_max.value()
            self.refresh()
        color_max.valueChanged.connect(on_color_max)

        # Point size
        point_size = QDoubleSpinBox()
        layout.addRow("Point Size", point_size)
        point_size.setSingleStep(1)
        point_size.setDecimals(2)
        point_size.setMinimum(1)

        def on_point_size():
            self.renderer.points_visual.point_size = point_size.value()
            self.refresh()
        point_size.valueChanged.connect(on_point_size)

        # Show grid
        show_grid = QCheckBox("Show Grid")
        layout.addRow(show_grid)

        def on_show_grid():
            self.renderer.show_grid = show_grid.isChecked()
            self.refresh()
        show_grid.stateChanged.connect(on_show_grid)

        def refresh():
            color_mode.setCurrentIndex(
                int(self.renderer.points_visual.color_mode))
            color_map.setCurrentIndex(
                int(self.renderer.points_visual.color_map))
            color_min.setValue(self.renderer.points_visual.color_min)
            color_max.setValue(self.renderer.points_visual.color_max)
            point_size.setValue(self.renderer.points_visual.point_size)
            show_grid.setChecked(self.renderer.show_grid)
        self.refresh_callbacks.append(refresh)

        return layout

    def create_toolbox_advanced(self, widget):
        layout = QFormLayout()
        widget.setLayout(layout)

        self.create_toolbox_debug(layout)

        return layout

    def create_toolbox_debug(self, parent_layout):
        header = create_toolbox_header("Debug")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        # Ruler
        measurement = QComboBox()
        layout.addRow("Measurement", measurement)
        measurement.addItems(["", "Angle Ruler", "Distance Ruler"])

        def on_measurement(i):
            self.renderer.angle_ruler_enabled = False
            self.renderer.distance_ruler_enabled = False
            if i == 0:
                pass
            elif i == 1:
                self.renderer.angle_ruler_enabled = True
            elif i == 2:
                self.renderer.distance_ruler_enabled = True
            else:
                assert(False)
        measurement.currentIndexChanged.connect(on_measurement)

        # Show all
        show_all_points = QCheckBox("Show All Points")
        layout.addRow(show_all_points)

        def on_show_all_points():
            self.renderer.show_all_points = show_all_points.isChecked()
            self.refresh()
        show_all_points.stateChanged.connect(on_show_all_points)

        # Show invalid
        show_invalid_points = QCheckBox("Show Invalid Points")
        layout.addRow(show_invalid_points)

        def on_show_invalid_points():
            self.renderer.show_invalid_points = show_invalid_points.isChecked()
            self.refresh()
        show_invalid_points.stateChanged.connect(on_show_invalid_points)

        # Selected Points
        selected_points_flag = QComboBox()
        layout.addRow("Selected Points", selected_points_flag)
        PointFlag = cepton_sdk.PointFlag
        all_point_flags = [enum_to_label(x) for x in PointFlag]
        selected_points_flag.addItems(["None"] + all_point_flags)

        def on_selected_points_flag(i):
            if i == 0:
                self.renderer.selected_points_flag = None
            else:
                self.renderer.selected_points_flag = PointFlag(i - 1)
            self.refresh()
        selected_points_flag.currentIndexChanged.connect(
            on_selected_points_flag)

        def refresh():
            if self.renderer.angle_ruler_enabled:
                measurement.setCurrentIndex(1)
            elif self.renderer.distance_ruler_enabled:
                measurement.setCurrentIndex(2)
            else:
                measurement.setCurrentIndex(0)
            show_all_points.setChecked(self.renderer.show_all_points)
            show_invalid_points.setChecked(self.renderer.show_invalid_points)
            if self.renderer.selected_points_flag is None:
                selected_points_flag.setCurrentIndex(0)
            else:
                selected_points_flag.setCurrentIndex(
                    self.renderer.selected_points_flag + 1)
        self.refresh_callbacks.append(refresh)

        return layout

    def create_toolbox_selection(self, widget):
        layout = QVBoxLayout()
        widget.setLayout(layout)

        form_widget = QWidget()
        layout.addWidget(form_widget)
        form_layout = QFormLayout()
        form_widget.setLayout(form_layout)

        # Mode
        mode = QComboBox()
        form_layout.addRow("Selection Mode", mode)
        mode.addItems(["", "Single"])

        def on_mode(i):
            if i == 0:
                self.renderer.points_selector_enabled = False
            elif i == 1:
                self.renderer.points_selector_enabled = True
            else:
                assert(False)
            self.refresh()
        mode.currentIndexChanged.connect(on_mode)

        tree = JSONView()
        layout.addWidget(tree.widget)

        def numpy_to_str(a, pattern=""):
            pattern = "{:" + pattern + "}"
            return "[" + ", ".join([pattern.format(x) for x in a]) + "]"

        def position_to_str(a):
            return numpy_to_str(a, "3.2f")

        def update():
            if self.renderer.points_selector_enabled:
                mode.setCurrentIndex(1)
            else:
                mode.setCurrentIndex(0)
        self.update_callbacks.append(update)

        def update():
            points = self.renderer.points_selector.selected_points
            if points is None:
                return
            if len(points) == 0:
                return

            points_data = [collections.OrderedDict([
                ["Timestamp", "{:.3f}".format(points.timestamps[i])],
                ["Distance", "{:3.2f}".format(points.distances[i])],
                ["Position", position_to_str(points.positions[i, :])],
                ["Intensity", "{:.2f}".format(points.intensities[i])],
                ["Strongest", str(bool(points.return_farthest[i]))],
                ["Farthest", str(bool(points.return_strongest))],
                ["Valid", str(bool(points.valid[i]))],
                ["Saturated", str(bool(points.saturated[i]))],
            ]) for i in range(len(points))]
            data = collections.OrderedDict([
                ["Count", len(points)],
                ["Mean Position", position_to_str(
                    numpy.mean(points.positions, axis=0))],
                ["Points", points_data],
            ])
            tree.set_data(data)
            tree.widget.setSortingEnabled(False)
            tree.expand(1)
        self.renderer.points_selector.update_callbacks.append(update)

        return layout

    def create_toolbox_monitors(self, widget):
        layout = QFormLayout()
        widget.setLayout(layout)

        sdk_version = QLabel(cepton_sdk.__version__)
        layout.addRow("SDK Version", sdk_version)

        n_points = QLabel()
        layout.addRow("# Points", n_points)

        def update():
            points = self.renderer.points
            if not points:
                return

            n_points.setText("{:,}".format(len(points)))
        self.update_callbacks.append(update)

        return layout

    @property
    def is_capturing(self):
        return self.pcap_capture is not None

    def start_capture(self, path, camera_devices):
        self.stop_capture()

        output_dir = OutputDataDirectory(path)

        self.pcap_capture = cepton_alg.common.capture.PCAPCapture(
            output_dir.pcap_path)

        for device in camera_devices:
            i_camera = int(parse.parse("/dev/video{}", device).fixed[0])
            camera_path = "{}/camera_{}.mkv".format(path, i_camera)
            self.camera_captures[device] = cepton_alg.common.capture.CameraCapture(
                device, camera_path)

    def stop_capture(self):
        if not self.is_capturing:
            return

        if self.pcap_capture is not None:
            self.pcap_capture.close()
            self.pcap_capture = None
        for camera_capture in self.camera_captures.values():
            camera_capture.close()
        camera_captures = {}

    def create_toolbox_capture(self, widget):
        layout = QFormLayout()
        widget.setLayout(layout)

        devices = glob.glob("/dev/video[0-9]")
        cameras = {}
        for device in devices:
            camera = QPushButton(device)
            camera.setCheckable(True)
            cameras[device] = camera

        label = QLabel("Requires dumpcap and ffmpeg.")
        layout.addRow(label)
        label.setWordWrap(True)

        # Start/Stop
        stop_start = QPushButton()
        layout.addRow(stop_start)

        def on_stop_start():
            if self.is_capturing:
                self.stop_capture()
            else:
                options = {
                    "caption": "Save Capture",
                    "directory": os.path.join(get_default_captures_path(), "cepton_{}".format(get_timestamp_str())),
                }
                dialog = QFileDialog(self.window, **options)
                dialog.setFileMode(QFileDialog.Directory)
                dialog.setAcceptMode(QFileDialog.AcceptSave)
                dialog.setOption(QFileDialog.ShowDirsOnly)
                if not dialog.exec_():
                    return
                path = dialog.selectedFiles()[0]

                camera_devices = [device for device,
                                  camera in cameras.items() if camera.isChecked()]
                self.start_capture(path, camera_devices=camera_devices)
        stop_start.clicked.connect(on_stop_start)

        # TODO: Refresh

        # Cameras
        header = create_toolbox_header("Cameras")
        layout.addRow(header)

        for device in sorted(cameras):
            camera = cameras[device]
            layout.addRow(camera)

        # TODO: GPS

        def update():
            stop_start.setText("Stop" if self.is_capturing else "Start")
            for camera in cameras.values():
                camera.setEnabled(not self.is_capturing)
        self.update_callbacks.append(update)

        return layout


__all__ = _all_builder.get()
