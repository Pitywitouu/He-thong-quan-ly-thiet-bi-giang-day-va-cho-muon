from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional, Sequence, Union

try:
    from borrowers.borrower import IBorrower
    from devices.teaching_device import TeachingDevice
    from borrowing.borrow_item import BorrowItem
    from exceptions.borrowing_exceptions import (
        BorrowingException,
        DeviceUnavailableException,
        BorrowLimitExceededException,
        InvalidBorrowPeriodException,
        DuplicateDeviceException,
        DeviceNotInSlipException,
        DeviceAlreadyReturnedException,
    )
except ImportError:
    from ..borrowers.borrower import IBorrower
    from ..devices.teaching_device import TeachingDevice
    from .borrow_item import BorrowItem
    from ..exceptions.borrowing_exceptions import (
        BorrowingException,
        DeviceUnavailableException,
        BorrowLimitExceededException,
        InvalidBorrowPeriodException,
        DuplicateDeviceException,
        DeviceNotInSlipException,
        DeviceAlreadyReturnedException,
    )


class BorrowingSlip:
    DEFAULT_DAILY_LATE_FEE: float = 20000.0

    def __init__(
        self,
        slip_id: str,
        borrower: IBorrower,
        teaching_room: str,
        borrowed_date: Optional[datetime] = None,
    ) -> None:
        if not isinstance(slip_id, str) or not slip_id.strip():
            raise ValueError("Mã phiếu mượn (SlipId) không được để trống.")
        if borrower is None:
            raise ValueError("Người mượn (Borrower) không được null.")
        if not isinstance(borrower, IBorrower):
            raise TypeError("Người mượn phải thực thi giao diện IBorrower.")
        if not isinstance(teaching_room, str) or not teaching_room.strip():
            raise ValueError("Phòng giảng dạy (TeachingRoom) không được để trống.")

        self._slip_id: str = slip_id.strip()
        self._borrower: IBorrower = borrower
        self._teaching_room: str = teaching_room.strip()
        self._borrowed_date: datetime = borrowed_date if borrowed_date is not None else datetime.now()
        self._items: List[BorrowItem] = []

    @property
    def slip_id(self) -> str:
        return self._slip_id

    @property
    def SlipId(self) -> str:
        return self._slip_id

    @property
    def borrower(self) -> IBorrower:
        """Người mượn thiết bị."""
        return self._borrower

    @property
    def Borrower(self) -> IBorrower:
        return self._borrower

    @property
    def teaching_room(self) -> str:
        return self._teaching_room

    @property
    def TeachingRoom(self) -> str:
        return self._teaching_room

    @property
    def borrowed_date(self) -> datetime:
        return self._borrowed_date

    @property
    def BorrowedDate(self) -> datetime:
        return self._borrowed_date

    @property
    def items(self) -> Sequence[BorrowItem]:
        return tuple(self._items)

    @property
    def Items(self) -> Sequence[BorrowItem]:
        return tuple(self._items)

    def validate_borrowing(self, device: TeachingDevice, borrow_days: int) -> None:
        # 1. Device không được null
        if device is None:
            raise ValueError("Thiết bị không được null.")
        if not isinstance(device, TeachingDevice):
            raise TypeError("Thiết bị mượn phải là đối tượng TeachingDevice.")

        # 2. borrowDays phải lớn hơn 0 và không vượt quá giới hạn thiết bị
        if isinstance(borrow_days, bool) or not isinstance(borrow_days, int) or borrow_days <= 0:
            raise InvalidBorrowPeriodException(
                device_id=device.device_id,
                requested_days=borrow_days if isinstance(borrow_days, int) else 0,
                max_days=device.max_borrow_days,
                message=f"Số ngày mượn ({borrow_days}) phải là số nguyên dương lớn hơn 0.",
            )
        if borrow_days > device.max_borrow_days:
            raise InvalidBorrowPeriodException(
                device_id=device.device_id,
                requested_days=borrow_days,
                max_days=device.max_borrow_days,
                message=(
                    f"Số ngày mượn ({borrow_days}) vượt quá giới hạn tối đa cho phép "
                    f"của thiết bị '{device.device_id}' ({device.max_borrow_days} ngày)."
                ),
            )

        # 3. Thiết bị chưa tồn tại trong phiếu
        if any(item.device.device_id == device.device_id for item in self._items):
            raise DuplicateDeviceException(device.device_id)

        # 4. Người mượn chưa đạt giới hạn thiết bị
        max_devices = self._borrower.get_maximum_devices()
        if len(self._items) >= max_devices:
            raise BorrowLimitExceededException(
                borrower_id=self._borrower.borrower_id,
                maximum_devices=max_devices,
            )

        # 5. Thiết bị đang ở trạng thái Available
        if not device.is_available():
            raise DeviceUnavailableException(
                device_id=device.device_id,
                current_status=device.status,
            )

    def add_device(self, device: TeachingDevice, borrow_days: int = 1) -> None:
        self.validate_borrowing(device=device, borrow_days=borrow_days)

        due_date = self._borrowed_date + timedelta(days=borrow_days)
        item = BorrowItem(
            device=device,
            borrowed_date=self._borrowed_date,
            due_date=due_date,
        )
        device.mark_as_borrowed()
        self._items.append(item)

    def AddDevice(self, device: TeachingDevice, borrow_days: int = 1) -> None:
        self.add_device(device=device, borrow_days=borrow_days)

    def return_device(self, device_id: str, returned_date: datetime) -> float:
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("Mã thiết bị không được để trống.")
        clean_id = device_id.strip()

        target_item: Optional[BorrowItem] = None
        for item in self._items:
            if item.device.device_id == clean_id:
                target_item = item
                break

        if target_item is None:
            raise DeviceNotInSlipException(clean_id)

        if target_item.is_returned:
            raise DeviceAlreadyReturnedException(clean_id)

        if not isinstance(returned_date, datetime):
            raise TypeError("Ngày trả phải là kiểu datetime hợp lệ.")

        if returned_date < target_item.borrowed_date:
            raise BorrowingException(
                f"Ngày trả ({returned_date.strftime('%Y-%m-%d')}) "
                f"không được trước ngày mượn ({target_item.borrowed_date.strftime('%Y-%m-%d')})."
            )

        # Ghi nhận trả và cập nhật trạng thái thiết bị
        target_item.return_item(returned_date)
        target_item.device.mark_as_available()

        # Tính tiền phạt trễ hạn của thiết bị này
        return target_item.calculate_late_fee(daily_fee=self.DEFAULT_DAILY_LATE_FEE)

    def ReturnDevice(self, device_id: str, returned_date: datetime) -> float:
        return self.return_device(device_id=device_id, returned_date=returned_date)

    def calculate_total_late_fee(self) -> float:
        return sum(item.calculate_late_fee(daily_fee=self.DEFAULT_DAILY_LATE_FEE) for item in self._items)

    def CalculateTotalLateFee(self) -> float:
        return self.calculate_total_late_fee()

    def has_unreturned_devices(self) -> bool:
        return any(not item.is_returned for item in self._items)

    def has_overdue_devices(self, as_of_date: Optional[datetime] = None) -> bool:
        return self.calculate_total_late_fee() > 0 or any(
            not item.is_returned and (as_of_date or datetime.now()) > item.due_date
            for item in self._items
        )

    def __str__(self) -> str:
        returned_count = sum(1 for item in self._items if item.is_returned)
        total_count = len(self._items)
        return (
            f"BorrowingSlip(Mã phiếu: '{self._slip_id}', Người mượn: {self._borrower.full_name}, "
            f"Phòng: '{self._teaching_room}', Ngày mượn: {self._borrowed_date.strftime('%Y-%m-%d')}, "
            f"Thiết bị: {returned_count}/{total_count} đã trả, Phạt trễ: {self.calculate_total_late_fee():,.0f} VND)"
        )

    def __repr__(self) -> str:
        return f"<BorrowingSlip id='{self._slip_id}' borrower='{self._borrower.borrower_id}' items_count={len(self._items)}>"
