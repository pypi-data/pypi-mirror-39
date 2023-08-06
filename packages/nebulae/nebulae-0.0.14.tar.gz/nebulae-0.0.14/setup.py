#!/usr/bin/env python
'''
setup
Created by Seria at 04/11/2018 10:50 AM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nebulae",
    version="0.0.14",
    author="Seria",
    author_email="zzqsummerai@yeah.net",
    description="A novel and simple framework based on prevalent DL framework and other image processing libs."
                + "v0.0.14: unable to assemble DUPLICATE component without name is not allowed but passing existent name is allowed."
                + "v0.0.13: allow users to assemble DUPLICATE component without passing name; "
                + "add RESIZE component; "
                + "shorten automatically generated component names."
                + "v0.0.12: fix wrong implementation on data augmentation; "
                + "FuelGenerator will keep original image size if width or height is not given.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    install_requires=
    ['graphviz',
     'scikit-image',
     'h5py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)