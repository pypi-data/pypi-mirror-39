#!python

import argparse
import sys
import warnings

import cepton_alg_redist
import cepton_sdk
from cepton_alg_redist.common.viewer_sdk import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--advanced", action="store_true",
                        help="Enable advanced features.")
    parser.add_argument("--capture_path")
    parser.add_argument("--settings_dir")
    args = parser.parse_args()

    if args.advanced:
        cepton_alg_redist.set_advanced(True)
    else:
        warnings.filterwarnings("ignore")

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
