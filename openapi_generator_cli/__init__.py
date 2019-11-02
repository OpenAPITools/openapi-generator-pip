# coding=utf-8
# !/usr/bin/env python
import os
import subprocess
import sys


def run():
    arguments = ["java"]

    if os.getenv("JAVA_OPTS"):
        arguments.append(os.getenv("JAVA_OPTS"))

    arguments.append("-jar")

    jar_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "openapi-generator.jar"
    )
    arguments.append(jar_path)

    if len(sys.argv) > 1:
        arguments.extend(sys.argv[1:])

    subprocess.call(" ".join(arguments), shell=True)
