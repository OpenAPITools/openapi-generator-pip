# coding=utf-8
# !/usr/bin/env python
import os
import subprocess
import sys


def run(args=None):
    arguments = ["java"]

    if os.getenv("JAVA_OPTS"):
        arguments.append(os.getenv("JAVA_OPTS"))

    arguments.append("-jar")

    jar_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "openapi-generator.jar"
    )
    arguments.append(jar_path)

    if args and type(args) == list:
        arguments.extend(args)

    subprocess.call(" ".join(arguments), shell=True)


def cli():
    args = []
    if len(sys.argv) > 1:
        args = sys.argv[1:]
    run(args)


if __name__ == "__main__":
    cli()
