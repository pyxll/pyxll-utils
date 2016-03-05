""" PyXLL extension loader.

Loads all the extensions contributing to the pyxll.modules namespace. This
module is supposed to be added to you pyxll.cfg file to automatically load all
the installed packages that contributes to PyXLL through setuptools.

"""
import logging

from stevedore import extension

from pyxll import get_config
from ribbon_synthesizer import RibbonSynthesizer

logger = logging.getLogger(__name__)

config = get_config()
orig_ribbon_path = config.get('PYXLL', 'default_ribbon')
extended_ribbon_path = config.get('PYXLL', 'ribbon')

ribbon_synthesizer = RibbonSynthesizer.from_file(orig_ribbon_path)

extension_manager = extension.ExtensionManager(
    namespace='pyxll.extensions',
    invoke_on_load=True,
    invoke_kwds={'submit_ribbon_tab': ribbon_synthesizer.submit_ribbon_tab},
)

if ribbon_synthesizer.modified:
    with open(extended_ribbon_path, 'w') as f:
        f.write(ribbon_synthesizer.to_bytes())
        logger.info("Wrote extended ribbon to {}".format(extended_ribbon_path))

if len(extension_manager.names()) > 0:
    logger.info(
        'Extensions loaded:\n{}'.format('\n'.join(extension_manager.names()))
    )
else:
    logger.info('No extension loaded')
