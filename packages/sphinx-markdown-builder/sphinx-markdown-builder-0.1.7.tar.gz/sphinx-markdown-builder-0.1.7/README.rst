sphinx-markdown-builder
=======================

|PyPI| |PyPI - Downloads| |PyPI - Python Version| |GitHub stars|

   sphinx builder that outputs markdown files

Please ★ this repo if you found it useful ★ ★ ★

If you want frontmatter support please use
`sphinx-jekyll-builder <https://github.com/codejamninja/sphinx-jekyll-builder>`__

Features
--------

-  Generates markdown

Installation
------------

.. code:: sh

   pip3 install sphinx-markdown-builder

Dependencies
------------

-  `Python 3 <https://www.python.org>`__

Usage
-----

Load extension in configuration.

*conf.py*

.. code:: py

   extensions = [
       'sphinx_markdown_builder'
   ]

If using `recommonmark <https://github.com/rtfd/recommonmark>`__, make
sure you explicitly ignore the build files as they will conflict with
the system.

*conf.py*

.. code:: py

   exclude_patterns = [
       'build/*'
   ]

Build markdown files with Makefile

.. code:: sh

   make markdown

Build markdown files with ``sphinx-build`` command

.. code:: sh

   cd docs
   sphinx-build -M markdown ./ build

Support
-------

Submit an
`issue <https://github.com/codejamninja/sphinx-markdown-builder/issues/new>`__

Screenshots
-----------

`Contribute <https://github.com/codejamninja/sphinx-markdown-builder/blob/master/CONTRIBUTING.md>`__
a screenshot

Contributing
------------

Review the `guidelines for
contributing <https://github.com/codejamninja/sphinx-markdown-builder/blob/master/CONTRIBUTING.md>`__

License
-------

`MIT
License <https://github.com/codejamninja/sphinx-markdown-builder/blob/master/LICENSE>`__

`Jam Risser <https://codejam.ninja>`__ © 2018

Changelog
---------

Review the
`changelog <https://github.com/codejamninja/sphinx-markdown-builder/blob/master/CHANGELOG.md>`__

Credits
-------

-  `Jam Risser <https://codejam.ninja>`__ - Author
-  `Matthew
   Brett <https://github.com/matthew-brett/nb2plots/blob/master/nb2plots/doctree2md.py>`__
   - doctree2md

Support on Liberapay
--------------------

A ridiculous amount of coffee ☕ ☕ ☕ was consumed in the process of
building this project.

`Add some fuel <https://liberapay.com/codejamninja/donate>`__ if you’d
like to keep me going!

|Liberapay receiving| |Liberapay patrons|

.. |PyPI| image:: https://img.shields.io/pypi/v/sphinx-markdown-builder.svg?style=flat-square
   :target: https://pypi.org/project/sphinx-markdown-builder
.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/sphinx-markdown-builder.svg?style=flat-square
   :target: https://pypi.org/project/sphinx-markdown-builder
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/sphinx-markdown-builder.svg?style=flat-square
   :target: https://pypi.org/project/sphinx-markdown-builder
.. |GitHub stars| image:: https://img.shields.io/github/stars/codejamninja/sphinx-markdown-builder.svg?style=flat-square&label=Stars
   :target: https://github.com/codejamninja/sphinx-markdown-builder
.. |Liberapay receiving| image:: https://img.shields.io/liberapay/receives/codejamninja.svg?style=flat-square
   :target: https://liberapay.com/codejamninja/donate
.. |Liberapay patrons| image:: https://img.shields.io/liberapay/patrons/codejamninja.svg?style=flat-square
   :target: https://liberapay.com/codejamninja/donate
