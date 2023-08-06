News
====

.. _release4.5:

4.5
---
* ``ctx`` parameter can be safely used in .decode() and won't be muted
* PP nametuple contains reference to the ASN1Obj itself
* ``colonize_hex`` function useful for pretty printing
* Integer values are also pretty printed in hexadecimal form

.. _release4.4:

4.4
---
* All errors are inherited from ASN1Error class
* NumericString/PrintableString has ``allowable_chars`` property holding
  all allowed characters

.. _release4.3:

4.3
---
* Fix NumericString: space is allowed character
* Strict PrintableString sanitizing

.. _release4.2:

4.2
---
* Removed ``lenindef``, ``ber_encoded`` attributes from the Choice --
  they must be taken from underlying value, as Choice does not have its
  own encoding
* Do not yield extra EOC PP for Any, having indefinite length encoding
  and containing autodecoded DEFINED BY value

.. _release4.1:

4.1
---
* ``bered`` attribute, meaning if object has BER-specific encoding, is
  renamed to ``ber_encoded``
* ``bered`` attribute is replace with property showing if any of
  underlying values are BER-encoded. If value has length indefinite
  encoded explicit tag, value, if value contains BER-related encoding,
  or if it contains other objects that are ``bered``, then it is ``bered``

.. _release4.0:

4.0
---
* Default value is checked also for Sets, not for Sequences only
* **Incompatible** change: defaulted values in Sequence/Set are always
  strictly checked, unless ``allow_default_values`` context option is
  set. ``strict_default_existence`` option disappeared
* Strict Set/Set Of's values ordering check

.. _release3.14:

3.14
----
* Additional encoding validness check: explicit tag must contain exactly
  one object inside. Throw DecodeError otherwise
* ``allow_expl_oob`` context and command-line options allow skipping of
  that check

.. _release3.13:

3.13
----
* DecodeError's decode paths are separated with ``:``, instead of ``.``,
  because of colliding with dots in OIDs
* Ability to print element decode paths with ``--print-decode-path``
  command line option (and corresponding keyword argument)
* Ability to print tree's branch specified with ``--decode-path-only``

.. _release3.12:

3.12
----
* Fix possible uncaught TypeError in Py2 with zero bytes inside the value
* Fix SequenceOf/SetOf raising BoundsError instead of DecodeError

.. _release3.11:

3.11
----
* Fix uncaught UTCTime/GeneralizedTime decode error when dealing with
  non ASCII-encoded values

.. _release3.10:

3.10
----
* Fix long-standing bug with explicitly tagged objects inside the
  Choice. If Choice had explicitly tagged value, then its ``.tlvlen``
  reports the size without taking value's explicit tag in advance
* Add ``.fulllen`` and ``.fulloffset`` properties for all objects

.. _release3.9:

3.9
---
* SEQUENCE's values are printed with field's name. Previously there was
  the following output::

    AlgorithmIdentifier SEQUENCE[OBJECT IDENTIFIER 1.3.14.3.2.26, [UNIV 5] ANY 0500 OPTIONAL]

  now it is::

    AlgorithmIdentifier SEQUENCE[algorithm: OBJECT IDENTIFIER 1.3.14.3.2.26; parameters: [UNIV 5] ANY 0500 OPTIONAL]
* Fixed EOC (Unicode character) repr printing issues under Python2

.. _release3.8:

3.8
---
BER's EOC is explicitly shown during pprinting. Following notation::

      15-2 [0,0,1576]-4  . content: [0] EXPLICIT [UNIV 16] ANY

is replaced with::

      15-2∞ [0,0,1576]∞  . content: [0] EXPLICIT [UNIV 16] ANY
    [...]
    1587    [1,1,   0]   . content:  BER EOC
    1589    [1,1,   0]   . content: EXPLICIT BER EOC

.. _release3.7:

3.7
---
* BER decoding support
* BitString's ''H notation support
* ``termcolor`` package is included in the tarball

.. _release3.6:

3.6
---
* Ability to set values during Sequence initialization

.. _release3.5:

3.5
---
* Fix TagMismatch exception completeness during Choice and Set decoding.
  Previously we will loose offset and decode_path information about
  concrete TagMismatched entity

.. _release3.4:

3.4
---
* Strict NumericString's value sanitation
* Invalid encoding in string types will raise ``DecodeError`` exception,
  instead of ``Unicode*Error``
* Fixed DecodePathDefBy workability with Python 2.x

.. _release3.3:

3.3
---
* Fix nasty BitString decoding bug: it could fail when data follows
  encoded BitString value. There weren't any problems when BitString is
  at the end of Sequence

.. _release3.2:

3.2
---
* Slightly corrected colours, now visible on white background

.. _release3.1:

3.1
---
* Fix bug related to DecodeError showing with DecodePathDefBy entities
* Respect ``NO_COLOR`` environment variable

.. _release3.0:

3.0
---
* :py:func:`pyderasn.decode_path_defby` is replaced with
  :py:class:`pyderasn.DecodePathDefBy`
* Ability to turn colourized terminal output by calling
  ``pprint(..., with_colours=True)``. You will need
  `termcolor package <https://pypi.org/project/termcolor/>`__

.. _release2.1:

2.1
---
* Fixed invalid offset calculation when dealing with DEFINED BY objects
  having explicit tags

.. _release2.0:

2.0
---
* BIT STRINGs can also be :ref:`DEFINED BY <definedby>`
* Decoding process can be governed with optional :ref:`ctx <ctx>`
  keyword argument to ``decode()`` method
* :ref:`defines_by_path <defines_by_path_ctx>` option is now
  :ref:`decode context <ctx>` option, not a keyword argument
* Ability to do ``strict validation``
  of defaulted values met in sequence, raising an exception

.. _release1.6:

1.6
---
Ability to skip specified number of bytes (``--skip``) in command line
utility.

.. _release1.5:

1.5
---
* Generic decoder's scheme and pretty printer
  (:py:func:`pyderasn.generic_decoder`) can be used in libraries
* Ability to specify :ref:`defines_by_path <defines_by_path_ctx>`
  during command line invocation

.. _release1.4:

1.4
---
Ability to automatically decode :ref:`DEFINED BY <definedby>` fields
inside SEQUENCEs.

.. _release1.3:

1.3
---
Removed ``__lt__``/``__eq__`` from base class, as pylint likes it.

.. _release1.2:

1.2
---
Full rich comparison operators added.


.. _release1.1:

1.1
---
Trivial README addition.

.. _release1.0:

1.0
---
Initial release.
