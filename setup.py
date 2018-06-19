from setuptools import setup, find_packages

setup(name='pyxll_utils',
      version='2.1',
      author='PyXLL Ltd, Enthought Inc.',
      license='BSD 2-Clause "Simplified" License',
      long_description=open('README.md').read(),
      packages=find_packages(),
      setup_requires=[
          'pypiwin32',
          'stevedore',
          'pytest-runner',
      ],
      tests_require=[
          'pytest'
      ],
      # Provides a namespace for extension points to contribute to. This
      # functionality is required by the pyxll_addons.extension_loader module
      provides=['pyxll.extensions'])
