from __future__ import annotations

from typing import Union

try:
    from enums.device_status import DeviceStatus
    from devices.teaching_device import TeachingDevice
except ImportError:
    from ..enums.device_status import DeviceStatus
    from .teaching_device import TeachingDevice


class AirConditionerRemote(TeachingDevice):
    def __init__(
        self,
        device_id,
        name,
        year_in_use,
        purchase_price,
        brand: str = "Daikin",
        battery_type: str = "AAA",
        has_screen: bool = True,
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
        self.brand = brand
        self.battery_type = battery_type
        self.has_screen = has_screen

    @property
    def brand(self) -> str:
        return self._brand

    @brand.setter
    def brand(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Hãng điều hòa không được để trống.")
        self._brand = value.strip()

    @property
    def battery_type(self) -> str:
        return self._battery_type

    @battery_type.setter
    def battery_type(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Loại pin không được để trống.")
        self._battery_type = value.strip()

    @property
    def has_screen(self) -> bool:
        return self._has_screen

    @has_screen.setter
    def has_screen(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("has_screen phải là giá trị boolean.")
        self._has_screen = value

    def calculate_annual_maintenance_cost(self) -> float:
        base_cost = 0.05 * self.purchase_price
        battery_cost = 40000.0
        age_extra = 30000.0 if self.years_of_use > 3 else 0.0
        return base_cost + battery_cost + age_extra

    def __str__(self) -> str:
        screen_info = "Có màn hình" if self._has_screen else "Không màn hình"
        return (
            f"AirConditionerRemote(ID: {self.device_id}, Tên: '{self.name}', "
            f"Hãng: '{self._brand}', Pin: {self._battery_type}, {screen_info}, "
            f"Năm SD: {self.year_in_use}, Giá: {self.purchase_price:,.0f} VND, "
            f"Mượn tối đa: {self.max_borrow_days} ngày, Trạng thái: {self.status.value})"
        )
