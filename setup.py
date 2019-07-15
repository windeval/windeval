"""Setup windeval."""

from setuptools import setup

setup(
    name="windeval",
    version="0.1.0",
    description="evaluate wind observations",
    packages=["windeval"],
    package_dir={"windeval": "windeval"},
    install_requires=["setuptools"],
    zip_safe=False,
)
