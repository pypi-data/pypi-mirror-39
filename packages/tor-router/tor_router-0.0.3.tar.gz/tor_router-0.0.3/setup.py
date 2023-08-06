# coding: utf-8

import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tor_router",
    version="0.0.3",
    author="Whales Zhong",
    author_email="whaleszhong@gmail.com",
    description="make routing similar to flask blueprint",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/whales2018/Tornado_Router",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
