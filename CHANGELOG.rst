Changelog
=========

.. warning:: This Document Page Under Construction

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

v0.1.0 (2021-08-23)
-------------------

Minor release

Added
#####

- Added module :mod:`src.mediapills.dependency_injection.exceptions` class :class:`RecursionError`

- Added `codecov <https://app.codecov.io/gh/mediapills/dependency-injection>`_ integration

- Added badges: `requires.io <https://requires.io/github/mediapills/dependency-injection/requirements>`_, `codecov <https://app.codecov.io/gh/mediapills/dependency-injection>`_, `actions <https://github.com/mediapills/dependency-injection/actions>`_, `py_versions <https://pypi.org/project/mediapills.dependency-injection/>`_, `license <https://github.com/mediapills/dependency-injection/blob/main/LICENSE.md>`_, `downloads <https://pepy.tech/project/mediapills-dependency-injection>`_, `wheel <https://pypi.org/project/mediapills.dependency-injection/>`_ and `codeclimate <https://codeclimate.com/github/mediapills/dependency-injection>`_

- Added files: ``LICENSE.md`` and ``CONTRIBUTING.md``

- Added **classifiers** and **project_urls** sections in file ``setup.cfg``

- Added `py36`, `py37` and `py39` into section **envlist** in ``tox.ini`` file

Other
#####

- Changed **mypy**, **pytest-cov** and **build** modules version

- Changed ``README.rst``

- Changed value in **python_requires** section in ``setup.cfg`` file from `3.8` to `3.5`

- Changed ``code-analysis.yml`` workflow file

v0.0.2 (2021-08-22)
-------------------

Patch release

Added
#####

- Created decorator :func:`handle_unknown_identifier`

- Created module :mod:`mediapills.dependency_injection` class :class:`Container` methods: :meth:`__getitem__`, :meth:`__setitem__`, :meth:`values`, :meth:`items`, :meth:`copy`, :meth:`update` and :meth:`protect`

- Created :class:`TestInjector` unit test case

Other
#####

- Changed module :mod:`mediapills.dependency_injection` class name from :class:`Container` to :class:`Injector`

- Changed name from :class:`TestContainer` to :class:`TestContainerBase` unit test case

v0.0.1 (2021-08-21)
-------------------

Minor release

Added
#####

- Created ``.coveragerc`` file specifies python `coverage <https://coverage.readthedocs.io>`_ configuration

- Created ``.gitignore`` file specifies intentionally untracked files

- Created ``.pre-commit-config.yaml`` file specifies `pre-commit <https://pre-commit.com/>`_ configuration

- Created `Makefile` the make utility

- Created `pyrightconfig.json` the `Pyright <https://github.com/microsoft/pyright>`_ flexible configuration

- Created python package builder ``setup.py`` and ``setup.cfg``

- Created module :mod:`mediapills.dependency_injection` class :class:`Container`

- Created module :mod:`src.mediapills.dependency_injection.exceptions` classes: :class:`BaseContainerException`, :class:`ExpectedInvokableException`, :class:`FrozenServiceException`, :class:`InvalidServiceIdentifierException`, :class:`UnknownIdentifierException` and :class:`RecursionInfiniteLoopError`

- Created unit tests case :class:`TestContainer`

- Created `virtualenv <https://virtualenv.pypa.io/en/latest/>`_ management file ``tox.ini``
