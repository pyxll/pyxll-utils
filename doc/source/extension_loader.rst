Extension loader
================

When distributing code based on PyXLL, the question of deployment needs to be
carefully solved. The PyXLL configuration file, `pyxll.cfg`, contains the list
of module that must be loaded to contribute functionalities to Excel. Forcing
the user to edit its configuration file to deploy new functionalities is very
impractical and does not scale in the context of corporate deployment.

The use of `external_config` in the `pyxll.cfg` file is also not very practical
as it can cause clash issues between PyXLL modules (shared dependencies
between config and modules, etc.). It also require manual modifications to the
main configuration file when deploying a new external config.

The extension loader for PyXLL allows developer to contribute functionalities
to PyXLL without the need to modify the configuration file. By exposing an
entry point, any Python package is allowed to contribute PyxLL function, macros
and menus in a very practical way. The extension loader relies on standard
Python deployment process which makes it the solution of choice for deployment.

How to use it?
--------------

1. Register the module with PyXLL

In order to use the extension loader, the developer needs to register it with
PyXLL. In the pyxll.cfg file, add the `pyxll_utils.extension_loader` module to
the list of modules::

    [PYXLL]
    ...
    modules =
        ...
        pyxll_utils.extension_loader
        
The next time PyXLL will be started all the Python packages contributing to the
`pyxll.extensions` extension point will be loaded by PyXLL.


Developers
----------

The PyXLL utils extension loader uses the `stevedore` package that leverages
the `setuptools` entry point machinerie to discover extensions. To build a
Python package that contributes to PyXLL, one just need to add the following
entry point to the `setup.py` of the package::

    setup(
        ...
        entry_points = {
            'pyxll.extensions': [
                'my_extension_name = mypackage.mymodule:callable'
            ]
        }
    )

In this code, the PyXLL extension loader will automatically call
`mypackage.myodule.callable()` when PyXLL will start. If the callable activates
some `@xl_func`, or `@xl_macro` or `@xl_menu` decorators, they will be exposed to
Excel.

Some advanced checkes can be added in the callable (dependencies verification,
version checks, access rights, etc.). 

Example
-------

A developer wants to expose the `ewma` functions from the Pandas library to
Excel. The function will belong to a package `data_analytics`.

The package will contain the following file:

1. `data_analytics/stats.py`::

    from pandas.stats.moments import ewma as pandas_ewma
    
    from pyxll import xl_func
    
    @xl_func('dataframe df, float span: dataframe')
    def ewma(df, span):
        """ Exponentially-weighted moving average. """
        return pandas_ewma(df, span)

2. `data_analytics/pyxll_extension.py`::

    def load():
        """ Loads the PyXLL modules to be exposed to Excel. """

        # load PyXLL utilities dependencies
        
        # required to support the dataframe type converters 
        import pyxll_utils.pandastypes 

        # load all the local modules that we want to expose to Excel
        import data_analytics.stats

3. `setup.py`::

    from setuptools import setup, find_packages

    setup(
        name='data_analytics',
        version='1.0',
        packages=find_packages(),
        entry_points = {
            'pyxll.extensions' : [
                'data_analytics_extension = data_analytics.pyxll_extension:load'
            ]
        }
    )

Then build and install your egg, start Excel and the ewna function will be
available. The PyXLL log file will list your extension::

    2015-02-03 16:15:34,510 - INFO : Extensions loaded:
    data_analytics_extension
    ...
    
    


