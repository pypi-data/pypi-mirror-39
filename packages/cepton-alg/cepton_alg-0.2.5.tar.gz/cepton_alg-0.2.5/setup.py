#!/usr/bin/env python3

import platform
import sys

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="cepton_alg",
        version="0.2.5",
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
            "cepton_sdk>=1.9.2",
            "imageio",
            "laspy",
            "matplotlib",
            "netifaces",
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
        scripts=[
            "samples/cepton_alg_render",
            "samples/cepton_alg_viewer",
            "samples/common/cepton_sdk_viewer",
        ]
    )
