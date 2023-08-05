import os.path
import signal
import time

import cepton_alg.common.render
from cepton_alg.common import *

_all_builder = AllBuilder(__name__)

from PyQt5.QtCore import *  # noqa isort:skip
from PyQt5.QtGui import *  # noqa isort:skip
from PyQt5.QtWidgets import *  # noqa isort:skip

from cepton_util.common import *  # noqa isort:skip


def name_to_label(value):
    return value.lower().replace("_", " ").title()


def enum_to_label(value):
    return name_to_label(value.name)


def format_seconds(t):
    return time.strftime("%M:%S", time.gmtime(t))


def _get_default_path(path):
    path = fix_path(path)
    if os.path.exists(path):
        return path
    return fix_path("~/")


def get_default_captures_path():
    return _get_default_path("~/Captures")


def get_default_images_path():
    return _get_default_path("~/Pictures")


def get_default_videos_path():
    return _get_default_path("~/Videos")


class WindowBase:
    def __init__(self):
        self.refresh_callbacks = []
        self.update_callbacks = []  # Called every 100Hz
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self.update)
        self._update_timer.start(100)

        self.window.closeEvent = self.on_close

    def on_close(self, *args):
        self._update_timer.stop()

    def update(self):
        for func in self.update_callbacks:
            func()

    def refresh(self):
        for func in self.refresh_callbacks:
            func()


class MainWindow(WindowBase):
    def __init__(self, **kwargs):
        self.window = QMainWindow()

        super().__init__(**kwargs)

        self.window.setAcceptDrops(True)
        self.window.dragEnterEvent = self.on_drag
        self.window.dragMoveEvent = self.on_drag
        self.window.dropEvent = self.on_drop
        self.window.keyPressEvent = self.on_key_press

        signal.signal(signal.SIGINT, self.on_sigint)

    def on_close(self, *args):
        super().on_close(*args)
        QCoreApplication.quit()

    def on_sigint(self, *args):
        QCoreApplication.quit()

    def on_drag(self, *args):
        pass

    def on_drop(self, *args):
        pass

    def on_key_press(self, *args):
        pass

    def create_menu(self):
        return self.window.menuBar()

    def create_toolbox(self):
        self.toolbox = QDockWidget("", self.window)
        self.window.addDockWidget(Qt.LeftDockWidgetArea, self.toolbox)
        self.toolbox.setFeatures(QDockWidget.DockWidgetClosable)

        scroll = QScrollArea()
        self.toolbox.setWidget(scroll)
        scroll.setWidgetResizable(True)

        widget = QWidget()
        scroll.setWidget(widget)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        selector = QComboBox()
        layout.addWidget(selector)

        stack = QStackedWidget()
        layout.addWidget(stack)

        def on_selector(i):
            stack.setCurrentIndex(i)
        selector.currentIndexChanged.connect(on_selector)

        return selector, stack

    def show_toolbox(self):
        self.toolbox.setVisible(True)


class Window(WindowBase):
    def __init__(self, **kwargs):
        self.window = QWidget()

        super().__init__(**kwargs)

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.window.close()
        except:
            pass


def create_toolbox_header(name):
    label = QLabel(name)
    label.setAlignment(Qt.AlignLeft)
    font = QFont()
    font.setBold(True)
    label.setFont(font)
    return label


class QJumpSlider(QSlider):
    def _update_value(self, event):
        value = QStyle.sliderValueFromPosition(
            self.minimum(), self.maximum(), event.x(), self.width())
        self.setValue(value)

    def mousePressEvent(self, event):
        self.setSliderDown(True)
        self._update_value(event)

    def mouseMoveEvent(self, event):
        self._update_value(event)

    def mouseReleaseEvent(self, event):
        self.sliderReleased.emit()
        self.setSliderDown(False)


def clear_layout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)


class JSONView:
    def __init__(self):
        self.widget = QTreeView()
        self.widget.header().hide()
        self.widget.setEditTriggers(QTreeView.NoEditTriggers)
        self.widget.setSortingEnabled(True)

        self.model = QStandardItemModel()
        self.widget.setModel(self.model)
        self.model.setColumnCount(2)

        # def on_selection(idx, _):
        #     # item = self.model.item(idx.column())
        #     item = self.model.itemFromIndex(idx)
        #     items = []
        #     while item:
        #         print(item.data())
        #         items.append(item)
        #         item = item.parent()
        #     # print(items)
        # self.widget.selectionModel().currentRowChanged.connect(on_selection)

    def _populate(self, parent, data, key=""):
        key_item = QStandardItem(key)
        if isinstance(data, dict):
            if key:
                value_item = QStandardItem("")
                parent.appendRow([key_item, value_item])
                parent = key_item
            for child_key in data:
                self._populate(parent, data[child_key], key=child_key)
        elif isinstance(data, list) and (len(data) > 0) and isinstance(data[0], dict):
            # List of dict
            if key:
                value_item = QStandardItem("")
                parent.appendRow([key_item, value_item])
                parent = key_item
            for i, child_data in enumerate(data):
                if "name" in child_data:
                    child_key = child_data["name"]
                    del child_data["name"]
                else:
                    child_key = "{} [{}]".format(key, i)
                self._populate(parent, child_data, key=child_key)
        else:
            # Value
            value_item = QStandardItem(str(data))
            parent.appendRow([key_item, value_item])

    def set_data(self, data):
        self.model.clear()
        self._populate(self.model.invisibleRootItem(), data)

    def expand(self, depth):
        self.widget.expandToDepth(depth)
        self.widget.resizeColumnToContents(0)
        self.widget.resizeColumnToContents(1)


class VideoReplayWindow(Window):
    def __init__(self, path, **kwargs):
        super().__init__(**kwargs)

        self.image = None
        self.video_replay = cepton_alg.common.render.VideoReplay(path)

        self.window.setWindowTitle(os.path.basename(path))
        self.window.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.window.resize(500, 300)
        self.window.show()

        layout = QVBoxLayout()
        self.window.setLayout(layout)

        # Kind of a hack for resizing window
        widget = QScrollArea()
        layout.addWidget(widget)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.canvas = QLabel()
        layout.addWidget(self.canvas)

        def update():
            if self.image is None:
                return
            width = self.canvas.frameGeometry().width()
            image = self.image.scaledToWidth(width)
            pixmap = QPixmap(image)
            self.canvas.setPixmap(pixmap)
            self.window.setFixedHeight(image.height())
        self.update_callbacks.append(update)

    def on_close(self, *args):
        super().on_close(*args)
        self.video_replay.close()

    def seek(self, t):
        try:
            frame = self.video_replay.get_frame(t)
        except:
            return
        self.image = QImage(
            frame.tobytes(), frame.shape[1], frame.shape[0], QImage.Format_RGB888)


__all__ = _all_builder.get()
