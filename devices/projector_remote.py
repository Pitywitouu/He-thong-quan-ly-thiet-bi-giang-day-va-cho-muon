from __future__ import annotations

from typing import Union

try:
    from enums.device_status import DeviceStatus
    from devices.teaching_device import TeachingDevice
except ImportError:
    from ..enums.device_status import DeviceStatus
    from .teaching_device import TeachingDevice


class ProjectorRemote(TeachingDevice):
    def __init__(
        self,
        device_id,
        name,
        year_in_use,
        purchase_price,
        supported_projector_brand: str = "Sony",
        has_laser_pointer: bool = True,
        battery_type: str = "AAA",
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
        self.supported_projector_brand = supported_projector_brand
        self.has_laser_pointer = has_laser_pointer
        self.battery_type = battery_type

    @property
    def supported_projector_brand(self) -> str:
        return self._supported_projector_brand

    @supported_projector_brand.setter
    def supported_projector_brand(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Hãng máy chiếu tương thích không được để trống.")
        self._supported_projector_brand = value.strip()

    @property
    def has_laser_pointer(self) -> bool:
        return self._has_laser_pointer

    @has_laser_pointer.setter
    def has_laser_pointer(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("has_laser_pointer phải là giá trị boolean.")
        self._has_laser_pointer = value

    @property
    def battery_type(self) -> str:
        return self._battery_type

    @battery_type.setter
    def battery_type(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Loại pin không được để trống.")
        self._battery_type = value.strip()

    def calculate_annual_maintenance_cost(self) -> float:
        base_cost = 0.06 * self.purchase_price
        laser_extra = 50000.0 if self._has_laser_pointer else 0.0
        age_extra = 30000.0 if self.years_of_use > 3 else 0.0
        return base_cost + laser_extra + age_extra

    def __str__(self) -> str:
        laser_str = "Có Laser" if self._has_laser_pointer else "Không Laser"
        return (
            f"ProjectorRemote(ID: {self.device_id}, Tên: '{self.name}', "
            f"Hãng máy chiếu: '{self._supported_projector_brand}', {laser_str}, Pin: {self._battery_type}, "
            f"Năm SD: {self.year_in_use}, Giá: {self.purchase_price:,.0f} VND, "
            f"Mượn tối đa: {self.max_borrow_days} ngày, Trạng thái: {self.status.value})"
        )
