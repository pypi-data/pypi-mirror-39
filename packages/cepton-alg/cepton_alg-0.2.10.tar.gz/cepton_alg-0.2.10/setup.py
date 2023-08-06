#!/usr/bin/env python3

import platform
import sys

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="cepton_alg",
        version="0.2.10",
        description="Cepton Python",
        long_description=open("README.md").read(),
        url="https://github.com/ceptontech/cepton_alg_redist",
        author="Cepton Technologies",
        author_email="support@cepton.com",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3",
        ],
        keywords="cepton",
        python_requires=">=3.3",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=[
            "cepton_sdk>=1.10.1",
            "imageio",
            "laspy",
            "matplotlib",
            "numpy_stl",
            "numpy",
            "parse",
            "pillow",
            "plyfile",
            "pynmea2",
            "pyqt5",
            "pyserial",
            "scipy",
            "seaborn",
            "transforms3d",
            "uuid",
            "vispy",
        ],
        extras_require={
            "capture": [
                "netifaces",
            ],
            "mask": [
                "pillow",
                "pykdtree",
            ],
        },
        scripts=[
            "samples/cepton_alg_render.py",
            "samples/cepton_alg_viewer.py",
            "samples/common/cepton_player.py",
        ]
    )
