#!/usr/bin/env python3

import argparse
import pprint
import sys
import warnings

import cepton_alg_redist
import cepton_alg_redist.api
import cepton_alg_redist.load
from cepton_alg_redist.render import *
from cepton_util.common import *


def main():
    parser = argparse.ArgumentParser(usage="%(prog)s [OPTIONS]")
    cepton_alg_redist.load.Loader.add_arguments(parser)
    Exporter.add_arguments(parser)
    parser.add_argument("--advanced", action="store_true",
                        help="Enable advanced features.")
    parser.add_argument("--render_settings_path")
    args = parser.parse_args()

    if args.advanced:
        cepton_alg_redist.set_advanced(True)
    else:
        warnings.filterwarnings("ignore")

    cepton_alg_redist.load.Loader.from_arguments(args)
    pprint.pprint(cepton_alg_redist.get_options())

    renderer = FrameRenderer()
    renderer.exporer = Exporter.from_arguments(args)

    if args.render_settings_path is not None:
        render_settings_path = fix_path(args.render_settings_path)
        with open(args.render_settings_path, "r") as f:
            render_settings = json.load(f)
        renderer.set_options(**render_settings.get("renderer", {}))
    pprint.pprint(renderer.get_options())

    cepton_alg_redist.api.listen_frames(renderer.add_frame)

    renderer.resume_animation()
    renderer.run()


if __name__ == "__main__":
    main()
