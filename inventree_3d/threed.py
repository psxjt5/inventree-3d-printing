from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _

from generic.states import ColorEnum
from machine.machine_type import BaseDriver, BaseMachineType, MachineStatus
from plugin import registry as plg_registry
from plugin.base.label.mixins import LabelPrintingMixin
from report.models import LabelTemplate
from stock.models import StockLocation

class ThreeDPrinterBaseDriver(BaseDriver):
    """Base driver for 3D printer machines."""

    machine_type = '3d-printer'

    USE_BACKGROUND_WORKER = True

class ThreeDPrinterStatus(MachineStatus):
    """3D printer status codes.

    Attributes:
        PRINTING: The printer is currently printing a job
        IDLE: The printer is connected and waiting for a job
        WARNING: The printer is in an unknown warning condition
        ERROR: The printer is in an unknown error condition
        MISCONFIGURED: The printer is missing required setting values
        UNKNOWN: The printer status is unknown (e.g. there is no active connection to the printer)
    """

    CONNECTED = 100, _('Connected'), ColorEnum.primary
    DISCONNECTED = 101, _('Disconnected'), ColorEnum.danger
    PRINTING = 200, _('Printing'), ColorEnum.primary
    IDLE = 201, _('Idle'), ColorEnum.primary
    FINISHED = 202, _('Finished'), ColorEnum.success
    PAUSED = 203, _('Paused'), ColorEnum.success
    FAILED = 204, _('Failed'), ColorEnum.danger
    MISCONFIGURED = 998, _('Misconfigured'), ColorEnum.danger
    UNKNOWN = 999, _('Unknown'), ColorEnum.secondary

class ThreeDPrinterMachine(BaseMachineType):
    """3D printer machine type."""

    SLUG = '3d-printer'
    NAME = _('3D Printer')
    DESCRIPTION = _('Print and monitor 3D printing jobs.')

    base_driver = ThreeDPrinterBaseDriver

    MACHINE_SETTINGS = {
        'LOCATION': {
            'name': _('3D Printer Location'),
            'description': _('Scope the printer to a specific location'),
            'model': 'stock.stocklocation',
        }
    }

    MACHINE_STATUS: type[ThreeDPrinterStatus] = ThreeDPrinterStatus

    default_machine_status = ThreeDPrinterStatus.UNKNOWN

    @property
    def location(self):
        """Access the machines location instance using this property."""
        location_pk = self.get_setting('LOCATION', 'M')

        if not location_pk:
            return None

        return StockLocation.objects.get(pk=location_pk)