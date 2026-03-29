"""3D Printing Support for InvenTree.

Adds support for 3D printing drivers to integrate into various parts of the system.
"""

from . import PLUGIN_VERSION

# InvenTree plugin libs
from report.models import LabelTemplate
from plugin import InvenTreePlugin
from plugin.machine import BaseMachineType
from .threed import ThreeDPrinterBaseDriver, ThreeDPrinterMachine

# Backwards compatibility imports
try:
    from plugin.mixins import MachineDriverMixin
except ImportError:

    class MachineDriverMixin:
        """Dummy mixin for backwards compatibility."""

        pass

class ThreeDPlugin(MachineDriverMixin, InvenTreePlugin):
    """3D Printing support for InvenTree."""

    AUTHOR = "James Todd"
    DESCRIPTION = "3D Printing support for InvenTree"
    VERSION = PLUGIN_VERSION

    MIN_VERSION = "0.16.0"

    NAME = "3D Printing"
    SLUG = "3d-printing"
    TITLE = "3D Printing Support"

    # Individual machine drivers should register themselves, we don't want the base driver being registered.
    # def get_machine_drivers(self) -> list:
    #     print("Registering 3D Printer Machine")
    #     return [ThreeDPrinterBaseDriver]
    
    def get_machine_types(self) -> list:
        print("Registering 3D Printer Type")
        return [ThreeDPrinterMachine]

# threedPlugin