import collections
import threading
import time

import cepton_alg.core
import cepton_sdk
import cepton_util.common
from cepton_alg.common import *

_all_builder = AllBuilder(__name__)


def wait_once():
    if cepton_sdk.is_realtime() or cepton_alg.core.is_full():
        time.sleep(0.1)
    else:
        cepton_sdk.capture_replay.resume_blocking(0.1)


def wait(duration=-1):
    t_0 = cepton_sdk.get_time()
    while True:
        wait_once()
        if duration >= 0:
            if (cepton_sdk.get_time() - t_0) > duration:
                break
        if is_end():
            break


def initialize(model=None, **kwargs):
    if model is None:
        sensor = cepton_sdk.Sensor.create_by_index(0)
        model = sensor.information.model

    # Initialize alg
    options = {
        "live": cepton_sdk.is_live(),
        "model": model,
        "tasks": [],
    }
    options.update(kwargs)
    cepton_alg.core._manager.initialize(**options)
    cepton_alg.core._manager.frames_callback.initialize()


def deinitialize():
    cepton_alg.core._manager.frames_callback.deinitialize()
    cepton_alg.core._manager.deinitialize()


def listen_frames(callback):
    return cepton_alg.core._manager.frames_callback.listen(callback)


def unlisten_frames(callback_id):
    return cepton_alg.core._manager.frames_callback.unlisten(callback_id)


def _wait_on_func(func, timeout=None):
    if timeout is not None:
        t_0 = cepton_sdk.get_timestamp()
    while not func():
        wait_once()
        if timeout is not None:
            if (cepton_sdk.get_timestamp() - t_0) > timeout:
                raise RuntimeError("Timed out!")


class FramesListener:
    def __init__(self):
        self._lock = threading.Lock()
        self._frames = collections.deque()
        self._callback_id = cepton_alg.core._manager.frames_callback.listen(
            self._on_frame)

    def __del__(self):
        try:
            cepton_alg.core._manager.frames_callback.unlisten(
                self._callback_id)
        except:
            pass

    def reset(self):
        with self._lock:
            self._frames = []

    def _on_frame(self, frame):
        with self._lock:
            self._frames.append(frame)

    def has_frames(self):
        with self._lock:
            return len(self._frames) > 0

    def _get_frame(self):
        with self._lock:
            return self._frames.popleft()

    def get_frame(self, **kwargs):
        _wait_on_func(self.has_frames, **kwargs)
        return self._get_frame()


__all__ = _all_builder.get()
