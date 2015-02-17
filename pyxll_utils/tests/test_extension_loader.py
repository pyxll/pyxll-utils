import mock
import unittest


from pkg_resources import EntryPoint
from stevedore.extension import ExtensionManager, Extension

from pyxll_utils.extension_loader import PYXLL_NAMESPACE, load_extensions


class ExtensionLoaderTestCase(unittest.TestCase):

    @mock.patch('pyxll_utils.extension_loader.ExtensionManager')
    def test_load_extensions(self, mock_em):

        mock_em.return_value = ExtensionManager.make_test_instance(
            extensions=[
                Extension(
                    'test', EntryPoint('fake_module', 'Callable'), None, self
                )
            ],
            namespace=PYXLL_NAMESPACE
        )

        manager = load_extensions()

        self.assertEqual(len(manager.extensions), 1)
        self.assertEqual(manager.names(), ['test'])

        
