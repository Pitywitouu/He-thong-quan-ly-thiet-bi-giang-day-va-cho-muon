from __future__ import annotations

from typing import Optional

try:
    from borrowers.borrower import Borrower, IBorrower
except ImportError:
    from .borrower import Borrower, IBorrower


class Lecturer(Borrower):
    MAX_DEVICES: int = 3

    def __init__(
        self,
        borrower_id: str,
        full_name: str,
        department: str = "",
        academic_title: str = "",
    ) -> None:
        super().__init__(borrower_id=borrower_id, full_name=full_name)
        self.department = department
        self.academic_title = academic_title

    def get_maximum_devices(self) -> int:
        return self.MAX_DEVICES

    def __str__(self) -> str:
        title_info = f", Học vị: {self.academic_title}" if self.academic_title else ""
        dept_info = f", Khoa: {self.department}" if self.department else ""
        return (
            f"Lecturer(ID: '{self.borrower_id}', Tên: '{self.full_name}'"
            f"{title_info}{dept_info}, Tối đa: {self.get_maximum_devices()} thiết bị)"
        )
