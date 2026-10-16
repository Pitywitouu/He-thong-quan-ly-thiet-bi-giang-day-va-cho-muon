from __future__ import annotations

try:
    from enums.device_status import DeviceStatus
except ImportError:
    from ..enums.device_status import DeviceStatus

from .device import Device
from .teaching_device import TeachingDevice
from .air_conditioner_remote import AirConditionerRemote
from .microphone import Microphone
from .projector_remote import ProjectorRemote

__all__ = [
    "DeviceStatus",
    "Device",
    "TeachingDevice",
    "AirConditionerRemote",
    "Microphone",
    "ProjectorRemote",
]
