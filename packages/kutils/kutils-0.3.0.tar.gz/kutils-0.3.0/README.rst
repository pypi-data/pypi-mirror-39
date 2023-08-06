kutils
======

Kyle's utilities.

These are various data structures and tools that I think are useful and
want to re-use across projects.

A Makefile is supplied to simplify certain tasks. This is aimed to
support *the author's* workflow, and may not be as useful to other
people.

+ ``build``: create a source distribution.
+ ``clean``: remove caches, compiled bytecode, build artifacts, and
  any generated documentation.
+ ``docs``: generate docs; if the ``DOCS`` variable isn't set, it defaults
  to generating HTML docs.
+ ``lint``: run pylint on ``$(LINTMOD)``, which should be the main project
  module.
+ ``setup``: use pip to install the project requirements.
+ ``test``: run pytest on the ``tests`` module.
+ ``viewdocs``: run ``$(SRVMOD)`` (which defaults to ``http.server``) on the
  HTML Sphinx documentation.
