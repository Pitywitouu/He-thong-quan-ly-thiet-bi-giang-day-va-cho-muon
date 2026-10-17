from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from enums.device_status import DeviceStatus
from exceptions.borrowing_exceptions import (
    BorrowingException,
    DeviceUnavailableException,
    BorrowLimitExceededException,
    InvalidBorrowPeriodException,
    DuplicateDeviceException,
    DeviceNotInSlipException,
    DeviceAlreadyReturnedException,
)


class TestBorrowingExceptionsHierarchy(unittest.TestCase):
    def test_base_borrowing_exception(self):
        self.assertTrue(issubclass(BorrowingException, Exception))
        inner = ValueError("Lỗi gốc")
        ex = BorrowingException("Lỗi mượn thiết bị", inner_exception=inner)
        self.assertEqual(str(ex), "Lỗi mượn thiết bị")
        self.assertEqual(ex.message, "Lỗi mượn thiết bị")
        self.assertEqual(ex.inner_exception, inner)

    def test_device_unavailable_exception(self):
        self.assertTrue(issubclass(DeviceUnavailableException, BorrowingException))
        ex = DeviceUnavailableException(device_id="AC01", current_status=DeviceStatus.UNDER_MAINTENANCE)
        self.assertEqual(ex.device_id, "AC01")
        self.assertEqual(ex.current_status, DeviceStatus.UNDER_MAINTENANCE)
        self.assertEqual(ex.DeviceId, "AC01")
        self.assertEqual(ex.CurrentStatus, DeviceStatus.UNDER_MAINTENANCE)
        self.assertIn("AC01", str(ex))
        self.assertIn("UnderMaintenance", str(ex))

    def test_borrow_limit_exceeded_exception(self):
        self.assertTrue(issubclass(BorrowLimitExceededException, BorrowingException))
        ex = BorrowLimitExceededException(borrower_id="TA01", maximum_devices=2)
        self.assertEqual(ex.borrower_id, "TA01")
        self.assertEqual(ex.maximum_devices, 2)
        self.assertEqual(ex.BorrowerId, "TA01")
        self.assertEqual(ex.MaximumDevices, 2)
        self.assertIn("TA01", str(ex))
        self.assertIn("2", str(ex))

    def test_invalid_borrow_period_exception(self):
        self.assertTrue(issubclass(InvalidBorrowPeriodException, BorrowingException))
        ex = InvalidBorrowPeriodException(device_id="MIC01", requested_days=3, max_days=1)
        self.assertEqual(ex.device_id, "MIC01")
        self.assertEqual(ex.requested_days, 3)
        self.assertEqual(ex.max_days, 1)
        self.assertEqual(ex.DeviceId, "MIC01")
        self.assertEqual(ex.RequestedDays, 3)
        self.assertEqual(ex.MaxDays, 1)
        self.assertIn("MIC01", str(ex))
        self.assertIn("3", str(ex))
        self.assertIn("1", str(ex))

    def test_duplicate_device_exception(self):
        self.assertTrue(issubclass(DuplicateDeviceException, BorrowingException))
        ex = DuplicateDeviceException(device_id="MIC01")
        self.assertEqual(ex.device_id, "MIC01")
        self.assertEqual(ex.DeviceId, "MIC01")
        self.assertIn("MIC01", str(ex))

    def test_device_not_in_slip_exception(self):
        self.assertTrue(issubclass(DeviceNotInSlipException, BorrowingException))
        ex = DeviceNotInSlipException(device_id="PR01")
        self.assertEqual(ex.device_id, "PR01")
        self.assertEqual(ex.DeviceId, "PR01")
        self.assertIn("PR01", str(ex))

    def test_device_already_returned_exception(self):
        self.assertTrue(issubclass(DeviceAlreadyReturnedException, BorrowingException))
        ex = DeviceAlreadyReturnedException(device_id="MIC01")
        self.assertEqual(ex.device_id, "MIC01")
        self.assertEqual(ex.DeviceId, "MIC01")
        self.assertIn("MIC01", str(ex))

    def test_polymorphic_catch_by_base_exception(self):
        exceptions_to_test = [
            DeviceUnavailableException("D01", DeviceStatus.BORROWED),
            BorrowLimitExceededException("B01", 3),
            InvalidBorrowPeriodException("D01", 5, 2),
            DuplicateDeviceException("D01"),
            DeviceNotInSlipException("D01"),
            DeviceAlreadyReturnedException("D01"),
        ]

        for ex in exceptions_to_test:
            caught = False
            try:
                raise ex
            except BorrowingException:
                caught = True
            self.assertTrue(caught, f"Ngoại lệ {type(ex).__name__} không được bắt bởi BorrowingException.")


if __name__ == "__main__":
    unittest.main()
