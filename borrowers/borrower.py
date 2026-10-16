from __future__ import annotations

from abc import ABC, abstractmethod


class IBorrower(ABC):
    @property
    @abstractmethod
    def borrower_id(self) -> str:
        pass

    @property
    @abstractmethod
    def full_name(self) -> str:
        pass

    @abstractmethod
    def get_maximum_devices(self) -> int:
        pass

    @property
    def BorrowerId(self) -> str:
        return self.borrower_id

    @property
    def FullName(self) -> str:
        return self.full_name

    def GetMaximumDevices(self) -> int:
        return self.get_maximum_devices()


class Borrower(IBorrower):
    def __init__(self, borrower_id: str, full_name: str) -> None:
        if not isinstance(borrower_id, str) or not borrower_id.strip():
            raise ValueError("Mã người mượn không được để trống.")
        if not isinstance(full_name, str) or not full_name.strip():
            raise ValueError("Tên người mượn không được để trống.")

        self._borrower_id: str = borrower_id.strip()
        self._full_name: str = full_name.strip()

    @property
    def borrower_id(self) -> str:
        return self._borrower_id

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Tên người mượn không được để trống.")
        self._full_name = value.strip()

    @abstractmethod
    def get_maximum_devices(self) -> int:
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IBorrower):
            return False
        return self.borrower_id == other.borrower_id

    def __hash__(self) -> int:
        return hash(self._borrower_id)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(ID: '{self.borrower_id}', Tên: '{self.full_name}', Giới hạn mượn: {self.get_maximum_devices()} thiết bị)"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id='{self.borrower_id}' name='{self.full_name}'>"
