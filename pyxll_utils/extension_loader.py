""" PyXLL extension loader.

Loads all the extensions contributing to the pyxll.modules namespace. This
module is supposed to be added to you pyxll.cfg file to automatically load all
the installed packages that contributes to PyXLL through setuptools.

"""
import logging

from stevedore import extension

logger = logging.getLogger(__name__)

extension_manager = extension.ExtensionManager(
        namespace='pyxll.extensions',
        invoke_on_load=True,
)


if len(extension_manager.names()) > 0:
    logger.info(
        'Extensions loaded:\n{}'.format('\n'.join(extension_manager.names()))
    )
else:
    logger.info('No extension loaded')

