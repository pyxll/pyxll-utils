Resize array formula
====================

The macro 'resize_array_formula' looks at the currently selected cell
and if it's an array formula re-calculates that cell and resizes the
output range so that it matches the dimensions of the result of the array
formula.

This can be useful when dealing with array formulas where the dimensions
of the result can vary and it's tedious to have to keep resizing the
Excel formula manually.

The function is registered as a menu item as well as a macro and can
be run from the menu or via the keyboard shortcut Ctrl+Shift+R.

.. warning: Depends on `pyxll_utils.shortcuts`

How to use it?
--------------

Just load the `pyxll_utils.resize_array_formula` in PyXLL (from within a PyXLL
extenion or directly in the `pyxll.cfg` file).
