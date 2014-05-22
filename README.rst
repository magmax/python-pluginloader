==============  ===============  =========  ============
VERSION         DOWNLOADS        TESTS      COVERAGE
==============  ===============  =========  ============
|pip version|   |pip downloads|  |travis|   |coveralls|
==============  ===============  =========  ============

Goal and Philosophy
===================

**Pluginloader** is a library to allow an easy way to **load plugins**. They can be managed by interfaces or just method validators.

Features
--------

- Each plugin can be instanciated **several times**.
- **Customizable filter** to select if a class should be loaded as a plugin.
- **Sandboxed**: plugins cannot access the main program or other plugins by default, because they are loaded in isolated environments.


Documentation
=============

Installation
------------

Two options: to install it in your system/project::

    pip install pluginloader

Usage
-----

You can load all plugins in a file, just doing:

.. code:: python

    loader = PluginLoader()
    plugins = loader.load_file('plugins.py')

With those simple lines you will have in the variable :code:`plugins` a dictionary with each class inside the ``plugins.py`` file as key and a factory as value.

Let's see an example. Using the ``plugins.py`` file:

.. code:: python

    class Foo(object):
        pass

We can have an object of that class just with:

.. code:: python

    loader = PluginLoader()
    plugins = loader.load_file('plugins.py')
    instance1 = plugins['Foo']()
    instance2 = plugins['Foo']()

Simple and easy.

API
---

This is a simple module with a simple API. It just contains one class, :code:`PluginLoader`, with these public methods:

:code:`load_file(filename, onlyif=None)`
////////////////////////////////////////

Loads all plugins in a file.

Parameters:

- ``filename``: File name to be loaded.
- ``onlyif``: Value or function that will be called with each class found. It will skip the plugin if this function returns :code:`False`.


:code:`load_directory(path, onlyif=None, recursive=False))`
///////////////////////////////////////////////////////////

Loads all plugins in a directory.

Parameters:

- ``path``: Path where plugins are in.
- ``onlyif``: Value or function that will be called with each class found. It will skip the plugin if this function returns :code:`False`.
- ``recursive``: Boolean value to allow recursive read of directories.

Links will always be ignored.


License
=======

Copyright (c) 2014 Miguel Ángel García (`@magmax9`_).

Licensed under `the MIT license`_.


.. |travis| image:: https://travis-ci.org/magmax/python-pluginloader.png
  :target: `Travis`_
  :alt: Travis results

.. |coveralls| image:: https://coveralls.io/repos/magmax/python-pluginloader/badge.png
  :target: `Coveralls`_
  :alt: Coveralls results_

.. |pip version| image:: https://pypip.in/v/pluginloader/badge.png
    :target: https://pypi.python.org/pypi/pluginloader
    :alt: Latest PyPI version

.. |pip downloads| image:: https://pypip.in/d/pluginloader/badge.png
    :target: https://pypi.python.org/pypi/pluginloader
    :alt: Number of PyPI downloads

.. _Travis: https://travis-ci.org/magmax/python-pluginloader
.. _Coveralls: https://coveralls.io/r/magmax/python-pluginloader

.. _@magmax9: https://twitter.com/magmax9

.. _the MIT license: http://opensource.org/licenses/MIT
.. _download the lastest zip: https://pypi.python.org/pypi/pluginloader
