#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
