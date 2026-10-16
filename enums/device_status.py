from __future__ import annotations

from enum import Enum


class DeviceStatus(Enum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
    UNDER_MAINTENANCE = "UnderMaintenance"
    RETIRED = "Retired"
    ACTIVE = "Active"

    Available = "Available"
    Borrowed = "Borrowed"
    UnderMaintenance = "UnderMaintenance"
    Retired = "Retired"
    Active = "Active"
