# -*- coding:utf-8 -*-

import setuptools


setuptools.setup(
    name="redis_kits",
    version="0.0.1",
    author="claydodo and his little friends (xiao huo ban)",
    author_email="claydodo@foxmail.com",
    description="Toolkits built upon Redis",
    url="https://github.com/claydodo/redis_kits",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2.7 ",
        "Programming Language :: Python :: 3 ",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        "redis>=3"
    ]
)
