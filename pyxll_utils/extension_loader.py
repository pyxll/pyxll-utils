""" PyXLL extension loader.

Loads all the extensions contributing to the pyxll.modules namespace. This
module is supposed to be added to you pyxll.cfg file to automatically load all
the installed packages that contributes to PyXLL through setuptools.

"""
import errno
import logging
import os

from stevedore import extension

from pyxll import get_config
from .ribbon_synthesizer import RibbonSynthesizer

logger = logging.getLogger(__name__)

# Keyword args to pass to plugin initializers
invoke_kwds = {}

config = dict(get_config().items('PYXLL'))
default_ribbon_path = config.get('default_ribbon', '')
ribbon_path = config.get('ribbon', '')

should_make_ribbon = (default_ribbon_path and ribbon_path and
                      default_ribbon_path != ribbon_path)
ribbon_synthesizer = RibbonSynthesizer.from_file(default_ribbon_path)

if should_make_ribbon:
    invoke_kwds['submit_ribbon_tab'] = ribbon_synthesizer.submit_ribbon_tab
else:
    logger.info("The ribbon will not be modified because your config does"
                " not define both PYXLL::ribbon and PYXLL::default_ribbon")

extension_manager = extension.ExtensionManager(
    namespace='pyxll.extensions',
    invoke_on_load=True,
    invoke_kwds=invoke_kwds,
)

extension_names = extension_manager.names()

if len(extension_names) > 0:
    logger.info(
        'Extensions loaded:\n{}'.format('\n'.join(extension_names))
    )
else:
    logger.info('No extension loaded')

if should_make_ribbon:
    target_dir = os.path.dirname(ribbon_path)
    try:
        # If the ribbon dirs don't exist, make them.
        os.makedirs(target_dir)
        logger.info("Created ribbon directory: {}".format(target_dir))
    except Exception as e:
        if not e.errno == errno.EEXIST:
            raise
    with open(ribbon_path, 'w') as f:
        f.write(ribbon_synthesizer.to_bytes())
        logger.info("Wrote extended ribbon to {}".format(ribbon_path))
