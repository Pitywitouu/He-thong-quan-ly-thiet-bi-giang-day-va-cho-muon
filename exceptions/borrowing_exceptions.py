from __future__ import annotations

from typing import Optional

try:
    from enums.device_status import DeviceStatus
except ImportError:
    from ..enums.device_status import DeviceStatus


class BorrowingException(Exception):
    def __init__(self, message: str, inner_exception: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.message = message
        self.inner_exception = inner_exception


class DeviceUnavailableException(BorrowingException):
    def __init__(
        self,
        device_id: str,
        current_status: DeviceStatus,
        message: Optional[str] = None,
    ) -> None:
        self.device_id = device_id
        self.current_status = current_status
        msg = (
            message
            or f"Thiết bị '{device_id}' hiện không ở trạng thái sẵn sàng (Trạng thái hiện tại: {current_status.value})."
        )
        super().__init__(msg)

    @property
    def DeviceId(self) -> str:
        return self.device_id

    @property
    def CurrentStatus(self) -> DeviceStatus:
        return self.current_status


class BorrowLimitExceededException(BorrowingException):
    def __init__(
        self,
        borrower_id: str,
        maximum_devices: int,
        message: Optional[str] = None,
    ) -> None:
        self.borrower_id = borrower_id
        self.maximum_devices = maximum_devices
        msg = (
            message
            or f"Người mượn '{borrower_id}' đã đạt số lượng thiết bị tối đa cho phép ({maximum_devices} thiết bị)."
        )
        super().__init__(msg)

    @property
    def BorrowerId(self) -> str:
        return self.borrower_id

    @property
    def MaximumDevices(self) -> int:
        return self.maximum_devices


class InvalidBorrowPeriodException(BorrowingException):
    def __init__(
        self,
        device_id: str,
        requested_days: int,
        max_days: int,
        message: Optional[str] = None,
    ) -> None:
        self.device_id = device_id
        self.requested_days = requested_days
        self.max_days = max_days
        msg = (
            message
            or f"Thời gian mượn {requested_days} ngày không hợp lệ cho thiết bị '{device_id}' (Tối đa: {max_days} ngày)."
        )
        super().__init__(msg)

    @property
    def DeviceId(self) -> str:
        return self.device_id

    @property
    def RequestedDays(self) -> int:
        return self.requested_days

    @property
    def MaxDays(self) -> int:
        return self.max_days


class DuplicateDeviceException(BorrowingException):
    def __init__(self, device_id: str, message: Optional[str] = None) -> None:
        self.device_id = device_id
        msg = message or f"Thiết bị '{device_id}' đã tồn tại trong phiếu mượn."
        super().__init__(msg)

    @property
    def DeviceId(self) -> str:
        return self.device_id


class DeviceNotInSlipException(BorrowingException):
    def __init__(self, device_id: str, message: Optional[str] = None) -> None:
        self.device_id = device_id
        msg = message or f"Thiết bị '{device_id}' không thuộc phiếu mượn này."
        super().__init__(msg)

    @property
    def DeviceId(self) -> str:
        return self.device_id


class DeviceAlreadyReturnedException(BorrowingException):
    def __init__(self, device_id: str, message: Optional[str] = None) -> None:
        self.device_id = device_id
        msg = message or f"Thiết bị '{device_id}' trong phiếu mượn đã được trả trước đó."
        super().__init__(msg)

    @property
    def DeviceId(self) -> str:
        return self.device_id
