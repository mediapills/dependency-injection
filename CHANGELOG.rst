=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

v0.1.0 (2021-08-23)
===================

Minor release

Added
-----

- Added :class:`RecursionError` handler
- Added ``codecov`` integration
- Added badges: ``requires.io``, ``codecov``, ``actions``, ``py_versions``, ``license``, ``downloads``, `wheel` and ``codeclimate``
- Added files: ``LICENSE.md`` and ``CONTRIBUTING.md``
- Added **classifiers** and **project_urls** sections in file ``setup.cfg``
- Added **py36**, **py37** and **py39** into section ``envlist`` in ``tox.ini`` file

Other
-----

- Changed ``mypy``, ``pytest-cov`` and ``build`` modules version
- Changed ``README.rst``
- Changed value in **python_requires** section in ``setup.cfg`` file from ``3.8`` to ``3.5``
- Change **code-analysis.yml** workflow file

v0.0.2 (2021-08-22)
===================

Patch release

Added
-----

- Created **handle_unknown_identifier** decorator
- Created  :class:`Container` methods ``__getitem__``, ``values``, ``items``, ``copy``, ``update``, ``protect``, ``factory`` and ``extend``
- Created :class:`TestInjector` unit test case

Other
-----

- Changed class name from :class:`Container` to :class:`Injector`
- Changed name unit test case name from :class:`TestContainer` to :class:`TestContainerBase`


v0.0.1 (2021-08-21)
===================

Minor release

Added
-----

- Created **.coveragerc** file specifies python coverage configuration
- Created **.gitignore** file specifies intentionally untracked files
- Created **.pre-commit-config.yaml**  file specifies ``pre-commit`` configuration
- Created **Makefile** the make utility
- Created **pyrightconfig.json** the ``Pyright`` flexible configuration
- Created python package builder **setup.py** and **setup.cfg**
- Created :class:`Container`
- Created package ``exceptions`` classes: :class:`BaseContainerException`, :class:`ExpectedInvokableException`, :class:`FrozenServiceException`, :class:`InvalidServiceIdentifierException`, :class:`UnknownIdentifierException` and :class:`RecursionInfiniteLoopError`
- Created :class:`TestContainer` unit tests case
- Created virtualenv management file **tox.ini**
