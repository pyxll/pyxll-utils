Shortuts
========

The decorator @xl_shortcut is used to decorate a macro function, and when
Excel starts win32com is used to associate that macro to a shortcut.

Example::

    from pyxll import xl_macro, xlcAlert
    from shortcuts import xl_shortcut

    @xl_shortcut("Ctrl+Shift+H")
    @xl_macro()
    def my_macro():
        xlcAlert("Hello!")

Pressing Ctrl+Shift+H calls the macro and shows the alert.


How to use it?
--------------

Load the `pyxll_utils.shortcuts` module in your PyXLL extension or in your
`pyxll.cfg` file.
