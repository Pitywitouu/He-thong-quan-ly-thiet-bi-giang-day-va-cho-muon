from __future__ import annotations

from typing import Optional

try:
    from borrowers.borrower import Borrower, IBorrower
except ImportError:
    from .borrower import Borrower, IBorrower


class TeachingAssistant(Borrower):
    MAX_DEVICES: int = 2

    def __init__(
        self,
        borrower_id: str,
        full_name: str,
        assigned_course: str = "",
    ) -> None:
        super().__init__(borrower_id=borrower_id, full_name=full_name)
        self.assigned_course = assigned_course

    def get_maximum_devices(self) -> int:
        return self.MAX_DEVICES

    def __str__(self) -> str:
        course_info = f", Môn trợ giảng: {self.assigned_course}" if self.assigned_course else ""
        return (
            f"TeachingAssistant(ID: '{self.borrower_id}', Tên: '{self.full_name}'"
            f"{course_info}, Tối đa: {self.get_maximum_devices()} thiết bị)"
        )
