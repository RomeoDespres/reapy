from setuptools import setup, find_packages
from os import path, walk, sep
from typing import Dict, List

here = path.abspath(path.dirname(__file__))

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


setup(name="python-reapy",
      version="0.4.2",
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
          'typing_extensions',
      ],
      python_requires=">=3.0")
