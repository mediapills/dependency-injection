Using the Container
===================

.. warning:: This Document Page Under Construction

This documentation describes the API of the **Container** object itself.

__setitem__
-----------

You can set entries directly on the container:

.. code-block::

   >>> from mediapills.dependency_injection import Container

   >>> di = Container()

   >>> di['key'] = 'value'

   >>> di['key']

   'value'


__getitem__
------------

You can get entries from the container:

.. code-block::

   >>> from mediapills.dependency_injection import Container

   >>> di = Container({"key": "value"})

   >>> di['key']

   'value'

   >>> di.get('key')

   'value'

   >>> di.get(None, 'default')

   'default'
