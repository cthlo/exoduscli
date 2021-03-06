exoduscli
==========

.. contents::

Summary
--------

exoduscli is a wrapped version of the XBMC addon, Exodus. It harnesses the power of Exodus by wrapping it with a fake/stubbed XBMC interface (``exoduscli/fakexbmc``).

This fake interface will not work on other XBMC addons because it is tailor-made for Exodus. Exodus and its dependencies are downloaded in the first run.

Installation and usage
-----------------------

pip
~~~~

.. code-block:: bash

    $ pip2 install --upgrade --user git+git://github.com/cthlo/exoduscli.git@master
    $ exoduscli
    Loading...
    _____________________
    [  0] << Exit
    [  1] Movies
    [  2] TV Shows
    [  3] Latest Movies
    [  4] Latest Episodes
    [  5] Search
    

``exoduscli.exe`` instead of ``exoduscli`` for Windows

From source
~~~~~~~~~~~~

.. code-block:: bash

    $ git clone https://github.com/cthlo/exoduscli
    $ cd exoduscli
    $ python2 -m exoduscli.main
    Loading...
    _____________________
    [  0] << Exit
    [  1] Movies
    [  2] TV Shows
    [  3] Latest Movies
    [  4] Latest Episodes
    [  5] Search
    

Requirements
-------------

* Python2 (>=2.6)
