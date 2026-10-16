from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Union

try:
    from devices.teaching_device import TeachingDevice
    from exceptions.borrowing_exceptions import (
        DeviceAlreadyReturnedException,
        BorrowingException,
    )
except ImportError:
    from ..devices.teaching_device import TeachingDevice
    from ..exceptions.borrowing_exceptions import (
        DeviceAlreadyReturnedException,
        BorrowingException,
    )


class BorrowItem:
    def __init__(
        self,
        device: TeachingDevice,
        borrowed_date: Optional[datetime] = None,
        due_date: Optional[datetime] = None,
        from_period: Optional[int] = None,
        to_period: Optional[int] = None,
    ) -> None:
        if device is None:
            raise ValueError("Thiết bị mượn không được null.")
        if not isinstance(device, TeachingDevice):
            raise TypeError("Thiết bị phải là một đối tượng kế thừa từ TeachingDevice.")

        self._device: TeachingDevice = device
        self._borrowed_date: datetime = borrowed_date if borrowed_date is not None else datetime.now()

        if due_date is not None:
            if due_date < self._borrowed_date:
                raise ValueError("Hạn trả (DueDate) phải sau hoặc bằng ngày mượn (BorrowedDate).")
            self._due_date: datetime = due_date
        else:
            self._due_date = self._borrowed_date + timedelta(days=device.max_borrow_days)

        self._from_period: Optional[int] = None
        self._to_period: Optional[int] = None
        if from_period is not None or to_period is not None:
            self.set_periods(from_period, to_period)

        self._returned_date: Optional[datetime] = None

    @property
    def device(self) -> TeachingDevice:
        return self._device

    @property
    def Device(self) -> TeachingDevice:
        return self._device

    @property
    def borrowed_date(self) -> datetime:
        return self._borrowed_date

    @property
    def BorrowedDate(self) -> datetime:
        return self._borrowed_date

    @property
    def due_date(self) -> datetime:
        return self._due_date

    @property
    def DueDate(self) -> datetime:
        return self._due_date

    @property
    def from_period(self) -> Optional[int]:
        return self._from_period

    @from_period.setter
    def from_period(self, value: Optional[int]) -> None:
        self.set_periods(value, self._to_period)

    @property
    def fromPeriod(self) -> Optional[int]:
        return self._from_period

    @fromPeriod.setter
    def fromPeriod(self, value: Optional[int]) -> None:
        self.from_period = value

    @property
    def to_period(self) -> Optional[int]:
        return self._to_period

    @to_period.setter
    def to_period(self, value: Optional[int]) -> None:
        self.set_periods(self._from_period, value)

    @property
    def toPeriod(self) -> Optional[int]:
        return self._to_period

    @toPeriod.setter
    def toPeriod(self, value: Optional[int]) -> None:
        self.to_period = value

    def set_periods(self, from_period: Optional[int], to_period: Optional[int]) -> None:
        if from_period is not None:
            if isinstance(from_period, bool) or not isinstance(from_period, int) or from_period <= 0:
                raise ValueError("Tiết bắt đầu (from_period) phải là số nguyên dương lớn hơn 0.")
        if to_period is not None:
            if isinstance(to_period, bool) or not isinstance(to_period, int) or to_period <= 0:
                raise ValueError("Tiết kết thúc (to_period) phải là số nguyên dương lớn hơn 0.")

        if from_period is not None and to_period is not None and to_period < from_period:
            raise ValueError(f"Tiết kết thúc ({to_period}) không được nhỏ hơn tiết bắt đầu ({from_period}).")

        self._from_period = from_period
        self._to_period = to_period

    @property
    def returned_date(self) -> Optional[datetime]:
        return self._returned_date

    @property
    def ReturnedDate(self) -> Optional[datetime]:
        return self._returned_date

    @property
    def is_returned(self) -> bool:
        return self._returned_date is not None

    @property
    def IsReturned(self) -> bool:
        return self.is_returned

    def return_item(self, returned_date: datetime) -> None:
        if self.is_returned:
            raise DeviceAlreadyReturnedException(self._device.device_id)

        if not isinstance(returned_date, datetime):
            raise TypeError("Ngày trả phải là đối tượng datetime hợp lệ.")

        if returned_date < self._borrowed_date:
            raise BorrowingException(
                f"Ngày trả ({returned_date.strftime('%Y-%m-%d')}) không được trước ngày mượn ({self._borrowed_date.strftime('%Y-%m-%d')})."
            )

        self._returned_date = returned_date

    def Return(self, returned_date: datetime) -> None:
        self.return_item(returned_date)

    def calculate_late_fee(self, daily_fee: float = 20000.0) -> float:
        end_date = self._returned_date or datetime.now()
        late_days = (end_date.date() - self._due_date.date()).days
        if late_days > 0:
            return float(late_days * daily_fee)
        return 0.0

    def __str__(self) -> str:
        status_str = f"Đã trả lúc {self._returned_date.strftime('%Y-%m-%d %H:%M')}" if self.is_returned else "Chưa trả"
        period_str = f", Tiết: {self._from_period}->{self._to_period}" if self._from_period and self._to_period else ""
        return (
            f"BorrowItem(Thiết bị: [{self._device.device_id}] {self._device.name}, "
            f"Mượn: {self._borrowed_date.strftime('%Y-%m-%d')}, Hạn: {self._due_date.strftime('%Y-%m-%d')}"
            f"{period_str}, {status_str})"
        )

    def __repr__(self) -> str:
        return (
            f"<BorrowItem device='{self._device.device_id}' "
            f"borrowed='{self._borrowed_date.strftime('%Y-%m-%d')}' is_returned={self.is_returned}>"
        )
