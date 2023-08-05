#!/usr/bin/env python3

# Disable warnings
import warnings  # noqa isort:skip
warnings.filterwarnings("ignore")  # noqa isort:skip

import argparse
import sys

import cepton_sdk
from cepton_alg_redist.common.viewer_sdk import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture_path")
    parser.add_argument("--settings_dir")
    args = parser.parse_args()

    cepton_sdk.initialize()

    app = QApplication(sys.argv)

    viewer = Viewer(renderer=ViewerRenderer())
    if args.capture_path is not None:
        capture_path = fix_path(args.capture_path)
        viewer.open_replay(capture_path)
    if args.settings_dir is not None:
        settings_dir = fix_path(args.settings_dir)
        viewer.load_settings(settings_dir)
    cepton_sdk.listen_frames(viewer.renderer.add_points)
    viewer.resume()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
