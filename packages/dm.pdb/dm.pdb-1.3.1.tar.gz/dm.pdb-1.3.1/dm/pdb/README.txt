Dieter Maurer's PDB extension.
==============================

``Pdb``, the Python debugger, has some limitations.
This extension tries to get rid of some of them.

Things done
-----------

 * setting breakpoints

   Allow *filename* to specify a module as well.

   Allow setting breakpoints from outside via ``do_break``.
   This is useful for debug setups.

 * exception display

   We store the exception in the ``Pdb`` instance.
   A new command ``exception`` (abbreviated ``e``) calls ``print_exception``
   on the stored exception value.


 * ``where`` command improvements

   - each frame identifies its level (the top frame is at level 0,
     the one below it at level 1, etc...)

   - the current frame is marked as such

   - ``where`` gets optional arguments *number* and *end*

     *number* controls how many frames are displayed (default: ``maxint``),
     *end* at what level the display ends, negative numbers count from
     the bottom (default: ``-1``, i.e. the bottom frame).

 * new command ``frame level`` (abbr: ``f``)

   switch to call frame at *level*

   without argument, provide info about current frame

 * allow to customize the display of the ``where`` command
   and of tracebacks
   e.g. to display additional debugging information as
   provided by Zope (for example).

   This can be done by customizing ``getAdditionalFrameInfo``.

Things not yet done
-------------------

 * Returning from ``debug`` occasionally returns to ``stop``
   rather than where we entered the recursive debugger.
   This is often nasty (and should be fixed)


zpdb
----

The module ``zpdb`` contains a debugger targeting Zope development. It displays
additional debug information often used for Zope development
(--> ``__traceback_info__``, ``__traceback_supplement__``). It depends
on the package ``zExceptions``.


Version history
---------------

1.3
,,,

 * Python 3 compatibility

1.2
,,,

 * fixed: ``do_break`` sometimes failed to resolve functions correctly.

1.1
,,,

 * improved handling of errors in command argument parsing

 * Python 2.6 compatibility


1.0.4
,,,,,

 * work around Python monkey patching ``set_trace`` inside a doctest.

1.0.3
,,,,,

 * fix ``debug`` to use the current ``Pdb`` class, not Python's.

1.0.2
,,,,,

 * let external calls to ``do_break`` work even after the first ``run``.
