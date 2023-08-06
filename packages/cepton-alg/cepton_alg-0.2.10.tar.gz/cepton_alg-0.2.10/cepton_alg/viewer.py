import collections
import glob
import json
import os.path
import shutil
import warnings

import numpy
import parse
import serial

import cepton_alg
import cepton_alg.load
import cepton_alg.render
import cepton_sdk
import cepton_sdk.export
import cepton_util.capture
from cepton_alg.common import *

_all_builder = AllBuilder(__name__)

from cepton_alg.common.gui import *  # noqa isort:skip
from cepton_alg.render import *  # noqa isort:skip


def create_viewer_renderer(cls=cepton_alg.render.FrameRenderer):
    class Renderer(cls):
        def __init__(self, **kwargs):
            kwargs["standalone"] = False
            super().__init__(**kwargs)

        # def on_mouse_press(self, event):
        #     # HACK
        #     if self.frame is not None:
        #         line = get_mouse_event_line(event, self.view)
        #         points = self.frame.points
        #         is_valid = points.is_filtered
        #         positions = self.frame.points.positions[is_valid, :]
        #         idx = get_selected_point(line, positions)
        #         print(idx)

        #     return super().on_mouse_press(event)

    return Renderer


ViewerRenderer = create_viewer_renderer()


class Viewer(MainWindow):
    def __init__(self, renderer=None):
        if renderer is None:
            renderer = ViewerRenderer()
        self.renderer = renderer

        super().__init__()

        self.alg_settings_path = None
        self.capture_writer = None
        self.is_started = False
        self.settings_dir = cepton_alg.load.InputDataDirectory()
        self.video_replay_windows = {}

        self.window.setWindowTitle("Cepton Alg Viewer")
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
        self.renderer.refresh_callbacks.append(self.refresh)

        self.window.show()

    def __del__(self):
        self.stop_capture()
        del self.renderer

    def on_close(self, *args):
        self.stop_capture()
        super().on_close(*args)

    def update(self):
        super().update()

        if self.renderer.exporter is None:
            self.renderer_widget.setFixedSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)
        else:
            self.renderer_widget.setFixedSize(self.renderer_widget.size())

    @property
    def renderer_widget(self):
        return self.renderer.canvas.native

    @property
    def is_running(self):
        return self.renderer.is_running

    def resume(self):
        if self.is_running:
            return
        if not cepton_alg.is_initialized():
            if not self.start():
                return False
        self.renderer.resume_animation()
        self.refresh()

    def pause(self):
        if not self.is_running:
            return
        self.renderer.pause_animation()
        self.refresh()

    def start(self):
        self.stop()

        if self.alg_settings_path is None:
            warnings.warn("No alg settings loaded!", RuntimeWarning)
            return False

        # Wait for sensor
        for i in range(30):
            cepton_sdk.wait(0.1)
            if cepton_sdk.get_n_sensors() > 0:
                break
        if cepton_sdk.get_n_sensors() == 0:
            warnings.warn("No sensors detected!", RuntimeWarning)
            return False

        alg_options = {
            "verbosity": cepton_alg.core.Verbosity.INFO,
        }
        alg_options.update(
            cepton_alg.load.load_alg_settings(self.alg_settings_path))
        alg_options.update({
            "enable_thread": True,
        })
        cepton_alg.load.start(alg_options=alg_options,
                              settings_dir=self.settings_dir.path)

        alg_options = cepton_alg.get_options()
        # if self.renderer.fast:
        #     self.renderer.frame_rate = 2 / alg_options["frame_length"]
        # self.renderer.frame_rate =

        cepton_alg.listen_frames(self.renderer.add_frame)
        self.is_started = True

        self.gps_thread = None
        if cepton_sdk.is_live():
            port = cepton_alg.load.find_gps()
            if port is not None:
                gps_device = serial.Serial(port)
                self.gps_thread = cepton_alg.load.run_gps(gps_device)

        self.resume()
        return True

    def stop(self):
        if not self.is_started:
            return
        if cepton_sdk.capture_replay.is_running():
            cepton_sdk.capture_replay.pause()
        cepton_alg.load.stop()
        self.pause()
        self.renderer.clear()
        self.is_started = False

    def load_settings(self, path):
        self.stop()
        self.settings_dir = cepton_alg.load.InputDataDirectory(path)
        self.refresh()

    @property
    def default_settings_path(self):
        if self.settings_dir.path is not None:
            return self.settings_dir.path
        return fix_path("~/")

    def load_alg_settings(self, path):
        self.stop()
        self.alg_settings_path = path
        self.refresh()

    def save_alg_settings(self, path):
        if self.alg_settings_path is None:
            return
        if path == self.alg_settings_path:
            return
        shutil.copy2(self.alg_settings_path, path)

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

    @property
    def is_capturing(self):
        return self.capture_writer is not None

    def start_capture(self, path):
        self.close_replay()
        self.stop_capture()

        capture_dir = cepton_alg.load.OutputDataDirectory(path)
        if self.settings_dir.path is not None:
            capture_dir.copy_settings(self.settings_dir.path)
        self.capture_writer = cepton_util.capture.CaptureWriter(
            capture_dir.pcap_path)
        self.refresh()

    def stop_capture(self):
        if not self.is_capturing:
            return
        self.capture_writer.close()
        self.capture_writer = None
        self.refresh()

    def open_replay(self, path):
        self.stop_capture()
        self.stop()

        cepton_sdk.open_replay(path)
        self.settings_dir = cepton_alg.load.InputDataDirectory(
            os.path.dirname(path))
        alg_settings_path = self.settings_dir.alg_settings_path
        if alg_settings_path is not None:
            self.load_alg_settings(alg_settings_path)
        render_settings_path = self.settings_dir.render_settings_path
        if render_settings_path is not None:
            self.load_render_settings(render_settings_path)
        self.refresh()

    def close_replay(self):
        if not cepton_sdk.capture_replay.is_open():
            return
        self.stop()
        cepton_sdk.close_replay()
        self.refresh()

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

        menu.addSeparator()

        # Load alg settings
        load_alg_settings = menu.addAction("Load Alg Settings")

        def on_load_alg_settings():
            options = {
                "caption": "Load Alg Settings",
                "filter": "JSON (*.json)",
            }
            path = QFileDialog.getOpenFileName(self.window, **options)[0]
            if not path:
                return
            self.load_alg_settings(path)
        load_alg_settings.triggered.connect(on_load_alg_settings)

        # Save alg settings
        save_alg_settings = menu.addAction("Save Alg Settings")

        def on_save_alg_settings():
            if not self.settings_dir:
                warnings.warn("No settings directory!")
                return
            self.save_alg_settings(self.settings_dir.default_alg_settings_path)
        save_alg_settings.triggered.connect(on_save_alg_settings)

        # Save alg settings as...
        save_alg_settings_as = menu.addAction("Save Alg Settings As...")

        def on_save_alg_settings_as():
            options = {
                "caption": "Save Alg Settings",
                "directory": fix_path("~/cepton_alg_config.json"),
                "filter": "JSON (*.json)",
            }
            path = QFileDialog.getSaveFileName(self.window, **options)[0]
            if not path:
                return
            path = set_extension(path, ".json")
            self.save_alg_settings(path)
        save_alg_settings_as.triggered.connect(on_save_alg_settings_as)

        menu.addSeparator()

        # Load render settings
        load_render_settings = menu.addAction("Load Render Settings")

        def on_load_render_settings():
            options = {
                "caption": "Load Render Settings",
                "filter": "JSON (*.json)",
            }
            path = QFileDialog.getOpenFileName(self.window, **options)[0]
            if not path:
                return
            self.load_render_settings(path)
        load_render_settings.triggered.connect(on_load_render_settings)

        # Save render settings
        save_render_settings = menu.addAction("Save Render Settings")

        def on_save_render_settings():
            if not self.settings_dir:
                warnings.warn("No settings directory!")
                return
            self.save_render_settings(
                self.settings_dir.default_render_settings_path)
        save_render_settings.triggered.connect(on_save_render_settings)

        # Save render settings as...
        save_render_settings_as = menu.addAction("Save Render Settings As...")

        def on_save_render_settings_as():
            options = {
                "caption": "Save Render Settings",
                "directory": fix_path("~/cepton_render_config.json"),
                "filter": "JSON (*.json)",
            }
            path = QFileDialog.getSaveFileName(self.window, **options)[0]
            if not path:
                return
            path = set_extension(path, ".json")
            self.save_render_settings(path)
        save_render_settings_as.triggered.connect(on_save_render_settings_as)

        menu.addSeparator()

        # Open replay
        open_replay = menu.addAction("Open Replay")

        def on_open_replay(*args):
            options = {
                "caption": "Open Replay",
                "directory": get_default_captures_path(),
                "filter": "PCAP (*.pcap)",
            }
            path = QFileDialog.getOpenFileName(self.window, **options)[0]
            if not path:
                return
            self.open_replay(path)
        open_replay.triggered.connect(on_open_replay)

        def update():
            save_alg_settings.setEnabled(bool(self.settings_dir))
            save_render_settings.setEnabled(bool(self.settings_dir))
        self.update_callbacks.append(update)

    def export_points(self, path, **kwargs):
        frame = self.renderer.get_accumulated_frame()
        if frame is None:
            return
        points = frame.points
        points = points[numpy.logical_not(points.is_invalid)]
        cepton_sdk.export.save_points(points, path, **kwargs)

    def start_export_video(self, path):
        frame_rate = self.renderer.frame_rate
        # Video doesn't work with low frame rate
        frame_rate = round(20 / frame_rate) * frame_rate
        self.renderer.exporter = Exporter(
            frame_rate=frame_rate,
            # image_dir=remove_extension(path),
            video_path=path)

    def stop_export_video(self):
        self.renderer.exporter = None

    def create_menu_tools(self, menu):
        # Start capture
        start_capture = menu.addAction("Start Capture")

        def on_start_capture(*args):
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
            self.start_capture(path)
        start_capture.triggered.connect(on_start_capture)

        menu.addSeparator()

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

        # Save video
        save_video = menu.addAction("Save Video")

        def on_save_video():
            options = {
                "caption": "Save Video",
                "directory": os.path.join(get_default_videos_path(), "cepton_{}.mp4".format(get_timestamp_str())),
                "filter": "MP4 (*.mp4)",
            }
            path = QFileDialog.getSaveFileName(self.window, **options)[0]
            if not path:
                return
            path = set_extension(path, ".mp4")
            self.start_export_video(path)
        save_video.triggered.connect(on_save_video)

        def refresh():
            save_video.setEnabled(not cepton_sdk.is_live())
        self.refresh_callbacks.append(refresh)

    def show_cameras(self):
        self.hide_cameras()
        if cepton_sdk.is_live():
            devices = glob.glob("/dev/video[0-9]")
            for device in devices:
                name = "<{}>".format(os.path.basename(device))
                self.video_replay_windows[name] = VideoReplayWindow(name)
        else:
            for camera_path in self.settings_dir.camera_paths:
                name = os.path.basename(camera_path)
                self.video_replay_windows[name] = VideoReplayWindow(
                    camera_path)

    def hide_cameras(self):
        for window in self.video_replay_windows.values():
            window.close()
        self.video_replay_windows = {}

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
            for video_replay in self.video_replay_windows.values():
                video_replay.update(self.renderer.t_animation)
        self.renderer.update_callbacks.append(update)

    def create_toolbox(self):
        selector, stack = super().create_toolbox()

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

        if cepton_alg.advanced():
            selector.addItem("Mask")
            mask = QWidget()
            stack.addWidget(mask)
            self.create_toolbox_mask(mask)

        selector.addItem("Monitors")
        monitors = QWidget()
        stack.addWidget(monitors)
        self.create_toolbox_monitors(monitors)

        selector.addItem("Parameters")
        parameters = QWidget()
        stack.addWidget(parameters)
        self.create_toolbox_parameters(parameters)

        selector.addItem("Profiler")
        profiler = QWidget()
        stack.addWidget(profiler)
        self.create_toolbox_profiler(profiler)

        return selector, stack

    def create_toolbox_general(self, widget):
        layout = QFormLayout()
        widget.setLayout(layout)

        self.create_toolbox_settings(layout)
        self.create_toolbox_capture(layout)
        self.create_toolbox_replay(layout)
        self.create_toolbox_export(layout)
        self.create_toolbox_render(layout)

        return layout

    def create_toolbox_settings(self, parent_layout):
        header = create_toolbox_header("Settings")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        # Alg preset
        alg_preset = QComboBox()
        layout.addRow("Alg Preset", alg_preset)
        alg_presets_dict = cepton_alg.load.get_presets("alg")
        all_alg_presets = sorted(alg_presets_dict.keys())
        alg_preset.addItems([""] + all_alg_presets)
        alg_preset_indices = {
            alg_presets_dict[x]: i for i, x in enumerate(all_alg_presets)}

        def on_alg_preset(i):
            if i == 0:
                self.refresh()
            else:
                self.load_alg_settings(
                    alg_presets_dict[all_alg_presets[i - 1]])
        alg_preset.currentIndexChanged.connect(on_alg_preset)

        # Render preset
        render_preset = QComboBox()
        layout.addRow("Render Preset", render_preset)
        render_presets_dict = cepton_alg.load.get_presets("render")
        all_render_presets = sorted(render_presets_dict.keys())
        render_preset.addItems([""] + all_render_presets)
        render_preset_indices = {
            render_presets_dict[x]: i for i, x in enumerate(all_render_presets)}

        def on_render_preset(i):
            if i == 0:
                return
            else:
                self.load_render_settings(
                    render_presets_dict[all_render_presets[i - 1]])
            render_preset.setCurrentIndex(0)
        render_preset.currentIndexChanged.connect(on_render_preset)

        # Fast
        fast = QCheckBox("Fast")
        layout.addRow(fast)
        fast.setToolTip("Render faster for slow machines and live data.")

        def on_fast():
            self.renderer.fast = fast.isChecked()
        fast.stateChanged.connect(on_fast)

        # Static
        static = QCheckBox("Static")
        layout.addRow(static)
        static.setToolTip("Render static point cloud.")

        def on_static():
            self.renderer.static = static.isChecked()
        static.stateChanged.connect(on_static)

        stop_start = QPushButton("")
        layout.addRow(stop_start)

        def on_stop_start(*args):
            if self.is_started:
                self.stop()
            else:
                self.start()
        stop_start.clicked.connect(on_stop_start)

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
            fast.setEnabled(not self.renderer.is_realtime)
            stop_start.setText("Stop" if self.is_started else "Start")
            pause_resume.setText("Pause" if self.is_running else "Resume")
            pause_resume.setVisible(self.is_started)
        self.update_callbacks.append(update)

        def refresh():
            if self.alg_settings_path is None:
                alg_preset.setCurrentIndex(0)
            elif self.alg_settings_path in alg_preset_indices:
                alg_preset.setCurrentIndex(
                    alg_preset_indices[self.alg_settings_path] + 1)
            else:
                alg_preset.setCurrentIndex(0)
            fast.setChecked(self.renderer.fast)
            static.setChecked(self.renderer.static)
        self.refresh_callbacks.append(refresh)

        return layout

    def create_toolbox_export(self, parent_layout):
        header = create_toolbox_header("Export")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        # Stop video
        stop = QPushButton("Stop")
        layout.addRow(stop)

        def on_stop(*args):
            self.stop_export_video()
        stop.clicked.connect(on_stop)

        # Length
        length = QLabel()
        layout.addRow("Length", length)

        def update():
            is_visible = self.renderer.exporter is not None
            widget.setVisible(is_visible)
            if not is_visible:
                return

            t = self.renderer.exporter.video.t

            length.setText("{}".format(format_seconds(t)))
        self.update_callbacks.append(update)
        return layout

    def create_toolbox_capture(self, parent_layout):
        header = create_toolbox_header("Capture")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        # Stop capture
        stop = QPushButton("Stop")
        layout.addRow(stop)

        def on_stop(*args):
            self.stop_capture()
        stop.clicked.connect(on_stop)

        # Length
        length = QLabel()
        layout.addRow("Length", length)

        def update():
            is_visible = self.is_capturing
            widget.setVisible(is_visible)
            if not is_visible:
                return

            length.setText(format_seconds(self.capture_writer.length))
        self.update_callbacks.append(update)
        return layout

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

        # Filename
        filename = QLabel()
        layout.addRow("Filename", filename)

        # Position
        position = QLabel()
        layout.addRow("Position", position)

        # Seek
        seek = QJumpSlider(Qt.Horizontal)
        layout.addRow(seek)
        seek.setMinimum(0)
        seek.setTickPosition(QSlider.NoTicks)

        def on_seek_released():
            is_started = self.is_started
            is_running = self.is_running
            self.stop()
            t = float(seek.value())
            cepton_sdk.capture_replay.seek(t)
            if is_started:
                self.start()
            if not is_running:
                self.pause()
        seek.sliderReleased.connect(on_seek_released)

        # Loop
        # TODO: Not working. Also, need to clear alg on rewind.
        # loop = QCheckBox("Loop")
        # layout.addRow(loop)

        # def on_loop():
        #     cepton_sdk.capture_replay.set_enable_loop(loop.isChecked())
        # loop.stateChanged.connect(on_loop)

        def update():
            is_visible = cepton_sdk.capture_replay.is_open()
            widget.setVisible(is_visible)
            if not is_visible:
                return

            path = cepton_sdk.capture_replay.get_filename()
            name = os.path.basename(path)
            if name == "lidar.pcap":
                name = os.path.basename(os.path.dirname(path))
            else:
                name = remove_extension(name)
            filename.setText(name)

            seek.setMaximum(int(cepton_sdk.capture_replay.get_length()))
            if seek.isSliderDown():
                t = seek.value()
            else:
                t = cepton_sdk.capture_replay.get_position()
                # t = 0
                # if self.renderer.timestamp is not None:
                #     t = self.renderer.timestamp - cepton_sdk.capture_replay.get_start_time()
                seek.setValue(int(t))
            position.setText("{} / {}".format(
                format_seconds(t),
                format_seconds(cepton_sdk.capture_replay.get_length())))

            # loop.setChecked(cepton_sdk.capture_replay.get_enable_loop())
        self.update_callbacks.append(update)

        return layout

    def create_toolbox_render(self, parent_layout):
        header = create_toolbox_header("Render")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        # Frame Length
        frame_length = QDoubleSpinBox()
        layout.addRow("Frame Length", frame_length)
        frame_length.setSingleStep(0.1)
        frame_length.setMinimum(0)
        frame_length.setMaximum(1)

        def on_frame_length():
            self.renderer.frame_length = frame_length.value()
            self.renderer.refresh()
        frame_length.valueChanged.connect(on_frame_length)

        # Color mode
        color_mode = QComboBox()
        layout.addRow("Color Mode", color_mode)
        color_mode.addItems([enum_to_label(x) for x in FramePointColorMode])

        def on_color_mode(i):
            self.renderer.points_visual.color_mode = FramePointColorMode(i)
            self.renderer.refresh()
        color_mode.currentIndexChanged.connect(on_color_mode)

        # Color map
        color_map = QComboBox()
        layout.addRow("Color Map", color_map)
        color_map.addItems([enum_to_label(x) for x in ColorMap])

        def on_color_map(i):
            self.renderer.points_visual.color_map = ColorMap(i)
            self.renderer.refresh()
        color_map.currentIndexChanged.connect(on_color_map)

        # Color min
        color_min = QDoubleSpinBox()
        layout.addRow("Color Min", color_min)
        color_min.setSingleStep(1)

        def on_color_min():
            self.renderer.points_visual.color_min = color_min.value()
            self.renderer.refresh()
        color_min.valueChanged.connect(on_color_min)

        # Color max
        color_max = QDoubleSpinBox()
        layout.addRow("Color Max", color_max)
        color_max.setSingleStep(1)

        def on_color_max():
            self.renderer.points_visual.color_max = color_max.value()
            self.renderer.refresh()
        color_max.valueChanged.connect(on_color_max)

        # Point size
        point_size = QDoubleSpinBox()
        layout.addRow("Point Size", point_size)
        point_size.setSingleStep(1)
        point_size.setDecimals(2)
        point_size.setMinimum(2)

        def on_point_size():
            self.renderer.point_size = point_size.value()
            self.renderer.refresh()
        point_size.valueChanged.connect(on_point_size)

        # Object color mode
        object_color_mode = QComboBox()
        layout.addRow("Object Color Mode", object_color_mode)
        object_color_mode.addItems([enum_to_label(x)
                                    for x in ObjectPointColorMode])

        def on_object_color_mode(i):
            self.renderer.object_points_visual.color_mode = \
                ObjectPointColorMode(i)
            self.renderer.refresh()
        object_color_mode.currentIndexChanged.connect(on_object_color_mode)

        # Enable shading
        enable_shading = QCheckBox("Enable Shading")
        layout.addRow(enable_shading)

        def on_enable_shading():
            self.renderer.enable_shading = enable_shading.isChecked()
            self.renderer.refresh()
        enable_shading.stateChanged.connect(on_enable_shading)

        # Mirror
        mirror = QCheckBox("Mirror")
        layout.addRow(mirror)

        def on_mirror():
            self.renderer.mirror = mirror.isChecked()
            self.renderer.refresh()
        mirror.stateChanged.connect(on_mirror)

        # Show car
        show_car = QCheckBox("Show Car")
        layout.addRow(show_car)

        def on_show_car():
            self.renderer.show_car = show_car.isChecked()
            self.renderer.refresh()
        show_car.stateChanged.connect(on_show_car)

        # Show grid
        show_grid = QCheckBox("Show Grid")
        layout.addRow(show_grid)

        def on_show_grid():
            self.renderer.show_grid = show_grid.isChecked()
            self.renderer.refresh()
        show_grid.stateChanged.connect(on_show_grid)

        # Show object boxes
        show_object_boxes = QCheckBox("Show Object Boxes")
        layout.addRow(show_object_boxes)

        def on_show_object_boxes():
            self.renderer.object_boxes_visual.visible = show_object_boxes.isChecked()
            self.renderer.refresh()
        show_object_boxes.stateChanged.connect(on_show_object_boxes)

        # Show object trajectories
        show_object_trajectories = QCheckBox("Show Object Trajectories")
        layout.addRow(show_object_trajectories)

        def on_show_object_trajectories():
            self.renderer.object_trajectories_visual.visible = show_object_trajectories.isChecked()
            self.renderer.refresh()
        show_object_trajectories.stateChanged.connect(
            on_show_object_trajectories)

        # Motion mode
        motion_mode = QComboBox()
        layout.addRow("Motion Mode", motion_mode)
        motion_mode.addItems(["None"] + [enum_to_label(x)
                                         for x in ViewMotionMode])

        def on_motion_mode(i):
            if i == 0:
                self.renderer.view_motion_mode = None
            else:
                self.renderer.view_motion_mode = ViewMotionMode(i - 1)
            self.renderer.refresh()
        motion_mode.currentIndexChanged.connect(on_motion_mode)

        def update():
            color_min.setEnabled(
                not self.renderer.points_visual.is_color_scale_constant)
            color_max.setEnabled(
                not self.renderer.points_visual.is_color_scale_constant)
        self.update_callbacks.append(update)

        def refresh():
            frame_length.setValue(self.renderer.frame_length)
            color_mode.setCurrentIndex(
                int(self.renderer.points_visual.color_mode))
            color_map.setCurrentIndex(
                int(self.renderer.points_visual.color_map))
            color_min.setValue(self.renderer.points_visual.color_min)
            color_max.setValue(self.renderer.points_visual.color_max)
            point_size.setValue(self.renderer.point_size)
            object_color_mode.setCurrentIndex(
                int(self.renderer.object_points_visual.color_mode))
            enable_shading.setChecked(self.renderer.enable_shading)
            mirror.setChecked(self.renderer.mirror)
            show_car.setChecked(self.renderer.show_car)
            show_grid.setChecked(self.renderer.show_grid)
            show_object_boxes.setChecked(self.renderer.show_object_boxes)
            show_object_trajectories.setChecked(
                self.renderer.show_object_trajectories)
            if self.renderer.view_motion_mode is None:
                motion_mode.setCurrentIndex(0)
            else:
                motion_mode.setCurrentIndex(self.renderer.view_motion_mode + 1)
        self.refresh_callbacks.append(refresh)

        def update():
            enable_shading.setEnabled(not self.renderer.fast)
            frame_length.setEnabled(not self.renderer.fast)
        self.update_callbacks.append(update)

        return layout

    def create_toolbox_advanced(self, widget):
        layout = QFormLayout()
        widget.setLayout(layout)

        self.create_toolbox_render_advanced(layout)
        self.create_toolbox_debug(layout)
        self.create_toolbox_view(layout)

        return layout

    def create_toolbox_mask(self, widget):
        layout = QFormLayout()
        widget.setLayout(layout)

        self.create_toolbox_image_mask_editor(layout)
        self.create_toolbox_mask_editor(layout)

        return layout

    def create_toolbox_mask_editor(self, parent_layout):
        header = create_toolbox_header("3D Mask Editor")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        def editor():
            return self.renderer.active_mask_editor

        # ID
        mask_id = QComboBox()
        layout.addRow("ID", mask_id)
        GridMaskId = cepton_alg.core.GridMaskId
        all_mask_ids = [None, GridMaskId.ABSOLUTE_3D, GridMaskId.RELATIVE_3D]
        mask_id.addItems([""] + [x.name for x in all_mask_ids[1:]])
        mask_id_indices = {x: (i + 1) for i, x in enumerate(all_mask_ids)}

        def on_mask_id(i):
            self.renderer.active_mask_editor_id = all_mask_ids[i]
            self.refresh()
        mask_id.currentIndexChanged.connect(on_mask_id)

        # Save
        save = QPushButton("Save")
        layout.addRow(save)

        def on_save():
            editor().save_mask()
            if self.settings_dir:
                path = self.settings_dir.default_grid_mask_path
                cepton_alg.load.save_grid_mask(
                    editor().mask_id, editor().mask, path)
            self.refresh()
        save.clicked.connect(on_save)

        # Reload
        reload_mask = QPushButton("Reload")
        layout.addRow(reload_mask)

        def on_reload():
            editor().reload_mask()
            self.refresh()
        reload_mask.clicked.connect(on_reload)

        # Clear
        clear = QPushButton("Clear")
        layout.addRow(clear)

        def on_clear():
            editor().reset_mask()
            self.refresh()
        clear.clicked.connect(on_clear)

        # Enabled
        enabled = QCheckBox("Enabled")
        layout.addRow(enabled)

        def on_enabled():
            editor().mask_enabled = enabled.isChecked()
            self.refresh()
        enabled.stateChanged.connect(on_enabled)

        # Add Points
        add_points = QPushButton("Add Selected Points")
        layout.addRow(add_points)

        def on_add_points():
            points = self.renderer.points_selector.selected_points
            if points is None:
                return
            editor().add_balls(points.positions, 0.5)
        add_points.clicked.connect(on_add_points)

        # Add Object
        add_object = QPushButton("Add Selected Object")
        layout.addRow(add_object)

        def on_add_object():
            selected_points = self.renderer.points_selector.selected_points
            if selected_points is None:
                return
            selected_object_idx = selected_points.object_indices[0]
            if selected_object_idx < 0:
                return
            points = self.renderer.points_selector.points
            is_valid = (points.object_indices == selected_object_idx)
            points = points[is_valid]
            editor().add_balls(points.positions, 0.5)
        add_object.clicked.connect(on_add_object)

        def update():
            has_editor = editor() is not None
            save.setEnabled(has_editor)
            reload_mask.setEnabled(has_editor)
            clear.setEnabled(has_editor)
            enabled.setEnabled(has_editor)
            add_points.setEnabled(has_editor)
            add_object.setEnabled(has_editor)
        self.update_callbacks.append(update)

        def refresh():
            if editor() is None:
                return

            enabled.setChecked(editor().mask.enabled)
        self.refresh_callbacks.append(refresh)

    def create_toolbox_image_mask_editor(self, parent_layout):
        header = create_toolbox_header("2D Mask Editor")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        def editor():
            return self.renderer.active_image_mask_editor

        # ID
        mask_id = QComboBox()
        layout.addRow("ID", mask_id)
        GridMaskId = cepton_alg.core.GridMaskId
        all_mask_ids = [None, GridMaskId.ABSOLUTE_2D, GridMaskId.RELATIVE_2D]
        mask_id.addItems([""] + [x.name for x in all_mask_ids[1:]])
        mask_id_indices = {x: i for i, x in enumerate(all_mask_ids)}

        def on_mask_id(i):
            self.renderer.active_image_mask_editor_id = all_mask_ids[i]
            self.refresh()
        mask_id.currentIndexChanged.connect(on_mask_id)

        # Save
        save = QPushButton("Save")
        layout.addRow(save)

        def on_save():
            editor().save_mask()
            if self.settings_dir:
                path = self.settings_dir.default_grid_mask_path
                cepton_alg.load.save_grid_mask(
                    editor().mask_id, editor().mask, path)
            self.refresh()
        save.clicked.connect(on_save)

        # Reload
        reload_mask = QPushButton("Reload")
        layout.addRow(reload_mask)

        def on_reload():
            editor().reload_mask()
            self.refresh()
        reload_mask.clicked.connect(on_reload)

        # Clear
        clear = QPushButton("Clear")
        layout.addRow(clear)

        def on_clear():
            editor().reset_mask()
            self.refresh()
        clear.clicked.connect(on_clear)

        # Enabled
        enabled = QCheckBox("Enabled")
        layout.addRow(enabled)

        def on_enabled():
            editor().mask_enabled = enabled.isChecked()
            self.refresh()
        enabled.stateChanged.connect(on_enabled)

        # Brush size
        brush_size = QDoubleSpinBox()
        layout.addRow("Brush Size", brush_size)
        brush_size.setMinimum(0)
        brush_size.setMaximum(100)
        brush_size.setSingleStep(1)

        def on_brush_size():
            editor().brush_size = brush_size.value()
            self.refresh()
        brush_size.valueChanged.connect(on_brush_size)

        def update():
            has_editor = editor() is not None
            save.setEnabled(has_editor)
            reload_mask.setEnabled(has_editor)
            clear.setEnabled(has_editor)
            enabled.setEnabled(has_editor)
            brush_size.setEnabled(has_editor)
        self.update_callbacks.append(update)

        def refresh():
            mask_id.setCurrentIndex(
                mask_id_indices[self.renderer.active_image_mask_editor_id])

            if editor() is None:
                return

            enabled.setChecked(editor().mask_enabled)
            brush_size.setValue(editor().brush_size)
        self.refresh_callbacks.append(refresh)

        return layout

    def create_toolbox_view(self, parent_layout):
        header = create_toolbox_header("View")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        # Origin
        origin = QPushButton("Origin")
        layout.addRow(origin)

        def on_origin():
            self.renderer.camera.center = [0, 0, 0]
            self.refresh()
        origin.clicked.connect(on_origin)

        azimuth = QLabel()
        layout.addRow("Azimuth", azimuth)

        elevation = QLabel()
        layout.addRow("Elevation", elevation)

        scale_factor = QLabel()
        layout.addRow("Scale Factor", scale_factor)

        fov = QLabel()
        layout.addRow("FOV", fov)

        center = QLabel()
        layout.addRow("Center", center)

        def update():
            azimuth.setText("{}°".format(int(self.renderer.camera.azimuth)))
            elevation.setText("{}°".format(
                int(self.renderer.camera.elevation)))
            scale_factor.setText("{}".format(
                int(self.renderer.camera.scale_factor)))
            fov.setText("{}°".format(int(self.renderer.camera.fov)))
            center.setText("[{}] m".format(
                ", ".join([str(int(x)) for x in self.renderer.camera.center])))
        self.update_callbacks.append(update)
        return layout

    def create_toolbox_render_advanced(self, parent_layout):
        header = create_toolbox_header("Render")
        parent_layout.addRow(header)

        widget = QWidget()
        parent_layout.addRow(widget)
        layout = QFormLayout()
        widget.setLayout(layout)

        # Frame rate
        frame_rate = QDoubleSpinBox()
        layout.addRow("Frame Rate", frame_rate)
        frame_rate.setSingleStep(5)
        frame_rate.setDecimals(0)
        frame_rate.setMinimum(5)

        def on_frame_rate():
            self.renderer.frame_rate = frame_rate.value()
            self.refresh()
        frame_rate.valueChanged.connect(on_frame_rate)

        # Interpolate frames
        interpolate_frames = QCheckBox("Interpolate Frames")
        layout.addRow(interpolate_frames)

        def on_interpolate_frames():
            self.renderer.interpolate_frames = interpolate_frames.isChecked()
            self.refresh()
        interpolate_frames.stateChanged.connect(on_interpolate_frames)

        def update():
            frame_rate.setEnabled(
                (not self.is_running) and (self.renderer.exporter is None) and
                (not self.renderer.is_realtime))
            interpolate_frames.setEnabled(not self.renderer.fast)
        self.update_callbacks.append(update)

        def refresh():
            frame_rate.setValue(self.renderer.frame_rate)
            interpolate_frames.setChecked(self.renderer.interpolate_frames)
        self.refresh_callbacks.append(refresh)

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

        # Coordinate reference
        coordinate_reference = QComboBox()
        layout.addRow("Coordinate Reference", coordinate_reference)
        all_coordinate_reference = [
            enum_to_label(x) for x in CoordinateReference]
        coordinate_reference.addItems(all_coordinate_reference)

        def on_coordinate_reference(i):
            self.renderer.coordinate_reference = CoordinateReference(i)
            self.renderer.refresh()
        coordinate_reference.currentIndexChanged.connect(
            on_coordinate_reference)

        # Show all points
        show_all_points = QCheckBox("Show All Points")
        layout.addRow(show_all_points)

        def on_show_all_points():
            self.renderer.show_all_points = show_all_points.isChecked()
            self.renderer.refresh()
        show_all_points.stateChanged.connect(on_show_all_points)

        # Selected Points
        selected_points_flag = QComboBox()
        layout.addRow("Selected Points", selected_points_flag)
        CombinedPointFlag = cepton_alg.CombinedPointFlag
        all_point_flags = [enum_to_label(x) for x in CombinedPointFlag]
        selected_points_flag.addItems(["None"] + all_point_flags)

        def on_selected_points_flag(i):
            if i == 0:
                self.renderer.selected_points_flag = None
            else:
                self.renderer.selected_points_flag = \
                    CombinedPointFlag.get_by_index(i - 1)
            self.renderer.refresh()
        selected_points_flag.currentIndexChanged.connect(
            on_selected_points_flag)

        # Downsample ground
        downsample_ground = QCheckBox("Downsample Ground")
        layout.addRow(downsample_ground)

        def on_downsample_ground():
            self.renderer.downsample_ground = downsample_ground.isChecked()
            self.renderer.refresh()
        downsample_ground.stateChanged.connect(on_downsample_ground)
        downsample_ground.setChecked(True)

        # Show scan
        show_scan = QCheckBox("Show Scan")
        layout.addRow(show_scan)

        def on_show_scan():
            self.renderer.show_scan = show_scan.isChecked()
            self.renderer.refresh()
        show_scan.stateChanged.connect(on_show_scan)

        # Show all objects
        show_all_objects = QCheckBox("Show All Objects")
        layout.addRow(show_all_objects)

        def on_show_all_objects():
            self.renderer.show_all_objects = show_all_objects.isChecked()
            self.renderer.refresh()
        show_all_objects.stateChanged.connect(on_show_all_objects)

        # Show object labels
        show_object_labels = QCheckBox("Show Object Labels")
        layout.addRow(show_object_labels)

        def on_show_object_labels():
            self.renderer.object_labels_visual.visible = show_object_labels.isChecked()
            self.renderer.refresh()
        show_object_labels.stateChanged.connect(on_show_object_labels)

        # Show surfaces
        show_surfaces = QCheckBox("Show Surfaces")
        layout.addRow(show_surfaces)

        def on_show_surfaces():
            self.renderer.show_surfaces = show_surfaces.isChecked()
            self.renderer.refresh()
        show_surfaces.stateChanged.connect(on_show_surfaces)

        def refresh():
            if self.renderer.angle_ruler_enabled:
                measurement.setCurrentIndex(1)
            elif self.renderer.distance_ruler_enabled:
                measurement.setCurrentIndex(2)
            else:
                measurement.setCurrentIndex(0)
            coordinate_reference.setCurrentIndex(
                self.renderer.coordinate_reference)
            show_all_points.setChecked(self.renderer.show_all_points)
            if self.renderer.selected_points_flag is None:
                selected_points_flag.setCurrentIndex(0)
            else:
                selected_points_flag.setCurrentIndex(
                    CombinedPointFlag.get_index(self.renderer.selected_points_flag) + 1)
            downsample_ground.setChecked(self.renderer.downsample_ground)
            show_scan.setChecked(self.renderer.show_scan)
            show_all_objects.setChecked(self.renderer.show_all_objects)
            show_object_labels.setChecked(self.renderer.show_object_labels)
            show_surfaces.setChecked(self.renderer.show_surfaces)
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

        tree = QJSONView()
        layout.addWidget(tree.widget)
        tree.widget.setSortingEnabled(False)

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
                ["Serial #", str(points.serial_numbers[i])],
                ["Segment #", str(points.segment_indices[i])],
                ["Object", str(points.object_indices[i])],
                ["Surface", str(points.surface_indices[i])],
                ["Timestamp", "{:.3f}".format(points.timestamps[i])],
                ["Distance", "{:3.2f}".format(points.distances[i])],
                ["Position", position_to_str(points.positions[i, :])],
                ["Intensity", "{:.2f}".format(points.intensities[i])],
                ["Return Type", collections.OrderedDict(
                    [[enum_to_label(flag), str(points.return_types[i, flag])]
                     for flag in cepton_sdk.ReturnType])],
                ["Flags", collections.OrderedDict(
                    [[enum_to_label(flag), str(points.flags[i, flag])]
                     for flag in cepton_sdk.PointFlag])],
                ["Alg Flags", collections.OrderedDict(
                    [[enum_to_label(flag), str(points.alg_flags[i, flag])]
                     for flag in cepton_alg.frame.PointFlag])],
            ]) for i in range(len(points))]
            data = collections.OrderedDict([
                ["Count", len(points)],
                ["Mean Position", position_to_str(
                    numpy.mean(points.positions, axis=0))],
                ["Points", points_data],
            ])
            tree.set_data(data)
            tree.expand(1)
        self.renderer.points_selector.update_callbacks.append(update)

        return layout

    def create_toolbox_monitors(self, widget):
        layout = QFormLayout()
        widget.setLayout(layout)

        header = create_toolbox_header("Version")
        layout.addRow(header)

        sdk_version = QLabel(cepton_sdk.__version__)
        layout.addRow("SDK Version", sdk_version)

        alg_version = QLabel(cepton_alg.__version__)
        layout.addRow("Alg Version", alg_version)

        header = create_toolbox_header("Frame")
        layout.addRow(header)

        timestamp = QLabel()
        layout.addRow("Timestamp", timestamp)

        position = QLabel()
        layout.addRow("Position", position)

        speed = QLabel()
        layout.addRow("Speed", speed)

        turning_radius = QLabel()
        layout.addRow("Turning Radius", turning_radius)

        n_points = QLabel()
        layout.addRow("# Points", n_points)

        n_objects = QLabel()
        layout.addRow("# Objects", n_objects)

        def numpy_to_str(a, pattern=""):
            pattern = "{" + pattern + "}"
            return "[" + ", ".join([pattern.format(x) for x in a]) + "]"

        def update():
            frame = self.renderer.frame
            if not frame:
                return

            timestamp.setText("{:.1f} s".format(frame.timestamp))
            position.setText("{} m".format(numpy_to_str(
                frame.motion_state.transform.translation[0, :], ":.1f")))
            speed.setText(
                "{:.1f} m/s".format(frame.motion_state.velocity.translation[0, 1]))
            turning_radius.setText(
                "{:.1f} °/s".format(numpy.degrees(
                    frame.motion_state.velocity.rotation_vector[0, 2])))
            n_points.setText("{:,}".format(len(frame.points)))
            n_objects.setText("{}".format(len(frame.objects)))
        self.update_callbacks.append(update)

        return layout

    def create_toolbox_parameters(self, widget):
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.parameter_viewer = QJSONView()
        layout.addWidget(self.parameter_viewer.widget)
        self.parameter_viewer.widget.setSortingEnabled(True)

        def update():
            data = cepton_alg.get_options()
            self.parameter_viewer.set_data(data)
            self.parameter_viewer.expand(0)
        self.renderer.update_callbacks.append(update)

        return layout

    def create_toolbox_profiler(self, widget):
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.profiler_viewer = QJSONView()
        layout.addWidget(self.profiler_viewer.widget)
        self.profiler_viewer.widget.setSortingEnabled(False)

        def update():
            data = cepton_alg.get_profiler_report()

            def format_task(data):
                return {
                    "# Calls": data["n_calls"],
                    "Mean (Max)": "{:.3f}s ({:.3f}s)".format(data["mean_time"], data["max_time"]),
                }
            for name in data:
                data[name] = format_task(data[name])

            self.profiler_viewer.set_data(data)
            self.profiler_viewer.expand(1)
        self.renderer.update_callbacks.append(update)
        return layout

    def on_drag(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def on_drop(self, event):
        if event.mimeData().hasUrls:
            path = event.mimeData().urls()[0]
            path = QDir.toNativeSeparators(path.toLocalFile())
            name = os.path.basename(path)
            if os.path.isdir(path):
                self.open_replay(os.path.join(path, "lidar.pcap"))
            elif name.lower().endswith(".pcap"):
                self.open_replay(path)
            event.accept()
        else:
            event.ignore()


__all__ = _all_builder.get()
