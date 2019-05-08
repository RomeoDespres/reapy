from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as f:
    long_description = f.read()

setup(
    name="python-reapy",
    version="0.3.0",
    description="A pythonic wrapper for REAPER's ReaScript Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Roméo Després",
    author_email="mail.reapy@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    keywords="REAPER DAW ReaScript API wrapper music audio",
    packages=find_packages(exclude=["docs"]),
    python_requires=">=3.0"
)
