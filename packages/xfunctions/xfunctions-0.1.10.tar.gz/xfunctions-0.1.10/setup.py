# coding:utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xfunctions",
    version="0.1.10",
    author="@neoctobers",
    author_email="neoctobers@gmail.com",
    description="Some useful functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neoctobers/xfunctions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)
