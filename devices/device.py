from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Union

try:
    from enums.device_status import DeviceStatus
except ImportError:
    from ..enums.device_status import DeviceStatus


class Device(ABC):
    def __init__(
        self,
        device_id: str,
        name: str,
        year_in_use: int,
        purchase_price: Union[float, int],
        status: Union[DeviceStatus, str] = DeviceStatus.AVAILABLE,
    ) -> None:
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("Mã thiết bị không được để trống.")
        self._device_id: str = device_id.strip()

        self.name = name
        self.year_in_use = year_in_use
        self.purchase_price = purchase_price
        self.status = status

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Tên thiết bị không được để trống.")
        self._name = value.strip()

    @property
    def year_in_use(self) -> int:
        return self._year_in_use

    @year_in_use.setter
    def year_in_use(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Năm đưa vào sử dụng phải là số nguyên.")
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError(
                f"Năm đưa vào sử dụng ({value}) không được lớn hơn năm hiện tại ({current_year})."
            )
        if value <= 0:
            raise ValueError("Năm đưa vào sử dụng phải lớn hơn 0.")
        self._year_in_use = value

    @property
    def purchase_price(self) -> float:
        return self._purchase_price

    @purchase_price.setter
    def purchase_price(self, value: Union[float, int]) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Giá mua phải là số.")
        if value <= 0:
            raise ValueError("Giá mua phải lớn hơn 0.")
        self._purchase_price = float(value)

    @property
    def status(self) -> DeviceStatus:
        return self._status

    @status.setter
    def status(self, value: Union[DeviceStatus, str]) -> None:
        if isinstance(value, str):
            clean_val = value.strip()
            try:
                self._status = DeviceStatus[clean_val]
            except KeyError:
                try:
                    self._status = DeviceStatus(clean_val)
                except ValueError:
                    raise ValueError(f"Trạng thái '{value}' không hợp lệ.")
        elif isinstance(value, DeviceStatus):
            self._status = value
        else:
            raise TypeError("Trạng thái phải là đối tượng DeviceStatus hoặc chuỗi hợp lệ.")

    @property
    def years_of_use(self) -> int:
        return max(0, datetime.now().year - self._year_in_use)

    @abstractmethod
    def calculate_annual_maintenance_cost(self) -> float:
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Device):
            return False
        return self._device_id == other._device_id

    def __hash__(self) -> int:
        return hash(self._device_id)

    def __str__(self) -> str:
        return (
            f"Device(ID: {self._device_id}, Tên: '{self._name}', "
            f"Năm SD: {self._year_in_use}, Giá: {self._purchase_price:,.0f} VND, "
            f"Trạng thái: {self._status.value})"
        )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} id='{self._device_id}' "
            f"name='{self._name}' status='{self._status.value}'>"
        )
