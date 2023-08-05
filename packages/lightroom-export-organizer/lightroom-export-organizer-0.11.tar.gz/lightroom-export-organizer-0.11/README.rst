.. -*- mode: rst -*-

|Travis|_ |PyPi|_ |TestStatus|_ |PythonVersion|_

.. |Travis| image:: https://travis-ci.org/aagnone3/lightroom-export-organizer.svg?branch=master
.. _Travis: https://travis-ci.org/aagnone3/lightroom-export-organizer

.. |PyPi| image:: https://badge.fury.io/py/lightroom-export-organizer.svg
.. _PyPi: https://badge.fury.io/py/lightroom-export-organizer

.. |TestStatus| image:: https://travis-ci.org/aagnone3/lightroom-export-organizer.svg
.. _TestStatus: https://travis-ci.org/aagnone3/lightroom-export-organizer.svg

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/lightroom-export-organizer.svg
.. _PythonVersion: https://img.shields.io/pypi/pyversions/lightroom-export-organizer.svg

lightroom-export-organizer
================

- Unit testing with pytest
- Continuous integration testing with Travis CI
- Packaging and publishing to PyPi
- Documentation with Sphinx and Github Pages

Documentation
-------------

Documentation can be found at the github pages here_

.. _here: https://aagnone3.github.io/lightroom-export-organizer/

Dependencies
~~~~~~~~~~~~

lightroom-export-organizer is tested to work under Python 3.x.
See the requirements via the following command:

.. code-block:: bash

  cat requirements.txt

Installation
~~~~~~~~~~~~

lightroom-export-organizer is currently available on the PyPi's repository and you can
install it via `pip`:

.. code-block:: bash

  pip install -U lightroom-export-organizer

If you prefer, you can clone it and run the setup.py file. Use the following
commands to get a copy from GitHub and install all dependencies:

.. code-block:: bash

  git clone https://github.com/aagnone3/lightroom-export-organizer.git
  cd lightroom-export-organizer
  pip install .

Or install using pip and GitHub:

.. code-block:: bash

  pip install -U git+https://github.com/aagnone3/lightroom-export-organizer.git

Testing
~~~~~~~

.. code-block:: bash

  make test
  
