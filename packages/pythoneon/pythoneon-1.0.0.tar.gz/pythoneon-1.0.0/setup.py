#-*-coding:utf-8-*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythoneon",
    version="1.0.0",
    author="René Bastian",
    author_email="rbastian@free.fr",
    description="compose electronic music",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.pythoneon.org",
    #packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+) ",
        "Operating System :: OS Independent",
    ],
)
