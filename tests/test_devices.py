from __future__ import annotations

import os
import sys
import unittest
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from enums.device_status import DeviceStatus
from devices.device import Device
from devices.teaching_device import TeachingDevice
from devices.air_conditioner_remote import AirConditionerRemote
from devices.microphone import Microphone
from devices.projector_remote import ProjectorRemote


class DummyDevice(Device):
    def calculate_annual_maintenance_cost(self) -> float:
        return 0.05 * self.purchase_price


class DummyTeachingDevice(TeachingDevice):
    def calculate_annual_maintenance_cost(self) -> float:
        return 0.05 * self.purchase_price


class TestDeviceStatusEnum(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(DeviceStatus.AVAILABLE.value, "Available")
        self.assertEqual(DeviceStatus.BORROWED.value, "Borrowed")
        self.assertEqual(DeviceStatus.UNDER_MAINTENANCE.value, "UnderMaintenance")
        self.assertEqual(DeviceStatus.RETIRED.value, "Retired")

    def test_enum_aliases(self):
        self.assertEqual(DeviceStatus.Available, DeviceStatus.AVAILABLE)
        self.assertEqual(DeviceStatus.Borrowed, DeviceStatus.BORROWED)
        self.assertEqual(DeviceStatus.UnderMaintenance, DeviceStatus.UNDER_MAINTENANCE)


class TestDeviceBase(unittest.TestCase):
    def test_valid_creation(self):
        d = DummyDevice(
            device_id="DEV01",
            name="Thiết bị mẫu",
            year_in_use=2022,
            purchase_price=500000.0,
            status=DeviceStatus.AVAILABLE,
        )
        self.assertEqual(d.device_id, "DEV01")
        self.assertEqual(d.name, "Thiết bị mẫu")
        self.assertEqual(d.year_in_use, 2022)
        self.assertEqual(d.purchase_price, 500000.0)
        self.assertEqual(d.status, DeviceStatus.AVAILABLE)

    def test_device_id_read_only(self):
        d = DummyDevice("DEV01", "Thiết bị mẫu", 2022, 500000)
        with self.assertRaises(AttributeError):
            d.device_id = "NEW_ID"

    def test_device_id_validation(self):
        with self.assertRaises(ValueError):
            DummyDevice("", "Tên", 2022, 500000)
        with self.assertRaises(ValueError):
            DummyDevice("   ", "Tên", 2022, 500000)

    def test_name_validation(self):
        with self.assertRaises(ValueError):
            DummyDevice("D01", "", 2022, 500000)
        with self.assertRaises(ValueError):
            DummyDevice("D01", "   ", 2022, 500000)

    def test_year_in_use_validation(self):
        current_year = datetime.now().year
        with self.assertRaises(ValueError):
            DummyDevice("D01", "Tên", current_year + 1, 500000)
        with self.assertRaises(ValueError):
            DummyDevice("D01", "Tên", 0, 500000)
        with self.assertRaises(ValueError):
            DummyDevice("D01", "Tên", -2020, 500000)
        with self.assertRaises(TypeError):
            DummyDevice("D01", "Tên", "2020", 500000)

    def test_purchase_price_validation(self):
        with self.assertRaises(ValueError):
            DummyDevice("D01", "Tên", 2022, 0)
        with self.assertRaises(ValueError):
            DummyDevice("D01", "Tên", 2022, -1000)
        with self.assertRaises(TypeError):
            DummyDevice("D01", "Tên", 2022, "500000")

    def test_status_setting_with_string_and_enum(self):
        d = DummyDevice("D01", "Tên", 2022, 500000)
        d.status = "Borrowed"
        self.assertEqual(d.status, DeviceStatus.BORROWED)
        d.status = DeviceStatus.UNDER_MAINTENANCE
        self.assertEqual(d.status, DeviceStatus.UNDER_MAINTENANCE)

        with self.assertRaises(ValueError):
            d.status = "InvalidStatus"
        with self.assertRaises(TypeError):
            d.status = 123

    def test_years_of_use(self):
        current_year = datetime.now().year
        d = DummyDevice("D01", "Tên", current_year - 3, 500000)
        self.assertEqual(d.years_of_use, 3)

    def test_equality_and_hash(self):
        d1 = DummyDevice("D01", "Thiết bị 1", 2022, 500000)
        d2 = DummyDevice("D01", "Thiết bị 1 sửa tên", 2023, 600000)
        d3 = DummyDevice("D02", "Thiết bị 2", 2022, 500000)
        self.assertEqual(d1, d2)
        self.assertNotEqual(d1, d3)
        self.assertEqual(len({d1, d2}), 1)


class TestTeachingDevice(unittest.TestCase):
    def test_teaching_device_init_and_properties(self):
        td = DummyTeachingDevice("TD01", "Thiết bị GD", 2022, 300000, max_borrow_days=2)
        self.assertEqual(td.max_borrow_days, 2)
        self.assertEqual(td.max_borrow_periods, 2)
        self.assertTrue(td.is_available())

    def test_max_borrow_days_validation(self):
        with self.assertRaises(ValueError):
            DummyTeachingDevice("TD01", "Thiết bị GD", 2022, 300000, max_borrow_days=0)
        with self.assertRaises(ValueError):
            DummyTeachingDevice("TD01", "Thiết bị GD", 2022, 300000, max_borrow_days=-1)
        with self.assertRaises(TypeError):
            DummyTeachingDevice("TD01", "Thiết bị GD", 2022, 300000, max_borrow_days="2")

    def test_status_transition_methods(self):
        td = DummyTeachingDevice("TD01", "Thiết bị GD", 2022, 300000)
        self.assertTrue(td.is_available())

        td.mark_as_borrowed()
        self.assertTrue(td.is_borrowed())
        self.assertFalse(td.is_available())

        td.mark_as_available()
        self.assertTrue(td.is_available())

        td.mark_as_under_maintenance()
        self.assertTrue(td.is_under_maintenance())

        # Kiểm tra bí danh PascalCase
        td.MarkAsAvailable()
        self.assertTrue(td.is_available())
        td.MarkAsBorrowed()
        self.assertTrue(td.is_borrowed())


class TestAirConditionerRemote(unittest.TestCase):
    def test_init_and_properties(self):
        ac = AirConditionerRemote(
            device_id="AC01",
            name="Điều khiển điều hòa Daikin",
            year_in_use=2022,
            purchase_price=200000,
            brand="Daikin",
            battery_type="AAA",
            has_screen=True,
            max_borrow_days=1,
        )
        self.assertEqual(ac.device_id, "AC01")
        self.assertEqual(ac.brand, "Daikin")
        self.assertEqual(ac.battery_type, "AAA")
        self.assertTrue(ac.has_screen)
        self.assertEqual(ac.max_borrow_days, 1)

    def test_brand_validation(self):
        with self.assertRaises(ValueError):
            AirConditionerRemote("AC01", "ĐK", 2022, 200000, brand="")

    def test_maintenance_cost_calculation(self):
        ac = AirConditionerRemote("AC01", "ĐK", datetime.now().year, 200000)
        self.assertEqual(ac.calculate_annual_maintenance_cost(), 50000.0)

        ac_old = AirConditionerRemote("AC02", "ĐK Cũ", datetime.now().year - 4, 200000)
        self.assertEqual(ac_old.calculate_annual_maintenance_cost(), 80000.0)


class TestMicrophone(unittest.TestCase):
    def test_init_and_properties(self):
        mic = Microphone(
            device_id="MIC01",
            name="Micro không dây Sony",
            year_in_use=2023,
            purchase_price=1200000,
            is_wireless=True,
            frequency_band="UHF",
            battery_type="AA",
            max_borrow_days=1,
        )
        self.assertEqual(mic.device_id, "MIC01")
        self.assertTrue(mic.is_wireless)
        self.assertEqual(mic.frequency_band, "UHF")
        self.assertEqual(mic.battery_type, "AA")
        self.assertEqual(mic.max_borrow_days, 1)

    def test_maintenance_cost_calculation(self):
        current_year = datetime.now().year
        mic_wireless = Microphone("MIC01", "Mic Không Dây", current_year, 1000000, is_wireless=True)
        self.assertEqual(mic_wireless.calculate_annual_maintenance_cost(), 180000.0)

        mic_wired = Microphone("MIC02", "Mic Có Dây", current_year, 1000000, is_wireless=False)
        self.assertEqual(mic_wired.calculate_annual_maintenance_cost(), 80000.0)


class TestProjectorRemote(unittest.TestCase):
    def test_init_and_properties(self):
        proj = ProjectorRemote(
            device_id="PR01",
            name="Điều khiển máy chiếu Panasonic",
            year_in_use=2022,
            purchase_price=300000,
            supported_projector_brand="Panasonic",
            has_laser_pointer=True,
            battery_type="AAA",
            max_borrow_days=1,
        )
        self.assertEqual(proj.device_id, "PR01")
        self.assertEqual(proj.supported_projector_brand, "Panasonic")
        self.assertTrue(proj.has_laser_pointer)
        self.assertEqual(proj.battery_type, "AAA")
        self.assertEqual(proj.max_borrow_days, 1)

    def test_maintenance_cost_calculation(self):
        current_year = datetime.now().year
        proj_with_laser = ProjectorRemote("PR01", "ĐK Máy Chiếu", current_year, 500000, has_laser_pointer=True)
        self.assertEqual(proj_with_laser.calculate_annual_maintenance_cost(), 80000.0)

        proj_without_laser = ProjectorRemote("PR02", "ĐK Máy Chiếu", current_year, 500000, has_laser_pointer=False)
        self.assertEqual(proj_without_laser.calculate_annual_maintenance_cost(), 30000.0)


if __name__ == "__main__":
    unittest.main()
