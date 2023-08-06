#!python

import argparse
import sys
import warnings

import cepton_alg_redist
import cepton_alg_redist.load
import cepton_sdk
from cepton_alg_redist.viewer import *


def main():
    parser = argparse.ArgumentParser()
    all_alg_presets = sorted(cepton_alg_redist.load.get_presets("alg").keys())
    parser.add_argument("--advanced", action="store_true",
                        help="Enable advanced features.")
    parser.add_argument("--alg_preset", choices=all_alg_presets)
    parser.add_argument("--alg_settings_path")
    parser.add_argument("--capture_path")
    parser.add_argument("--capture_seek")
    parser.add_argument("--render_settings_path")
    parser.add_argument("--settings_dir")
    parser.add_argument("--start", action="store_true")
    args = parser.parse_args()

    if args.advanced:
        cepton_alg_redist.set_advanced(True)
    else:
        warnings.filterwarnings("ignore")

    cepton_alg_redist.initialize_sdk()

    app = QApplication(sys.argv)

    viewer = Viewer(renderer=ViewerRenderer())
    if args.render_settings_path is not None:
        render_settings_path = fix_path(args.render_settings_path)
        viewer.load_render_settings(render_settings_path)
    if args.alg_settings_path is not None:
        alg_settings_path = fix_path(args.alg_settings_path)
    elif args.alg_preset is not None:
        alg_settings_path = cepton_alg_redist.load.get_preset(
            "alg", args.alg_preset)
    else:
        alg_settings_path = cepton_alg_redist.load.get_preset("alg", "default")
    viewer.load_alg_settings(alg_settings_path)
    if args.capture_path is not None:
        capture_path = fix_path(args.capture_path)
        viewer.open_replay(capture_path)
    if args.capture_seek is not None:
        capture_seek = parse_time_hms(args.capture_seek)
        cepton_sdk.capture_replay.seek(capture_seek)
    if args.settings_dir is not None:
        settings_dir = fix_path(args.settings_dir)
        viewer.load_settings(settings_dir)
    if args.start:
        viewer.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
