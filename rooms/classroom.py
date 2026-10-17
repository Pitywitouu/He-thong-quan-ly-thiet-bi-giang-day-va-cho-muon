from __future__ import annotations

from typing import List, Optional

try:
    from enums.device_status import DeviceStatus
    from devices.device import Device
except ImportError:
    from ..enums.device_status import DeviceStatus
    from ..devices.device import Device


class ClassRoom:
    def __init__(
        self,
        room_id: str,
        room_name: str,
        capacity: int,
        devices: Optional[List[Device]] = None,
    ) -> None:
        if not isinstance(room_id, str) or not room_id.strip():
            raise ValueError("Mã phòng không được để trống.")
        self._room_id: str = room_id.strip()

        self.room_name = room_name
        self.capacity = capacity
        self._devices: List[Device] = []

        if devices:
            for device in devices:
                self.add_device(device)

    @property
    def room_id(self) -> str:
        return self._room_id

    @property
    def RoomId(self) -> str:
        return self._room_id

    @property
    def room_name(self) -> str:
        return self._room_name

    @room_name.setter
    def room_name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Tên phòng không được để trống.")
        self._room_name = value.strip()

    @property
    def RoomName(self) -> str:
        return self._room_name

    @RoomName.setter
    def RoomName(self, value: str) -> None:
        self.room_name = value

    @property
    def capacity(self) -> int:
        return self._capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Sức chứa phòng phải là số nguyên.")
        if value <= 0:
            raise ValueError("Sức chứa phòng phải lớn hơn 0.")
        self._capacity = value

    @property
    def Capacity(self) -> int:
        return self._capacity

    @Capacity.setter
    def Capacity(self, value: int) -> None:
        self.capacity = value

    @property
    def devices(self) -> List[Device]:
        return list(self._devices)

    @property
    def Devices(self) -> List[Device]:
        return list(self._devices)

    def add_device(self, device: Device) -> None:
        if device is None or not isinstance(device, Device):
            raise ValueError("Không chấp nhận đối tượng thiết bị null hoặc không hợp lệ.")

        if self.find_device(device.device_id) is not None:
            raise ValueError(f"Thiết bị có mã '{device.device_id}' đã tồn tại trong phòng.")

        self._devices.append(device)

    def AddDevice(self, device: Device) -> None:
        self.add_device(device)

    def remove_device(self, device_id: str) -> bool:
        if not isinstance(device_id, str) or not device_id.strip():
            return False

        device = self.find_device(device_id.strip())
        if device is not None:
            self._devices.remove(device)
            return True
        return False

    def RemoveDevice(self, device_id: str) -> bool:
        return self.remove_device(device_id)

    def find_device(self, device_id: str) -> Optional[Device]:
        if not isinstance(device_id, str):
            return None

        clean_id = device_id.strip()
        for device in self._devices:
            if device.device_id == clean_id:
                return device
        return None

    def FindDevice(self, device_id: str) -> Optional[Device]:
        return self.find_device(device_id)

    def calculate_annual_maintenance_cost(self) -> float:
        return sum(device.calculate_annual_maintenance_cost() for device in self._devices)

    def CalculateAnnualMaintenanceCost(self) -> float:
        return self.calculate_annual_maintenance_cost()

    def get_devices_requiring_maintenance(self) -> List[Device]:
        return [
            device
            for device in self._devices
            if device.status == DeviceStatus.UNDER_MAINTENANCE or device.years_of_use > 5
        ]

    def GetDevicesRequiringMaintenance(self) -> List[Device]:
        return self.get_devices_requiring_maintenance()

    def __str__(self) -> str:
        return (
            f"ClassRoom(Mã: '{self._room_id}', Tên: '{self._room_name}', "
            f"Sức chứa: {self._capacity}, Số thiết bị: {len(self._devices)})"
        )

    def __repr__(self) -> str:
        return f"<ClassRoom id='{self._room_id}' name='{self._room_name}' devices={len(self._devices)}>"

Classroom = ClassRoom