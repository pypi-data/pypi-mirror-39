
.. :changelog:

Changelog
---------

0.9 (2018-11-28)
++++++++++++++++

- Enforce ``I`` noun with non callable attributes in the story
  definition.
- ``Context`` is passed as an argument into story step methods.
- Pass real class instances into step method.
- Show story execution path in the ``Context`` representation.
- Add Sentry, Py.test and Django Debug Toolbar plugins with
  ``Context`` reporter built in.
- Raise an exception on ``Failure`` when the story was called
  directly.
- Support iterable protocol in the ``Context`` class.
- Add ``Failure`` reason.
- Fix ``Skip`` result behavior in deeper sub-story hierarchy.

0.8 (2018-05-12)
++++++++++++++++

- Add ``dir()`` and ``repr()`` support to the context class.
- Failed result holds a link to the context.

0.7 (2018-05-06)
++++++++++++++++

- Add ``run`` interface to the story.

0.6 (2018-04-19)
++++++++++++++++

- Representation methods for story, context and point result classes.
- Python 2 support.

0.5 (2018-04-07)
++++++++++++++++

- Do not execute nested stories of the skipped story.

0.4 (2018-04-07)
++++++++++++++++

- Package was rewritten with linearization algorithm.
- ``Skip`` result was added to finish nested stories without finish
  the caller.

0.0.3 (2018-04-06)
++++++++++++++++++

- Nested stories support.

0.0.2 (2018-04-03)
++++++++++++++++++

- Fix class and instance attribute access.
- Validate return values.
- Make context append only.

0.0.1 (2018-04-02)
++++++++++++++++++

- Initial release.
