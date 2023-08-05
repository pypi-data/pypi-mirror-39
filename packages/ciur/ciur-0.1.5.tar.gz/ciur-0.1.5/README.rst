====
Ciur
====

.. image:: ./docs/images/wooden-sieve-old-ancient-isolated-white-background.jpg
   :target: https://bitbucket.org/ada/python-ciur
   :alt: Ciur

..

    *Ciur is a scrapper layer in development*

    *Ciur is a lib because it has less black magic than a framework*


It exports all scrapper related code into separate layer.

If you are annoyed by
`Spaghetti code <https://en.wikipedia.org/wiki/Spaghetti_code>`_,
sql inside php and inline css inside html
THEN you also are annoyed by xpath/css code inside crawler.

Ciur gives the taste of `Lasagna code <http://c2.com/cgi/wiki?LasagnaCode>`_
generally by enforcing encapsulation for scrapping layer.

For more information visit the
`documentation <http://python-ciur.readthedocs.io/>`_.


Nutshell
========

Ciur uses own DSL, here is a small example of a ``example.org.ciur`` query:

.. code-block:: yaml

    root `/html/body` +1
        name `.//h1/text()` +1
        paragraph `.//p/text()` +1

This command

.. code-block :: bash

    $ ciur --url "http://example.org" --rule "example.org.ciur"

Will produce a json

.. code-block :: json

    {
        "root": {
            "name": "Example Domain",
            "paragraph": "This domain is established to be used for illustrative
                           examples in documents. You may use this
                           domain in examples without prior coordination or
                          asking for permission."
        }
    }

Installation
============

The recommendable way to install is via
`Python Virtual environment <docs/python_virtual_environment.rst>`_.

Ciur use MIT License
====================
This means that code may be included in proprietary code without any additional restrictions.

Please see `LICENSE <./LICENSE>`_.
