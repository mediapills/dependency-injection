Installation
~~~~~~~~~~~~

Before using mediapills.dicontainer in your project, add it to your ``requirements.txt``
file:

.. code-block:: bash

    $ echo "mediapills.dicontainer==0.0.1" >> requirements.txt

Usage
~~~~~

Creating a container is a matter of creating a ``Container`` instance:

.. code-block:: python

    from mediapills.dicontainer import Container

    container = Container()

As many other dependency injection containers, mediapills.dicontainer manages two
different kind of data: **services** and **parameters**.

Defining Services
~~~~~~~~~~~~~~~~~

A service is an object that does something as part of a larger system. Examples
of services: a database connection, a templating engine, or a mailer. Almost
any **global** object can be a service.

Services are defined by **anonymous functions** that return an instance of an
object:


.. code-block:: python

    // define some services
    container['session_storage'] = lambda c: Container (
        return SessionStorage('SESSION_ID')
    )

    container['session'] = lambda c: Container (
        return Session(c['session_storage'])
    )

Notice that the anonymous function has access to the current container
instance, allowing references to other services or parameters.

As objects are only created when you get them, the order of the definitions
does not matter.

Using the defined services is also very easy:

.. code-block:: php

    // get the session object
    session = container['session']

    // the above call is roughly equivalent to the following code:
    // storage = SessionStorage('SESSION_ID');
    // session = Session(storage);

Defining Factory Services
~~~~~~~~~~~~~~~~~~~~~~~~~

By default, each time you get a service, Pimple returns the **same instance**
of it. If you want a different instance to be returned for all calls, wrap your
anonymous function with the ``factory()`` method

.. code-block:: php

    container['session'] = container.factory(lambda c: Container (
        return Session(c['session_storage'])
    ))

Now, each call to ``container['session']`` returns a new instance of the
session.

Defining Parameters
~~~~~~~~~~~~~~~~~~~

Defining a parameter allows to ease the configuration of your container from
the outside and to store global values:

.. code-block:: php

    // define some parameters
    container['cookie_name'] = 'SESSION_ID';
    container['session_storage_cls'] = 'SessionStorage';

If you change the ``session_storage`` service definition like below:

.. code-block:: php

    container['session_storage'] = lambda c: Container (
        return c['session_storage_cls'](c['cookie_name']);
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

    container['random_func'] = container.protect(lambda: return rand())

Modifying Services after Definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases you may want to modify a service definition after it has been
defined. You can use the ``extend()`` method to define additional code to be
run on your service just after it is created:

.. code-block:: php

    container['session_storage'] = lambda c: Container (
        return c['session_storage_class'](c['cookie_name'])
    )

    container.extend('session_storage', lambda storage, c: Container (
        storage...()

        return storage
    ))

The first argument is the name of the service to extend, the second a function
that gets access to the object instance and the container.

Fetching the Service Creation Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you access an object, Pimple automatically calls the anonymous function
that you defined, which creates the service object for you. If you want to get
raw access to this function, you can use the ``raw()`` method:

.. code-block:: php

    container['session'] = lambda c: Container (
        return Session(c['session_storage'])
    )

    sessionFunction = container.raw('session')
