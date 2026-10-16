from __future__ import annotations

from typing import Union

try:
    from enums.device_status import DeviceStatus
    from devices.teaching_device import TeachingDevice
except ImportError:
    from ..enums.device_status import DeviceStatus
    from .teaching_device import TeachingDevice


class Microphone(TeachingDevice):
    def __init__(
        self,
        device_id,
        name,
        year_in_use,
        purchase_price,
        is_wireless: bool = True,
        frequency_band: str = "UHF",
        battery_type: str = "AA",
        max_borrow_days: int = 1,
        status: Union[DeviceStatus, str] = DeviceStatus.AVAILABLE,
    ) -> None:
        super().__init__(
            device_id = device_id,
            name = name,
            year_in_use = year_in_use,
            purchase_price = purchase_price,
            max_borrow_days = max_borrow_days,
            status = status,
        )
        self.is_wireless = is_wireless
        self.frequency_band = frequency_band
        self.battery_type = battery_type

    @property
    def is_wireless(self) -> bool:
        return self._is_wireless

    @is_wireless.setter
    def is_wireless(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("is_wireless phải là giá trị boolean.")
        self._is_wireless = value

    @property
    def frequency_band(self) -> str:
        return self._frequency_band

    @frequency_band.setter
    def frequency_band(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Dải băng tần không được để trống.")
        self._frequency_band = value.strip()

    @property
    def battery_type(self) -> str:
        return self._battery_type

    @battery_type.setter
    def battery_type(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Loại pin không được để trống.")
        self._battery_type = value.strip()

    def calculate_annual_maintenance_cost(self) -> float:
        base_cost = 0.08 * self.purchase_price
        wireless_extra = 100000.0 if self._is_wireless else 0.0
        age_extra = 50000.0 if self.years_of_use > 3 else 0.0
        return base_cost + wireless_extra + age_extra

    def __str__(self) -> str:
        type_str = "Không dây" if self._is_wireless else "Có dây"
        return (
            f"Microphone(ID: {self.device_id}, Tên: '{self.name}', "
            f"Loại: {type_str}, Băng tần: {self._frequency_band}, Pin: {self._battery_type}, "
            f"Năm SD: {self.year_in_use}, Giá: {self.purchase_price:,.0f} VND, "
            f"Mượn tối đa: {self.max_borrow_days} ngày, Trạng thái: {self.status.value})"
        )
