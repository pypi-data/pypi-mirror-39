Oanda REST-v20 API wrapper
==========================

|PyPI latest| |PyPI Version| |Coverage Status| |Travis Build Status| |Code Health| |PyPI License|

NOTE`: DO NOT USE THIS LIBRARY ON PRODUCTION!
It is under heavy development and still lacks testing suites. It is also partially documented.


OVERVIEW
--------

`OANDAPY <https://github.com/gustavooferreira/oandapy>`_ is a python3 wrapper for Oanda's REST API v20.
This library currently implements the features released under `version 3.0.1 <http://developer.oanda.com/rest-live-v20/release-notes/>`_ of OANDA's REST API.

Head over to `OANDA's REST API v20 docs <http://developer.oanda.com/rest-live-v20/introduction>`_ to go through their documentation.

Requirements
------------

This project requires:

    * Python 3.4 or earlier
    * git client
    * virtualenvwrapper/virtualenv for local development


Installation
------------

Right now, this library has not yet been pushed to pypi, so as of now you can't use pip to install it. (But will be soon in pypi)

.. code-block:: bash

    $ git clone git@github.com:gustavooferreira/oandapy.git
    $ cd oandapy
    $ python setup.py install

USAGE
-----

1. Create a account on `<https://www.oanda.com>`_ to get a API Access Token.
2. Import the oandapy module and create an instance with your access token:

.. code-block:: python

    from oandapy import APIv20
    from oandapy.exceptions import OandaError

    access_token = ""
    con = APIv20(environment="practice", access_token=access_token)

    try:
      result = con.account.get_accounts()

      for acc in result.accounts:
        print(acc.aid)
    except oanda.OandaError as exc:
      print(str(exc))



Contributing
------------

Please send pull requests, very much appreciated.


1. Fork the `repository <https://github.com/gustavooferreira/oandapy>`_ on GitHub.
2. Create a virtualenv.
3. Install requirements. ``pip install -r requirements-dev.txt``
4. Install pre-commit. ``pre-commit install``
5. Make a branch off of master and commit your changes to it.
6. Create a Pull Request with your contribution


NOTES
-----

* Oanda API REST-v20 is still under development, some functionality have not yet been implemented (Streaming, Pricing History, Forex Labs), but I will keep an eye on it, and as soon as it gets implemented I will update this library accordingly.
* Use this library at your own risk.
* Happy hunting on the markets!!


.. |Travis Build Status| image:: https://travis-ci.org/gustavooferreira/oandapy.svg?branch=master
   :target: https://travis-ci.org/gustavooferreira/oandapy.svg?branch=master
.. |Coverage Status| image:: https://coveralls.io/repos/github/gustavooferreira/oandapy/badge.svg?branch=master
    :target: https://coveralls.io/github/gustavooferreira/oandapy?branch=master
.. |Code Health| image:: https://landscape.io/github/gustavooferreira/oandapy/master/landscape.svg?style=flat
    :target: https://landscape.io/github/gustavooferreira/oandapy/master
.. |PyPI Version| image:: https://img.shields.io/pypi/pyversions/oandapy.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/oandapy
.. |PyPI License| image:: https://img.shields.io/pypi/l/oandapy.svg?maxAge=2592000
   :target: https://github.com/gustavooferreira/oandapy/blob/master/LICENCE
.. |PyPI latest| image:: https://img.shields.io/pypi/v/oandapy.svg?maxAge=360
   :target: https://pypi.python.org/pypi/oandapy
