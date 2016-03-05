#!/usr/bin/env python
# -*- coding: utf-8 -*-


def load(submit_ribbon_tab=None, **kw):
    """ Loads the PyXLL modules to be exposed to Excel. """

    # Try to submit our ribbon piece to PyXLL

    if submit_ribbon_tab:
        import os
        import pkgutil
        tab_template = pkgutil.get_data('data_analytics', 'ribbon_tab.xml')
        root_path = os.path.join(os.path.dirname(__file__), '')
        tab = tab_template.format(ROOT=root_path)
        submit_ribbon_tab('data_analytics', tab)
