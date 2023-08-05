#!/usr/bin/env python3

# Disable warnings
import warnings  # noqa isort:skip
warnings.filterwarnings("ignore")  # noqa isort:skip

import argparse
import sys

import cepton_alg_redist
import cepton_alg_redist.api
import cepton_alg_redist.load
from cepton_alg_redist.render import *
from cepton_util.common import *


def main():
    parser = argparse.ArgumentParser(usage="%(prog)s [OPTIONS]")
    cepton_alg_redist.load.Loader.add_arguments(parser)
    Exporter.add_arguments(parser)
    parser.add_argument("--render_settings_path")
    args = parser.parse_args()

    cepton_alg_redist.load.Loader.from_arguments(args)

    renderer = FrameRenderer()
    renderer.exporer = Exporter.from_arguments(args)

    render_settings = {}
    if args.render_settings_path is not None:
        render_settings_path = fix_path(args.render_settings_path)
        with open(args.render_settings_path, "r") as f:
            render_settings.update(json.load(f))
    renderer.points_visual.set_options(
        **render_settings.get("points_visual", {}))
    renderer.set_options(**render_settings.get("renderer", {}))

    cepton_alg_redist.api.listen_frames(renderer.add_frame)

    renderer.run()


if __name__ == "__main__":
    main()
