Bio2BEL FamPlex |build|
=======================
Protein complex and family hierarchies from FamPlex.

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
``bio2bel_famplex`` can be installed easily from
`PyPI <https://pypi.python.org/pypi/bio2bel_famplex>`_
with the following code in your favorite terminal:

.. code-block:: sh

    $ python3 -m pip install bio2bel_famplex

or from the latest code on `GitHub <https://github.com/bio2bel/famplex>`_ with:

.. code-block:: sh

    $ python3 -m pip install git+https://github.com/bio2bel/famplex.git

Setup
-----
FamPlex can be downloaded and populated from either the
Python REPL or the automatically installed command line utility.

Python REPL
~~~~~~~~~~~
.. code-block:: python

    >>> import bio2bel_famplex
    >>> famplex_manager = bio2bel_famplex.Manager()
    >>> graph = famplex_manager.to_bel()

.. |build| image:: https://travis-ci.com/bio2bel/famplex.svg?branch=master
    :target: https://travis-ci.com/bio2bel/famplex
    :alt: Build Status

.. |documentation| image:: http://readthedocs.org/projects/bio2bel-famplex/badge/?version=latest
    :target: http://bio2bel.readthedocs.io/projects/famplex/en/latest/?badge=latest
    :alt: Documentation Status

.. |pypi_version| image:: https://img.shields.io/pypi/v/bio2bel_famplex.svg
    :alt: Current version on PyPI

.. |coverage| image:: https://codecov.io/gh/bio2bel/famplex/coverage.svg?branch=master
    :target: https://codecov.io/gh/bio2bel/famplex?branch=master
    :alt: Coverage Status

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/bio2bel_famplex.svg
    :alt: Stable Supported Python Versions

.. |pypi_license| image:: https://img.shields.io/pypi/l/bio2bel_famplex.svg
    :alt: MIT License
