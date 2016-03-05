Extension loader
================

When distributing code based on PyXLL, the question of deployment needs to be
carefully solved. The PyXLL configuration file, `pyxll.cfg`, contains the list
of module that must be loaded to contribute functionalities to Excel. Forcing
the user to edit the configuration file to deploy new functionalities is not
always practical and does not scale in the context of corporate deployment.

The extension loader for PyXLL allows developer to contribute functionalities
to PyXLL without the need to modify the configuration file. By exposing an
entry point, any Python package is allowed to contribute PyXLL function, macros
and menus in a very practical way. The extension loader relies on standard
Python deployment process which makes it a good choice for deployment.

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

2. Adjust the `ribbon` configuration value.

As of this writing, PyXLL reads the configuration setting for the ribbon file
prior to loading extensions. The solution is to rename the `ribbon`
configuration key to `default_ribbon`, and to create a new `ribbon` with a
value that is safe to modify. This file doesn't need to exist yet and will be
overwritten. We suggest setting this new `ribbon` file to be right next to the
`default_ribbon` like so::

    [PYXLL]
    ...
    default_ribbon = ./examples/ribbon/ribbon.xml
    ribbon = ./examples/ribbon/ribbon_extended.xml


Developers
----------

The PyXLL utils extension loader uses the `stevedore` package that leverages
the `setuptools` entry point machinery to discover extensions. To build a
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
`mypackage.myodule.callable(**kw)` when PyXLL will start. The callable must be
prepared to accept arbitrary keyword arguments in order to avoid forward
compatibility issues as this extension mechanism grows new features. If the
callable activates some `@xl_func`, or `@xl_macro` or `@xl_menu` decorators,
they will be exposed to Excel.

Some advanced checks can be added in the callable (dependencies verification,
version checks, access rights, etc.).

The ribbon workaround is due to PyXLL reading the config file prior to loading
any extensions. To work around this, the extension mechanism must
write directly over the file marked as `ribbon` so that PyXLL will load it. Our
solution is specify a second "default" ribbon file, which will serve as the
base to which other extensions can contribute. PyXLL will combine the
`default_ribbon` with any additional ribbon features contributed by extensions
before writing out a finalized ribbon to `ribbon`.

Basic Example
-------------

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

    def load(**kw):
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
                'data_analytics = data_analytics.pyxll_extension:load'
            ]
        }
    )

Then build and install your egg, start Excel and the ewma function will be
available. The PyXLL log file will list your extension::

    2015-02-03 16:15:34,510 - INFO : Extensions loaded:
    data_analytics
    ...


Ribbon Extension Example
------------------------

A developer has written an extension which should contribute a tab to the excel
ribbon (requires PyXLL >= 3.0). If the `tab` element's `id` attribute matches
an existing tab, the two tabs will be combined by appended the contributed
tab's groups to the original.

The package will contain the following files:

1. `data_analytics/pyxll_extension.py`::

    def load(submit_ribbon_tab=None, **kw):
        """ Loads the PyXLL modules to be exposed to Excel. """

        # Try to submit our ribbon piece to PyXLL
        if submit_ribbon_tab:
            import os
            import pkgutil
            tab_template = pkgutil.get_data('data_analytics', 'ribbon_tab.xml')
            root_path = os.path.dirname(__file__)
            tab = tab_template.format(ROOT=root_path)
            submit_ribbon_tab('data_analytics', tab)

2. `setup.py`::

    from setuptools import setup, find_packages

    setup(
        name='data_analytics',
        version='1.0',
        packages=find_packages(),
        package_data={'data_analytics': ['ribbon_tab.xml', '*.png']},
        entry_points={
            'pyxll.extensions': [
                'data_analytics = data_analytics.pyxll_extension:load'
            ]
        }
    )

3. `data_analytics/ribbon_tab.xml`::

    <tab id="data_analytics_tab" label="DataAnalytics">
      <group id="data_analytics_group" label="Analyze">
        <button id="data_analytics_button"
          size="large"
          label="Do Some Analytics!"
          onAction="pyxll.about"
          image="{ROOT}\data_analytics_button.png"/>
      </group>
    </tab>

4. `data_analytics/data_analytics_button.png` - An image file


Then build and install your egg, start Excel and the new ribbon button will be
available. The PyXLL log file will announce your extension's ribbon fragment::

    2016-03-05 12:22:48,867 - INFO : Adding ribbon fragment: data_analytics
    2016-03-05 12:22:48,867 - INFO : Wrote extended ribbon to C:\Users\EnUser\AppData\Local\Enthught\Canopy32\User\lib\site-packages\pyxll\examples\ribbon\ribbon_extended.xml
    2016-03-05 12:22:48,867 - INFO : Extensions loaded:
    data_analytics
    ...
