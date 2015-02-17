""" PyXLL extension loader.

Loads all the extensions contributing to the pyxll.extensions namespace. This
module is supposed to be added to you pyxll.cfg file to automatically load all
the installed packages that contributes to PyXLL through setuptools.

"""
import logging

from stevedore.extension import ExtensionManager

logger = logging.getLogger(__name__)

PYXLL_NAMESPACE = 'pyxll.extensions'

def load_extensions():
    extension_manager = ExtensionManager(
        namespace=PYXLL_NAMESPACE, invoke_on_load=True,
    )


    if len(extension_manager.extensions) > 0:
        logger.info(
            'Extensions loaded:\n{}'.format('\n'.join(extension_manager.names()))
        )
    else:
        logger.info('No extension loaded')

    return extension_manager

_manager = load_extensions()
