from setuptools import setup, find_packages
from os import getenv

setup(
    name="dotpup",
    version=getenv("DOTPUP_VERSION", "1.0.0"),
    packages=find_packages(),
    license="MIT",
    long_description=open("README.md").read(),
    entry_points={
        "console_scripts": ["dpup=dotpup.cli:cli"],
    })
