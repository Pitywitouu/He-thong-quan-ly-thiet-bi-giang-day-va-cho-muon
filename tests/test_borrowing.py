from __future__ import annotations

import os
import sys
import unittest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from enums.device_status import DeviceStatus
from devices.air_conditioner_remote import AirConditionerRemote
from devices.microphone import Microphone
from devices.projector_remote import ProjectorRemote
from borrowers.borrower import IBorrower, Borrower
from borrowers.lecturer import Lecturer
from borrowers.teaching_assistant import TeachingAssistant
from borrowing.borrow_item import BorrowItem
from borrowing.borrowing_slip import BorrowingSlip
from exceptions.borrowing_exceptions import (
    BorrowingException,
    DeviceUnavailableException,
    BorrowLimitExceededException,
    InvalidBorrowPeriodException,
    DuplicateDeviceException,
    DeviceNotInSlipException,
    DeviceAlreadyReturnedException,
)


class TestBorrowers(unittest.TestCase):
    def test_lecturer_properties_and_limit(self):
        lec = Lecturer(
            borrower_id="GV01",
            full_name="Nguyễn Văn A",
            department="Khoa CNTT",
            academic_title="Tiến sĩ",
        )
        self.assertEqual(lec.borrower_id, "GV01")
        self.assertEqual(lec.full_name, "Nguyễn Văn A")
        self.assertEqual(lec.get_maximum_devices(), 3)
        self.assertEqual(lec.department, "Khoa CNTT")
        self.assertEqual(lec.academic_title, "Tiến sĩ")
        self.assertIsInstance(lec, IBorrower)

    def test_teaching_assistant_properties_and_limit(self):
        ta = TeachingAssistant(
            borrower_id="TG01",
            full_name="Trần Thị B",
            assigned_course="Lập trình hướng đối tượng",
        )
        self.assertEqual(ta.borrower_id, "TG01")
        self.assertEqual(ta.full_name, "Trần Thị B")
        self.assertEqual(ta.get_maximum_devices(), 2)
        self.assertEqual(ta.assigned_course, "Lập trình hướng đối tượng")
        self.assertIsInstance(ta, IBorrower)

    def test_borrower_validation(self):
        with self.assertRaises(ValueError):
            Lecturer("", "Tên GV")
        with self.assertRaises(ValueError):
            Lecturer("GV01", "")
        with self.assertRaises(ValueError):
            TeachingAssistant("", "Tên TG")
        with self.assertRaises(ValueError):
            TeachingAssistant("TG01", "   ")


class TestBorrowItem(unittest.TestCase):
    def setUp(self):
        self.mic = Microphone("MIC01", "Micro", 2023, 1000000, max_borrow_days=1)
        self.base_time = datetime(2026, 10, 10, 8, 0, 0)

    def test_valid_creation(self):
        item = BorrowItem(
            device=self.mic,
            borrowed_date=self.base_time,
            due_date=self.base_time + timedelta(days=1),
            from_period=1,
            to_period=3,
        )
        self.assertEqual(item.device, self.mic)
        self.assertEqual(item.borrowed_date, self.base_time)
        self.assertEqual(item.due_date, self.base_time + timedelta(days=1))
        self.assertEqual(item.from_period, 1)
        self.assertEqual(item.to_period, 3)
        self.assertFalse(item.is_returned)
        self.assertIsNone(item.returned_date)

    def test_null_device_raises(self):
        with self.assertRaises(ValueError):
            BorrowItem(device=None)

    def test_period_validation(self):
        with self.assertRaises(ValueError):
            BorrowItem(self.mic, from_period=0, to_period=3)
        with self.assertRaises(ValueError):
            BorrowItem(self.mic, from_period=4, to_period=2)

    def test_return_item_success(self):
        item = BorrowItem(self.mic, borrowed_date=self.base_time)
        return_time = self.base_time + timedelta(days=1)
        item.return_item(return_time)
        self.assertTrue(item.is_returned)
        self.assertEqual(item.returned_date, return_time)

    def test_return_item_twice_raises(self):
        item = BorrowItem(self.mic, borrowed_date=self.base_time)
        item.return_item(self.base_time + timedelta(days=1))
        with self.assertRaises(DeviceAlreadyReturnedException):
            item.return_item(self.base_time + timedelta(days=2))

    def test_return_before_borrow_raises(self):
        item = BorrowItem(self.mic, borrowed_date=self.base_time)
        invalid_return = self.base_time - timedelta(days=1)
        with self.assertRaises(BorrowingException):
            item.return_item(invalid_return)

    def test_late_fee_calculation(self):
        item = BorrowItem(
            self.mic,
            borrowed_date=self.base_time,
            due_date=self.base_time + timedelta(days=1),
        )
        return_time = self.base_time + timedelta(days=3)
        item.return_item(return_time)
        self.assertEqual(item.calculate_late_fee(daily_fee=20000.0), 40000.0)


