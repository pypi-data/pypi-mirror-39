import setuptools
from pathlib import Path

setuptools.setup(
    name="profemzyutils",
    version=1.0,
    long_descriptions=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", ])
)
