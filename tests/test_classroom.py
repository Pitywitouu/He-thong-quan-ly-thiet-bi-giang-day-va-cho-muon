from __future__ import annotations

import os
import sys
import unittest
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from enums.device_status import DeviceStatus
from devices.air_conditioner_remote import AirConditionerRemote
from devices.microphone import Microphone
from devices.projector_remote import ProjectorRemote
from rooms.classroom import ClassRoom, Classroom


class TestClassRoomInit(unittest.TestCase):
    def test_valid_init(self):
        room = ClassRoom(room_id="P101", room_name="Phòng Lý Thuyết 101", capacity=50)
        self.assertEqual(room.room_id, "P101")
        self.assertEqual(room.room_name, "Phòng Lý Thuyết 101")
        self.assertEqual(room.capacity, 50)
        self.assertEqual(len(room.devices), 0)

    def test_alias_classroom(self):
        room = Classroom(room_id="P102", room_name="Phòng Thực Hành", capacity=40)
        self.assertIsInstance(room, ClassRoom)

    def test_room_id_read_only(self):
        room = ClassRoom("P101", "Phòng 101", 50)
        with self.assertRaises(AttributeError):
            room.room_id = "P999"

    def test_validation_empty_room_id(self):
        with self.assertRaises(ValueError):
            ClassRoom("", "Phòng 101", 50)
        with self.assertRaises(ValueError):
            ClassRoom("   ", "Phòng 101", 50)

    def test_validation_empty_room_name(self):
        with self.assertRaises(ValueError):
            ClassRoom("P101", "", 50)
        with self.assertRaises(ValueError):
            ClassRoom("P101", "   ", 50)

    def test_validation_capacity(self):
        with self.assertRaises(ValueError):
            ClassRoom("P101", "Phòng 101", 0)
        with self.assertRaises(ValueError):
            ClassRoom("P101", "Phòng 101", -10)
        with self.assertRaises(TypeError):
            ClassRoom("P101", "Phòng 101", "50")


class TestClassRoomDeviceManagement(unittest.TestCase):
    def setUp(self):
        self.room = ClassRoom("P201", "Phòng Hội Thảo", 100)
        self.current_year = datetime.now().year
        self.ac = AirConditionerRemote("AC01", "ĐK Daikin", self.current_year, 200000)
        self.mic = Microphone("MIC01", "Micro Sony", self.current_year, 1000000)
        self.proj = ProjectorRemote("PR01", "ĐK Máy Chiếu", self.current_year, 400000)

    def test_add_device_success(self):
        self.room.add_device(self.ac)
        self.room.add_device(self.mic)
        self.assertEqual(len(self.room.devices), 2)
        self.assertIn(self.ac, self.room.devices)
        self.assertIn(self.mic, self.room.devices)

    def test_add_null_device_raises(self):
        with self.assertRaises(ValueError):
            self.room.add_device(None)

    def test_add_duplicate_device_id_raises(self):
        self.room.add_device(self.ac)
        ac_duplicate = AirConditionerRemote("AC01", "ĐK Daikin Khác", self.current_year, 250000)
        with self.assertRaises(ValueError):
            self.room.add_device(ac_duplicate)

    def test_remove_device(self):
        self.room.add_device(self.ac)
        self.room.add_device(self.mic)

        self.assertTrue(self.room.remove_device("AC01"))
        self.assertEqual(len(self.room.devices), 1)
        self.assertIsNone(self.room.find_device("AC01"))

        self.assertFalse(self.room.remove_device("NOT_FOUND"))

    def test_find_device(self):
        self.room.add_device(self.proj)
        found = self.room.find_device("PR01")
        self.assertEqual(found, self.proj)
        self.assertIsNone(self.room.find_device("UNKNOWN"))

    def test_calculate_annual_maintenance_cost_polymorphic(self):
        self.room.add_device(self.ac)
        self.room.add_device(self.mic)
        self.room.add_device(self.proj)

        expected_total = (
            self.ac.calculate_annual_maintenance_cost()
            + self.mic.calculate_annual_maintenance_cost()
            + self.proj.calculate_annual_maintenance_cost()
        )
        self.assertEqual(self.room.calculate_annual_maintenance_cost(), expected_total)

    def test_get_devices_requiring_maintenance(self):
        # Thiết bị 1: Mới, Available -> Không cần bảo trì
        dev_ok = Microphone("MIC_OK", "Mic Tốt", self.current_year, 1000000, status=DeviceStatus.AVAILABLE)

        # Thiết bị 2: Đang UnderMaintenance -> Cần bảo trì
        dev_maint = AirConditionerRemote(
            "AC_MAINT", "ĐK Hỏng", self.current_year, 200000, status=DeviceStatus.UNDER_MAINTENANCE
        )

        # Thiết bị 3: Sử dụng trên 5 năm (current_year - 6) -> Cần bảo trì
        dev_old = ProjectorRemote(
            "PR_OLD", "ĐK Cũ", self.current_year - 6, 300000, status=DeviceStatus.AVAILABLE
        )

        # Thiết bị 4: Đúng 5 năm (current_year - 5) -> Không > 5 năm
        dev_five_years = Microphone(
            "MIC_5Y", "Mic 5 Năm", self.current_year - 5, 1000000, status=DeviceStatus.AVAILABLE
        )

        self.room.add_device(dev_ok)
        self.room.add_device(dev_maint)
        self.room.add_device(dev_old)
        self.room.add_device(dev_five_years)

        req_maint = self.room.get_devices_requiring_maintenance()
        self.assertEqual(len(req_maint), 2)
        self.assertIn(dev_maint, req_maint)
        self.assertIn(dev_old, req_maint)
        self.assertNotIn(dev_ok, req_maint)
        self.assertNotIn(dev_five_years, req_maint)


if __name__ == "__main__":
    unittest.main()
