Definitions
===========

.. warning:: This Document Page Under Construction

Lazy Loading
------------

**Lazy loading** (also known as `asynchronous loading`) is a **design pattern**
commonly used in computer programming and mostly in web design and development
to defer initialization of an object until the point at which it is needed. It
can contribute to efficiency in the program's operation if properly and
appropriately used.


:class:`Container` loads the definitions you have written and uses them like
instructions on how to create objects.

However those objects are only created when/if they are requested from the
:class:`Container`, for example through `container.get(…)` or when they need to
be injected in another object. That means you can have a large amount of
definitions, :class:`Container` will not create all the objects unless asked
to.

Definition types
----------------

This definition format is the most powerful of all. There are several kind of entries you can define:

- :ref:`scalars`

- :ref:`generic container type objects`

- :ref:`objects`

- :ref:`aliases`

- :ref:`environment variables`

- :ref:`string expressions`

- :ref:`arrays`

.. _scalars:

Scalars
******

Scalars are simple Python values:

.. code-block::

   >>> from mediapills.dependency_injection import Container

   >>> di = Container({
   ...   'database.driver': 'mysql',
   ...   'database.host': '127.0.0.1',
   ...   'database.port': 80,
   ...   'database.auth': False,
   ...   'database.user': 'root',
   ... })

   >>> di['database.host']

   '127.0.0.1'

You can also define object entries by creating them directly:

.. code-block::

   >>> from mediapills.dependency_injection import Container

   >>> di = Container()

   >>> di['key'] = 'value'

   >>> di['key']

   'value'

However this is **not recommended** as that object will be created for every
entry invocation, even if not used (it will not be lazy loaded like explained
at this section).

.. _generic container type objects:

Generic Container Type Objects
******************************

:class:`Container` supports any object that holds an arbitrary number of other
objects. `Examples` of containers include **tuple**, **list**, **set**,
**dict**; these are the built-in containers.

.. code-block::

   >>> from mediapills.dependency_injection import Container

   >>> di = Container()

   >>> di['parameters'] = {
   ...   'database.host': '127.0.0.1',
   ...   'database.port': '80',
   ...   'database.user': 'root',
   ... }

   >>> di['parameters']

   {'database.host': '127.0.0.1', 'database.port': '80', 'database.user': 'root'}

.. _factories:

Factories
*********

.. warning:: This Page Section Under Construction

.. _objects:

Objects
*******

Services are defined by **anonymous functions** that return an instance of an
object:

.. code-block:: python

    # define some services
    container['session_storage'] = lambda di: (
        SessionStorage('SESSION_ID')
    )

    container['session'] = lambda di: (
        Session(di['session_storage'])
    )

**Notice** that the anonymous function has access to the current container
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

.. _autowired objects:

Autowired Objects
*****************

.. warning:: This Page Section Under Construction

.. _aliases:

Aliases
*******

You can alias an entry to another using the :class:`Container`:

.. code-block:: python

    # define arguments container
    container['arguments'] = lambda _: sys.argv

    # define arguments container alias with name properties
    container['properties'] = lambda di: di['arguments']

Allows the interface of an existing location to be used as another name.

.. _environment variables:

Environment Variables
*********************

You can get an environment variable's value using the :class:`Container`:

.. code-block:: python

    >>> container['env'] = lambda _: os.environ

    >>> di['env'].get("LANGUAGE")

    'en_US'

.. _string expressions:

String Expressions
******************

.. warning:: This Page Section Under Construction

.. _wildcards:

Wildcards
*********

.. warning:: This Page Section Under Construction
