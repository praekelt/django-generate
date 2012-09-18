Changelog
=========

0.0.6
-----
#. Use ``_default_manager`` instead of ``objects`` manager to allow for overrides.

0.0.5
-----
#. Only pass fields that support an exact lookup to get_or_create.

0.0.4
-----
#. Use `exists` optimisation.
#. Force commit on every execution of method since settings may specify a transaction managed database layer.
#. Prevent redundant calls to save().
#. Support direct assignment of foreign key ids.


0.0.3 (2011-08-12)
------------------
#. Corrected manifest.

0.0.2 (2011-07-26)
------------------
#. Docs.

0.0.1
-----
#. Initial release.

