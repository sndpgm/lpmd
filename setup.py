import codecs
import os

from setuptools import find_packages, setup

PACKAGE = "lpmd"
README = "README.md"
REQUIREMENTS = "requirements.txt"

VERSION = "0.0.0"


def read(fname):
    """
    Read specified file as utf-8 in py3 to avoid to be bytes.

    Parameters
    ----------
    fname : str
        String expressing file name.

    """
    return codecs.open(
        os.path.join(os.path.dirname(__file__), fname), encoding="utf-8"
    ).read()


setup(
    name=PACKAGE,
    version=VERSION,
    description="lpmd: Livestock Product Marketing Data for Japan",
    long_description=read(README),
    author="sndpgm",
    url="https://lpmd.readthedocs.io/en/latest",
    packages=find_packages(),
    install_requires=list(read(REQUIREMENTS).splitlines()),
    include_package_data=True,
    python_requires=">=3.9",
)
