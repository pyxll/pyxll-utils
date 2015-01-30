""" PyXLL extension loader. """

from stevedore import extension

mgr = extension.ExtensionManager(
        namespace='pyxll.modules',
        invoke_on_load=True,
)