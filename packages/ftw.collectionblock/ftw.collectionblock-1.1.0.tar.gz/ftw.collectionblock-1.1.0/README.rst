ftw.collectionblock
###################

This package is an addon for `ftw.simplelayout <http://github.com/4teamwork/ftw.simplelayout>`_. Please make sure you
already installed ``ftw.simplelayout`` on your plone site before installing this addon.

``ftw.collectionblock`` works exactly the same way as a Plone Collection, since it uses the same ICollection behavior.

The differences:

1. The collection block is shown as a Block with a simplified default view.
2. Only one detail view the `listing_view` is implemented. If you need more it's on you :-)
3. RSS is enabled by default, it just needs to be enabled globally, since it respects the ISyndication settings.
4. The collectionblock has its own permission


Development
===========

**Python:**

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python boostrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- GitHub: https://github.com/4teamwork/ftw.collectionblock
- Issues: https://github.com/4teamwork/ftw.collectionblock/issues
- PyPI: http://pypi.python.org/pypi/ftw.collectionblock
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.collectionblock


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.collectionblock`` is licensed under GNU General Public License, version 2.
