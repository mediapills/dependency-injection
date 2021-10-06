# Copyright The Mediapills Dependency Injection Authors.
# SPDX-License-Identifier: MIT
import setuptools
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements

version = "0.1.1"

requirements = parse_requirements("requirements.txt", session=PipSession())

install_requires = [str(requirement.req) for requirement in requirements]  # type: ignore

setuptools.setup(version=version, install_requires=install_requires)
