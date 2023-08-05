=========
 CHANGES
=========

1.1.1 (2018-12-03)
==================

- Important bugfix for the new feature introduced in 1.1.0: Fall back to
  active site manager if no local site manager can be looked up for provided
  context.


1.1.0 (2018-11-30)
==================

- Ensure that a convtext is provided when looking up the vocabulary factory.

- Drop support for Python 2.6 and 3.3.

- Add support for Python 3.5, 3.6, 3.7, PyPy and PyPy3.


1.0.0 (2013-03-01)
==================

- Added support for Python 3.3.

- Replaced deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Dropped support for Python 2.4 and 2.5.

- Initial release independent of ``zope.app.schema``.
