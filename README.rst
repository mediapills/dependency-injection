.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
     :target: https://github.com/mediapills/dependency-injection/blob/main/LICENSE.md
     :alt: License: MIT

.. image:: https://readthedocs.org/projects/dependency-injection/badge/?version=main
    :target: https://dependency-injection.readthedocs.io/en/main/?badge=main
    :alt: Documentation Status

.. image:: https://pypip.in/py_versions/mediapills.dependency_injection/badge.svg
    :target: https://pypi.python.org/pypi/mediapills.dependency_injection
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/wheel/mediapills.dependency-injection.svg
    :target: https://pypi.python.org/pypi/mediapills.dependency_injection
    :alt: Wheel

.. image:: https://static.pepy.tech/personalized-badge/mediapills-dependency-injection?period=month&units=international_system&left_color=gray&right_color=blue&left_text=Downloads
    :target: https://pepy.tech/project/mediapills-dependency-injection
    :alt: Downloads

.. image:: https://github.com/mediapills/dependency-injection/workflows/CI%20Build/badge.svg?branch=main
    :target: https://github.com/mediapills/dependency-injection/actions
    :alt: GitHub Workflow Actions Status

.. image:: https://api.codeclimate.com/v1/badges/31682a7859575a4f64b0/maintainability
    :target: https://codeclimate.com/github/mediapills/dependency-injection/maintainability
    :alt: Maintainability

.. image:: https://codecov.io/gh/mediapills/dependency-injection/branch/main/graph/badge.svg?token=USMBZ0W54N
    :target: https://codecov.io/gh/mediapills/dependency-injection
    :alt: Absolute coverage and coverage changes

.. image:: https://requires.io/github/mediapills/dependency-injection/requirements.svg?branch=main
     :target: https://requires.io/github/mediapills/dependency-injection/requirements/?branch=main
     :alt: Requirements Status

.. image:: https://bestpractices.coreinfrastructure.org/projects/5169/badge
     :target: https://bestpractices.coreinfrastructure.org/projects/5169
     :alt: CII Best Practices


Usage
-----

Creating a injector is a matter of creating a ``Container`` instance:

.. code-block:: python

    from mediapills.dependency_injection import Container

    injector = Container()

As many other dependency injection containers, mediapills.dependency_injection manages two
different kind of data: **services** and **parameters**.

Defining Services
~~~~~~~~~~~~~~~~~

A service is an object that does something as part of a larger system. Examples
of services: a database connection, a templating engine, or a mailer. Almost
any object can be a service.

Services are defined by **anonymous functions** that return an instance of an
object:

.. code-block:: python

    # define some services
    injector['session_storage'] = lambda di: (
        SessionStorage('SESSION_ID')
    )

    injector['session'] = lambda di: (
        Session(di['session_storage'])
    )

Notice that the anonymous function has access to the current injector
instance, allowing references to other services or parameters.

As objects are only created when you get them, the order of the definitions
does not matter.

Using the defined services is also very easy:

.. code-block:: python

    # get the session object
    session = injector['session']

    # the above call is roughly equivalent to the following code:
    # storage = SessionStorage('SESSION_ID')
    # session = Session(storage)

Defining Factory Services
~~~~~~~~~~~~~~~~~~~~~~~~~

By default, each time you get a service, ``Container`` returns the
**same instance** of it. If you want a different instance to be returned for
all calls, wrap your anonymous function with the ``factory()`` method

.. code-block:: python

    injector['session'] = injector.factory(lambda di: (
        Session(di['session_storage'])
    ))

Now, each call to ``injector['session']`` returns a new instance of the
session.

Defining Parameters
~~~~~~~~~~~~~~~~~~~

Defining a parameter allows to ease the configuration of your container from
the outside and to store global values:

.. code-block:: python

    # define some parameters
    injector['cookie_name'] = 'SESSION_ID'
    injector['session_storage_cls'] = SessionStorage

If you change the ``session_storage`` service definition like below:

.. code-block:: python

    injector['session_storage'] = lambda di: (
        di['session_storage_cls'](di['cookie_name'])
    )

You can now easily change the cookie name by overriding the
``cookie_name`` parameter instead of redefining the service
definition.

Protecting Parameters
~~~~~~~~~~~~~~~~~~~~~

Because Pimple sees anonymous functions as service definitions, you need to
wrap anonymous functions with the ``protect()`` method to store them as
parameters:

.. code-block:: php

    injector['random_func'] = lambda i: rand()
    injector.protect('random_func')

Modifying Services after Definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases you may want to modify a service definition after it has been
defined. You can use the ``extend()`` method to define additional code to be
run on your service just after it is created:

.. code-block:: python

    injector['session_storage'] = lambda di: (
        di['session_storage_class'](di['cookie_name'])
    )

    def session_storage_ext(storage: Callable, di: Container):
        # Do something with base storage using di

        return storage

    injector.extend('session_storage', session_storage_ext)

The first argument is the name of the service to extend, the second a function
that gets access to the object instance and the container.

Fetching the Service Creation Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you access an object, ``Container`` automatically calls the anonymous
function that you defined, which creates the service object for you. If you
want to get raw access to this function, you can use the ``raw()`` method:

.. code-block:: python

    injector['session'] = lambda di: (
        Session(di['session_storage'])
    )

    sessionFunction = container.raw('session')
