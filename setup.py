from setuptools import setup, find_packages
from os import path, walk, sep
from typing import Dict, List
import re


here = path.abspath(path.dirname(__file__))


def read_version() -> str:
    # Read the version without importing reapy, whose runtime dependencies
    # (e.g. psutil) are not installed in isolated build environments.
    with open(path.join(here, "reapy", "__init__.py")) as f:
        match = re.search(
            r"^__version__ = [\"']([^\"']+)[\"']", f.read(), re.M
        )
    if match is None:
        raise RuntimeError("Unable to find reapy.__version__")
    return match.group(1)


with open(path.join(here, "README.md")) as f:
    long_description = f.read()


def find_stubs(package: str) -> Dict[str, List[str]]:
    stubs = []
    for root, dirs, files in walk(package):
        for file in files:
            r_path = path.join(root, file).replace(package + sep, '', 1)
            stubs.append(r_path)
    stubs.append('py.typed')
    return {package: stubs}


setup(
    name="python-reapy",
    version=read_version(),
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
    package_data=find_stubs('reapy'),
    install_requires=[
        'psutil',
        'typing_extensions'
    ],
    python_requires=">=3.0"
)
