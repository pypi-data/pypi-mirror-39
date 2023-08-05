import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()

# Package version
VERSION = "0.4.0"


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this library: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="jupygit",
    url="https://github.com/fferegrino/jupygit",
    author="Antonio Feregrino",
    author_email="antonio.feregrino@gmail.com",
    version=VERSION,
    description="Prepare your Notebooks to be pushed to Git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
