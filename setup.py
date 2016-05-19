from setuptools import setup, find_packages

setup(name='pyxll_utils',
      version='1.0',
      author='PyXLL Ltd, Enthought Inc.',
      packages=find_packages(),
      # Provides a namespace for extension points to contribute to. This
      # functionality is required by the pyxll_addons.extension_loader module
      provides=['pyxll.extensions'])
