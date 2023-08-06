Spellchecker based on Malayalam morphology analyser
===================================================


.. image:: https://img.shields.io/pypi/v/mlmorph-spellchecker.svg
    :target: https://pypi.python.org/pypi/mlmorph-spellchecker
    :alt: PyPI Version




This is a Spellchcker for Malayalam language based on `Malayalam morphology analyser - mlmorph`_.

Installation
------------

Python 3 is required. Using with `venv`_ is recommended

  .. code-block:: console

    $ pip install mlmorph_spellchecker

Usage
-----

  .. code-block:: python

    from mlmorph import Analyser
    from mlmorph_spellchecker import spellcheck, getSuggestions
    analyser = Analyser()
    if spellcheck(word, analyser) is True:
        print('%s ✔️' % (word))
    else:
        print('%s ❌ Suggestions: %s' % (word, getSuggestions(word, analyser)))

Command line interface
----------------------

  .. code-block:: console

    $ python -m mlmorph_spellchecker --help
    usage: __main__.py [-h] word

    positional arguments:
    word        word to spellcheck

    optional arguments:
    -h, --help  show this help message and exit

.. _`Malayalam morphology analyser - mlmorph`: https://gitlab.com/smc/mlmorph
.. _`venv`: https://docs.python.org/3/library/venv.html
