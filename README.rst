.. image:: https://api.codeclimate.com/v1/badges/31682a7859575a4f64b0/maintainability
    :target: https://codeclimate.com/github/mediapills/dependency-injection/maintainability
    :alt: Maintainability

.. image:: https://codecov.io/gh/mediapills/dependency-injection/branch/main/graph/badge.svg?token=USMBZ0W54N
    :target: https://codecov.io/gh/mediapills/dependency-injection
    :alt: Absolute coverage and coverage changes

.. image:: https://github.com/mediapills/dependency-injection/workflows/CI%20Build/badge.svg?branch=main
    :target: https://github.com/mediapills/dependency-injection/actions
    :alt: GitHub Workflow Actions Status

.. image:: https://pypip.in/py_versions/mediapills.dependency_injection/badge.svg
    :target: https://pypi.python.org/pypi/mediapills.dependency_injection
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/wheel/mediapills.dependency-injection.svg
    :target: https://pypi.python.org/pypi/mediapills.dependency_injection
    :alt: Wheel

.. image:: https://static.pepy.tech/personalized-badge/mediapills-dependency-injection?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads
    :target: https://pepy.tech/project/mediapills-dependency-injection
    :alt: Downloads

.. image:: https://requires.io/github/mediapills/dependency-injection/requirements.svg?branch=main
     :target: https://requires.io/github/mediapills/dependency-injection/requirements/?branch=main
     :alt: Requirements Status

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
     :target: https://github.com/mediapills/dependency-injection/blob/main/LICENSE.md
     :alt: License: MIT


Overview
--------

**Dependency Injection** is a technique in which an object receives other
objects that it depends on, called dependencies. Typically, the receiving
object is called a client and the passed-in ('injected') object is called a
service. The code that passes the service to the client is called the injector.
Instead of the client specifying which service it will use, the injector tells
the client what service to use. The 'injection' refers to the passing of a
dependency (a service) into the client that uses it.

Dependency injection solves the following problems:

* How can a class be independent of how the objects on which it depends are created?
* How can the way objects are created be specified in separate configuration files?
* How can an application support different configurations?

Creating objects directly within the class commits the class to particular
implementations. This makes it difficult to change the instantiation at
runtime, especially in compiled languages where changing the underlying objects
can require re-compiling the source code.

Dependency injection separates the creation of a client's dependencies from the
client's behavior, which promotes loosely coupled programs and the dependency
inversion and single responsibility principles. Fundamentally, dependency
injection is based on passing parameters to a method.

Dependency injection is an example of the more general concept of inversion of
control.

Roles
~~~~~

Dependency injection involves four roles:

* the service objects to be used
* the client object, whose behavior depends on the services it uses
* the interfaces that define how the client may use the services
* the injector, which constructs the services and injects them into the client

Any object that may be used can be considered a **service**. Any object that
uses other objects can be considered a **client**. The names relate only to the
role the objects play in an injection.

The **interfaces** are the types the client expects its dependencies to be. The
client should not know the specific implementation of its dependencies, only
know the interface's name and API. As a result, the client will not need to
change even if what is behind the interface changes. Dependency injection can
work with true interfaces or abstract classes, but also concrete services,
though this would violate the dependency inversion principle and sacrifice the
dynamic decoupling that enables testing. It is only required that the client
never treats its interfaces as concrete by constructing or extending them. If
the interface is refactored from a class to an interface type (or vice versa)
the client will need to be recompiled. This is significant if the client and
services are published separately.

The **injector** introduces services to the client. Often, it also constructs
the client. An injector may connect a complex object graph by treating the same
object as both a client at one point and as a service at another. The injector
itself may actually be many objects working together, but may not be the client
(as this would create a circular dependency). The injector may be referred to
as an assembler, provider, container, factory, builder, spring, or construction
code.

Pros
~~~~

A basic benefit of dependency injection is decreased coupling between classes
and their dependencies. By removing a client's knowledge of how its
dependencies are implemented, programs become more reusable, testable and
maintainable.

This also results in increased flexibility: a client may act on anything that
supports the intrinsic interface the client expects.

Many of dependency injection's benefits are particularly relevant to
unit-testing.

For example, dependency injection can be used to externalize a system's
configuration details into configuration files, allowing the system to be
reconfigured without recompilation. Separate configurations can be written for
different situations that require different implementations of components. This
includes testing. Similarly, because dependency injection does not require any
change in code behavior it can be applied to legacy code as a refactoring. The
result is clients that are more independent and that are easier to unit test in
isolation using stubs or mock objects that simulate other objects not under
test. This ease of testing is often the first benefit noticed when using
dependency injection.

More generally, dependency injection reduces boilerplate code, since all
dependency creation is handled by a singular component.

Finally, dependency injection allows concurrent development. Two developers can
independently develop classes that use each other, while only needing to know
the interface the classes will communicate through. Plugins are often developed
by third party shops that never even talk to the developers who created the
product that uses the plugins.

Cons
~~~~

Creates clients that demand configuration details, which can be onerous when
obvious defaults are available.

Make code difficult to trace because it separates behavior from construction.

Is typically implemented with reflection or dynamic programming. This canhinder
IDE automation.

Typically requires more upfront development effort.

Forces complexity out of classes and into the links between classes which might
be harder to manage.

Encourage dependence on a framework.

Installation
------------

Before using mediapills.dependency_injection in your project, add it to your ``requirements.txt``
file:

.. code-block:: bash

    $ echo "-e git+ssh://git@github.com/mediapills/dependency_injection.git@0.0.2#egg=mediapills.dependency_injection" >> requirements.txt

or

.. code-block:: bash

    $ echo "mediapills.dependency_injection==0.0.2" >> requirements.txt


Usage
-----

Creating a injector is a matter of creating a ``Injector`` instance:

.. code-block:: python

    from mediapills.dependency_injection import Injector

    injector = Injector()

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

By default, each time you get a service, Injector returns the **same instance**
of it. If you want a different instance to be returned for all calls, wrap your
anonymous function with the ``factory()`` method

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

    def session_storage_ext(storage: Callable, di: Injector):
        # Do something with base storage using di

        return storage

    injector.extend('session_storage', session_storage_ext)

The first argument is the name of the service to extend, the second a function
that gets access to the object instance and the container.

Fetching the Service Creation Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you access an object, Injector automatically calls the anonymous function
that you defined, which creates the service object for you. If you want to get
raw access to this function, you can use the ``raw()`` method:

.. code-block:: python

    injector['session'] = lambda di: (
        Session(di['session_storage'])
    )

    sessionFunction = container.raw('session')
