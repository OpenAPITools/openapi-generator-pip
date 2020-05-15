# coding=utf-8
import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

NAME = "openapi-generator-cli"
DESCRIPTION = "CLI for openapi generator"
URL = "https://github.com/OpenAPITools/openapi-generator"
EMAIL = "team@openapitools.org"
AUTHOR = "OpenAPI Generator community"
VERSION = open("version").read()
EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


class UploadCommand(Command):
    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=["openapi_generator_cli"],
    extras_require=EXTRAS,
    package_data={"openapi_generator_cli": ["*.jar"]},
    include_package_data=True,
    license="APACHE 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    cmdclass={"upload": UploadCommand},
    entry_points={"console_scripts": ["openapi-generator=openapi_generator_cli:run"]},
)
