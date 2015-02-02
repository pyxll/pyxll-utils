""" PyXLL Automation support with COM. """

import pyxll

import logging	
_log = logging.getLogger(__name__)

try:
    import win32com.client
except ImportError:
    _log.warning("*** win32com.client is required for COM support   ***")

#
# Getting the Excel COM object
#
# PyXLL has a function 'get_active_object'. This returns
# a PyIDispatch object for the Excel window instance.
# It is better to use this than
# win32com.client.Dispatch("Excel.Application")
# as it will always be the correct handle - ie the handle
# to the correct instance of Excel.
#
# The window object can be wrapped as a 
# win32com.client.Dispatch object to make it
# easier to use, as shown in these examples.
#
# For more information on win32com see the pywin32 project
# on sourceforge.
#
# The Excel object model is the same from COM as from VBA
# so usually it's straightforward to write something
# in python if you know how to do it in VBA.
#
# For more information about the Excel object model
# see MSDN or the object browser in the Excel VBA editor.
#

def xl_app():
    """returns a Dispatch object for the current Excel instance"""
    # get the Excel application object from PyXLL and wrap it
    xl_window = pyxll.get_active_object()
    xl_app = win32com.client.Dispatch(xl_window).Application

    # it's helpful to make sure the gen_py wrapper has been created
    # as otherwise things like constants and event handlers won't work.
    win32com.client.gencache.EnsureDispatch(xl_app)

    return xl_app