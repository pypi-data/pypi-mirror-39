#!/usr/bin/env python3

import platform
import sys

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="cepton_alg",
        version="0.2.1",
        description="Cepton Python",
        long_description=open("README.md").read(),
        url="https://github.com/ceptontech/cepton_alg_redist",
        author="Cepton Technologies",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3",
        ],
        keywords="cepton",
        python_requires=">=3.3",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=[
            "cepton_sdk",
            "netifaces",
            "numpy",
            "parse",
            "pillow",
            "pynmea2",
            "pyserial",
            "scipy",
            "transforms3d",
            "imageio",
            "laspy",
            "matplotlib",
            "numpy_stl",
            "plyfile",
            "pyqt5",
            "seaborn",
            "uuid",
            "vispy",
        ],
        scripts=[
            "samples/cepton_alg_render",
            "samples/cepton_alg_viewer",
            "samples/common/cepton_sdk_viewer",
        ]
    )
