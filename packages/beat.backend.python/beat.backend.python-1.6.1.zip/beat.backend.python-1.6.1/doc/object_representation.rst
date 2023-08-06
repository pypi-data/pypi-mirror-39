.. _python-object-representation:

=======================
 Object Representation
=======================

As it is mentioned in `Algorithms`_ section, data is available via our
backend API to the user algorithms. For example, in Python, the |project|
platform uses NumPy data types to pass data to and from algorithms. For
example, when the algorithm reads data for which the format is defined like:

.. code-block:: javascript

   {
       "value": "float64"
   }


The field ``value`` of an instance named ``object`` of this format is
accessible as ``object.value`` and will have the type ``numpy.float64``. If the
format would be, instead:

.. code-block:: javascript

   {
       "value": [0, 0, "float64"]
   }


It would be accessed in the same way (i.e., via ``object.value``), except that
the type would be ``numpy.ndarray`` and ``object.value.dtype`` would be
``numpy.float64``. Naturally, objects which are instances of a format like
this:

.. code-block:: javascript

   {
       "x": "int32",
       "y": "int32"
   }


Could be accessed like ``object.x``, for the ``x`` value and ``object.y``, for
the ``y`` value. The type of ``object.x`` and ``object.y`` would be
``numpy.int32``.

Conversely, if you *write* output data in an algorithm, the type of the output
objects are checked for compatibility with respect to the value declared on the
format. For example, this would be a valid use of the format above, in Python:

.. code-block:: python

   import numpy

   class Algorithm:

       def process(self, inputs, dataloaders, outputs):

           # read data

           # prepares object to be written
           myobj = {"x": numpy.int32(4), "y": numpy.int32(6)}

           # write it
           outputs["point"].write(myobj) #OK!


If you try to write into an object that is supposed to be of type ``int32``, a
``float64`` object, an exception will be raised. For example:


.. code-block:: python

   import numpy

   class Algorithm:

       def process(self, inputs, dataloaders outputs):

           # read data

           # prepares object to be written
           myobj = {"x": numpy.int32(4), "y": numpy.float64(3.14)}

           # write it
           outputs["point"].write(myobj) #Error: cannot downcast!


The bottomline is: **all type casting in the platform must be explicit**. It
will not automatically downcast or upcast objects for you as to avoid
unexpected precision loss leading to errors.

.. include:: links.rst