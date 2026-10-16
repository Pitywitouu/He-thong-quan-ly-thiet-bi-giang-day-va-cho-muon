from __future__ import annotations

from abc import ABC
from typing import Union

try:
    from enums.device_status import DeviceStatus
    from devices.device import Device
except ImportError:
    from ..enums.device_status import DeviceStatus
    from .device import Device


class TeachingDevice(Device, ABC):
    def __init__(
        self,
        device_id,
        name,
        year_in_use,
        purchase_price,
        max_borrow_days: int = 1,
        status: Union[DeviceStatus, str] = DeviceStatus.AVAILABLE,
    ) -> None:
        super().__init__(
            device_id = device_id,
            name = name,
            year_in_use = year_in_use,
            purchase_price = purchase_price,
            status = status,
        )
        self.max_borrow_days = max_borrow_days

    @property
    def max_borrow_days(self) -> int:
        return self._max_borrow_days

    @max_borrow_days.setter
    def max_borrow_days(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Số ngày mượn tối đa phải là số nguyên.")
        if value <= 0:
            raise ValueError("Số ngày mượn tối đa phải lớn hơn 0.")
        self._max_borrow_days = value

    @property
    def max_borrow_periods(self) -> int:
        return self._max_borrow_days

    @max_borrow_periods.setter
    def max_borrow_periods(self, value: int) -> None:
        self.max_borrow_days = value

    def mark_as_borrowed(self) -> None:
        self.status = DeviceStatus.BORROWED

    def MarkAsBorrowed(self) -> None:
        self.mark_as_borrowed()

    def mark_as_available(self) -> None:
        self.status = DeviceStatus.AVAILABLE

    def MarkAsAvailable(self) -> None:
        self.mark_as_available()

    def mark_as_under_maintenance(self) -> None:
        self.status = DeviceStatus.UNDER_MAINTENANCE

    def MarkAsUnderMaintenance(self) -> None:
        self.mark_as_under_maintenance()

    def is_available(self) -> bool:
        return self.status in (DeviceStatus.AVAILABLE, DeviceStatus.Available)

    def is_borrowed(self) -> bool:
        return self.status in (DeviceStatus.BORROWED, DeviceStatus.Borrowed)

    def is_under_maintenance(self) -> bool:
        return self.status in (DeviceStatus.UNDER_MAINTENANCE, DeviceStatus.UnderMaintenance)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(ID: {self.device_id}, Tên: '{self.name}', "
            f"Năm SD: {self.year_in_use}, Giá: {self.purchase_price:,.0f} VND, "
            f"Mượn tối đa: {self._max_borrow_days} ngày, Trạng thái: {self.status.value})"
        )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} id='{self.device_id}' "
            f"name='{self.name}' max_days={self._max_borrow_days} status='{self.status.value}'>"
        )