class TestBorrowingWorkflow(unittest.TestCase):
    def setUp(self):
        self.lecturer = Lecturer("GV01", "Thầy Hoàng")
        self.ta = TeachingAssistant("TA01", "Cô Lan")
        self.proj_remote = ProjectorRemote("PR01", "ĐK Máy Chiếu Sony", 2022, 500000, max_borrow_days=2)
        self.ac_remote = AirConditionerRemote("AC01", "ĐK Điều Hòa Daikin", 2022, 300000, max_borrow_days=1)
        self.mic = Microphone("MIC01", "Micro Không Dây", 2023, 1500000, is_wireless=True, max_borrow_days=1)
        self.base_time = datetime(2026, 10, 16, 7, 30, 0)

    def test_section_11_1_successful_workflow(self):
        slip = BorrowingSlip("PH001", self.lecturer, "Phòng A.203", borrowed_date=self.base_time)

        # 4. Thêm điều khiển máy chiếu (mượn 2 ngày) và micro (mượn 1 ngày)
        slip.add_device(self.proj_remote, borrow_days=2)
        slip.add_device(self.mic, borrow_days=1)

        self.assertEqual(len(slip.items), 2)
        self.assertTrue(self.proj_remote.is_borrowed())
        self.assertTrue(self.mic.is_borrowed())

        # 5. Trả điều khiển máy chiếu đúng hạn (sau 2 ngày)
        proj_return_time = self.base_time + timedelta(days=2)
        proj_fee = slip.return_device("PR01", proj_return_time)
        self.assertEqual(proj_fee, 0.0)
        self.assertTrue(self.proj_remote.is_available())

        # 6. Trả micro muộn 2 ngày (hạn là 1 ngày, trả sau 3 ngày)
        mic_return_time = self.base_time + timedelta(days=3)
        mic_fee = slip.return_device("MIC01", mic_return_time)
        # Phạt 2 ngày muộn * 20,000 VND = 40,000 VND
        self.assertEqual(mic_fee, 40000.0)
        self.assertTrue(self.mic.is_available())

        # 7. Kiểm tra tổng phí phạt
        self.assertEqual(slip.calculate_total_late_fee(), 40000.0)
        self.assertFalse(slip.has_unreturned_devices())

    def test_section_11_2_under_maintenance_raises(self):
        # 1. Mượn điều khiển điều hòa đang UnderMaintenance
        self.ac_remote.mark_as_under_maintenance()
        slip = BorrowingSlip("PH002", self.lecturer, "Phòng B.101", borrowed_date=self.base_time)
        with self.assertRaises(DeviceUnavailableException) as ctx:
            slip.add_device(self.ac_remote, borrow_days=1)
        self.assertEqual(ctx.exception.device_id, "AC01")
        self.assertEqual(ctx.exception.current_status, DeviceStatus.UNDER_MAINTENANCE)
        self.assertTrue(self.ac_remote.is_under_maintenance())
        self.assertEqual(len(slip.items), 0)

    def test_section_11_2_borrow_limit_exceeded_raises(self):
        # 2. Trợ giảng mượn thiết bị thứ ba (giới hạn là 2)
        slip = BorrowingSlip("PH003", self.ta, "Phòng C.301", borrowed_date=self.base_time)
        slip.add_device(self.proj_remote, borrow_days=1)
        slip.add_device(self.mic, borrow_days=1)

        with self.assertRaises(BorrowLimitExceededException) as ctx:
            slip.add_device(self.ac_remote, borrow_days=1)
        self.assertEqual(ctx.exception.borrower_id, "TA01")
        self.assertEqual(ctx.exception.maximum_devices, 2)
        self.assertTrue(self.ac_remote.is_available())
        self.assertEqual(len(slip.items), 2)

    def test_section_11_2_duplicate_device_raises(self):
        # 3. Thêm cùng một micro hai lần
        slip = BorrowingSlip("PH004", self.lecturer, "Phòng D.401", borrowed_date=self.base_time)
        slip.add_device(self.mic, borrow_days=1)

        with self.assertRaises(DuplicateDeviceException) as ctx:
            slip.add_device(self.mic, borrow_days=1)
        self.assertEqual(ctx.exception.device_id, "MIC01")
        self.assertEqual(len(slip.items), 1)

    def test_section_11_2_invalid_borrow_period_raises(self):
        # 4. Mượn micro trong 3 ngày dù giới hạn là 1 ngày
        slip = BorrowingSlip("PH005", self.lecturer, "Phòng E.501", borrowed_date=self.base_time)
        with self.assertRaises(InvalidBorrowPeriodException) as ctx:
            slip.add_device(self.mic, borrow_days=3)
        self.assertEqual(ctx.exception.device_id, "MIC01")
        self.assertEqual(ctx.exception.requested_days, 3)
        self.assertEqual(ctx.exception.max_days, 1)
        self.assertTrue(self.mic.is_available())
        self.assertEqual(len(slip.items), 0)

    def test_section_11_2_device_not_in_slip_raises(self):
        # 5. Trả một điều khiển máy chiếu không thuộc phiếu
        slip = BorrowingSlip("PH006", self.lecturer, "Phòng A.101", borrowed_date=self.base_time)
        slip.add_device(self.mic, borrow_days=1)

        with self.assertRaises(DeviceNotInSlipException) as ctx:
            slip.return_device("PR01", self.base_time + timedelta(days=1))
        self.assertEqual(ctx.exception.device_id, "PR01")

    def test_section_11_2_device_already_returned_raises(self):
        # 6. Trả cùng một thiết bị hai lần
        slip = BorrowingSlip("PH007", self.lecturer, "Phòng A.101", borrowed_date=self.base_time)
        slip.add_device(self.mic, borrow_days=1)
        slip.return_device("MIC01", self.base_time + timedelta(days=1))

        with self.assertRaises(DeviceAlreadyReturnedException) as ctx:
            slip.return_device("MIC01", self.base_time + timedelta(days=1))
        self.assertEqual(ctx.exception.device_id, "MIC01")

    def test_section_11_2_return_date_before_borrow_raises(self):
        # 7. Trả thiết bị với ngày trả trước ngày mượn
        slip = BorrowingSlip("PH008", self.lecturer, "Phòng A.101", borrowed_date=self.base_time)
        slip.add_device(self.mic, borrow_days=1)

        with self.assertRaises(BorrowingException):
            slip.return_device("MIC01", self.base_time - timedelta(days=1))
        self.assertTrue(self.mic.is_borrowed())


if __name__ == "__main__":
    unittest.main()
