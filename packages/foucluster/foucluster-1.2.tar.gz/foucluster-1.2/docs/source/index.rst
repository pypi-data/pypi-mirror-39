.. foucluster documentation master file, created by
   sphinx-quickstart on Mon Oct  8 12:37:09 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FouCluster's documentation!
======================================

.. image:: https://travis-ci.org/cperales/foucluster.svg?branch=master
   :target: https://travis-ci.org/cperales/foucluster

.. image:: https://coveralls.io/repos/github/cperales/foucluster/badge.svg?branch=master
   :target: https://coveralls.io/github/cperales/foucluster?branch=master


Motivation
-----------
Recommendation song systems nowadays, like Spotify,
use song clustering by made up parameters such as
danceability, energy, instrumentalness, ... etc,
which need an expert in that area to create those parameters.

In order to avoid expert knowledge and make access to machine learning
applied to song easier, this library use signal analysis for measuring
distances between songs. Because musical notes have associated frequencies,
this proposal is based on transforming from time series to frequency
series, and then grouping theses series using various techniques and
distance metrics.

Use
----

The process to do the clustering can be divided in different steps


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   transform
   distance
   cluster

An example is explained in

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   example

It is also necessary install `mpg123` or `ffmpeg` for MP3 to WAV
transform. For Ubuntu, it is as easy as

.. code-block:: bash

    sudo apt install mpg123



Indices and tables
==================

* :ref:`genindex`
