"""
MSSV: 202418985
Họ tên: Nguyễn Phú Thái
"""

from __future__ import annotations

from datetime import datetime, timedelta

from enums.device_status import DeviceStatus
from devices.air_conditioner_remote import AirConditionerRemote
from devices.microphone import Microphone
from devices.projector_remote import ProjectorRemote
from rooms.classroom import ClassRoom
from borrowers.lecturer import Lecturer
from borrowers.teaching_assistant import TeachingAssistant
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

def main() -> None:
    print("                         HỆ THỐNG QUẢN LÝ THIẾT BỊ GIẢNG DẠY VÀ PHIẾU MƯỢN")

    # 1. KHỞI TẠO THIẾT BỊ VÀ PHÒNG HỌC (QUAN HỆ KẾT TẬP & ĐA HÌNH)
    print("\n--- 1. Khởi tạo danh mục thiết bị và phòng học ---")
    current_year = datetime.now().year

    proj1 = ProjectorRemote("PR01", "Điều khiển máy chiếu Sony Laser", 2022, 500000, "Sony", True, "AAA", max_borrow_days=2)
    ac1 = AirConditionerRemote("AC01", "Điều khiển điều hòa Daikin Inverter", 2023, 350000, "Daikin", "AAA", True, max_borrow_days=1)
    mic1 = Microphone("MIC01", "Micro không dây Shure UHF", 2023, 1200000, is_wireless=True, frequency_band="UHF", max_borrow_days=1)
    
    # Thiết bị đang bảo trì và thiết bị cũ trên 5 năm để kiểm thử bảo trì phòng
    ac_broken = AirConditionerRemote("AC02", "Điều khiển điều hòa Panasonic", 2022, 300000, "Panasonic", status=DeviceStatus.UNDER_MAINTENANCE)
    mic_old = Microphone("MIC02", "Micro không dây Sennheiser", current_year - 6, 2000000, is_wireless=True)

    room_a = ClassRoom("P.A201", "Phòng Giảng đường A201", 60)
    room_a.add_device(proj1)
    room_a.add_device(ac1)
    room_a.add_device(mic1)
    room_a.add_device(ac_broken)
    room_a.add_device(mic_old)

    print(f"Phòng học: {room_a}")
    print(f"Tổng số thiết bị trong phòng: {len(room_a.devices)}")
    print(f"Tổng chi phí bảo trì dự kiến hàng năm (Đa hình): {room_a.calculate_annual_maintenance_cost():,.0f} VND")

    print("\nCác thiết bị trong phòng cần bảo trì (Đang bảo trì hoặc tuổi thọ > 5 năm):")
    for d in room_a.get_devices_requiring_maintenance():
        print(f"  - [{d.device_id}] {d.name} | Năm SD: {d.year_in_use} ({d.years_of_use} năm) | Trạng thái: {d.status.value}")

    # 2. KHỞI TẠO NGƯỜI MƯỢN (INTERFACE IBorrower)
    print("\n--- 2. Khởi tạo người mượn thiết bị ---")
    lecturer = Lecturer("GV001", "TS. Nguyễn Văn An", department="Khoa Công nghệ thông tin", academic_title="Tiến sĩ")
    ta = TeachingAssistant("TA001", "ThS. Lê Thị Bình", assigned_course="Lập trình hướng đối tượng")

    print(f"Giảng viên: {lecturer}")
    print(f"Trợ giảng:  {ta}")

    # 3. KỊCH BẢN KIỂM THỬ 11.1: LUỒNG NGHIỆP VỤ THÀNH CÔNG
    print("\n")
    print("                         KỊCH BẢN 11.1: LUỒNG NGHIỆP VỤ THÀNH CÔNG")
    borrow_date = datetime(2026, 10, 10, 8, 0, 0)
    slip = BorrowingSlip("PM-2026-001", lecturer, "Phòng A201", borrowed_date=borrow_date)
    print(f"[Tạo phiếu] {slip}")

    # Thêm điều khiển máy chiếu (mượn 2 ngày) và micro (mượn 1 ngày)
    print("\nThêm thiết bị vào phiếu:")
    slip.add_device(proj1, borrow_days=2)
    print(f"  + Đã thêm [{proj1.device_id}] {proj1.name} (Hạn mượn: 2 ngày). Trạng thái thiết bị: {proj1.status.value}")

    slip.add_device(mic1, borrow_days=1)
    print(f"  + Đã thêm [{mic1.device_id}] {mic1.name} (Hạn mượn: 1 ngày). Trạng thái thiết bị: {mic1.status.value}")

    print("\nChi tiết các thiết bị trong phiếu mượn:")
    for item in slip.items:
        print(f"  * {item}")

    # Trả thiết bị
    print("\nTiến hành trả thiết bị:")
    # 1. Trả điều khiển máy chiếu đúng hạn (sau 2 ngày: 2026-10-12)
    return_proj_date = borrow_date + timedelta(days=2)
    fee_proj = slip.return_device("PR01", return_proj_date)
    print(f"  -> Trả máy chiếu PR01 vào ngày {return_proj_date.strftime('%Y-%m-%d')} (Đúng hạn) - Phí phạt: {fee_proj:,.0f} VND. Trạng thái thiết bị: {proj1.status.value}")

    # 2. Trả micro muộn 2 ngày (hạn: 2026-10-11, trả ngày: 2026-10-13)
    return_mic_date = borrow_date + timedelta(days=3)
    fee_mic = slip.return_device("MIC01", return_mic_date)
    print(f"  -> Trả micro MIC01 vào ngày {return_mic_date.strftime('%Y-%m-%d')} (Muộn 2 ngày) - Phí phạt: {fee_mic:,.0f} VND. Trạng thái thiết bị: {mic1.status.value}")

    print(f"\n[Kết quả phiếu mượn]")
    print(f"  - Trạng thái phiếu: {'Tất cả đã trả' if not slip.has_unreturned_devices() else 'Còn thiết bị chưa trả'}")
    print(f"  - Tổng tiền phạt trễ hạn: {slip.calculate_total_late_fee():,.0f} VND")

    # 4. KỊCH BẢN KIỂM THỬ 11.2: LUỒNG PHÁT SINH NGOẠI LỆ (TRY - CATCH - FINALLY)
    print("\n")
    print("                         KỊCH BẢN 11.2: XỬ LÝ NGOẠI LỆ BẤT THƯỜNG (TRY - EXCEPT - FINALLY)")

    # Tình huống 1: Mượn thiết bị đang UnderMaintenance
    print("\n[Tình huống 1] Mượn điều khiển điều hòa đang ở trạng thái UnderMaintenance:")
    slip_ex1 = BorrowingSlip("PM-EX-001", lecturer, "Phòng B101", borrowed_date=borrow_date)
    try:
        slip_ex1.add_device(ac_broken, borrow_days=1)
    except DeviceUnavailableException as ex:
        print(f"  => Bắt ngoại lệ DeviceUnavailableException: {ex}")
    finally:
        print(f"  => [Tính nhất quán]: Thiết bị '{ac_broken.device_id}' vẫn giữ trạng thái: {ac_broken.status.value}")

    # Tình huống 2: Trợ giảng mượn thiết bị thứ 3 (Vượt quá giới hạn 2 thiết bị)
    print("\n[Tình huống 2] Trợ giảng mượn vượt quá số thiết bị cho phép (tối đa 2 thiết bị):")
    slip_ex2 = BorrowingSlip("PM-EX-002", ta, "Phòng B102", borrowed_date=borrow_date)
    slip_ex2.add_device(proj1, borrow_days=1)
    slip_ex2.add_device(mic1, borrow_days=1)
    try:
        slip_ex2.add_device(ac1, borrow_days=1)
    except BorrowLimitExceededException as ex:
        print(f"  => Bắt ngoại lệ BorrowLimitExceededException: {ex}")
    finally:
        print(f"  => [Tính nhất quán]: Phiếu chỉ có {len(slip_ex2.items)} thiết bị, thiết bị '{ac1.device_id}' không bị đổi thành Borrowed (Hiện tại: {ac1.status.value})")

    # Tình huống 3: Thêm cùng một micro hai lần vào phiếu
    print("\n[Tình huống 3] Thêm cùng một thiết bị hai lần vào một phiếu:")
    slip_ex3 = BorrowingSlip("PM-EX-003", lecturer, "Phòng B103", borrowed_date=borrow_date)
    # Trả lại proj1 để sẵn sàng
    proj1.mark_as_available()
    slip_ex3.add_device(proj1, borrow_days=1)
    try:
        slip_ex3.add_device(proj1, borrow_days=1)
    except DuplicateDeviceException as ex:
        print(f"  => Bắt ngoại lệ DuplicateDeviceException: {ex}")
    finally:
        print(f"  => [Tính nhất quán]: Số thiết bị trong phiếu giữ nguyên: {len(slip_ex3.items)}")

    # Tình huống 4: Mượn micro 3 ngày dù giới hạn chỉ là 1 ngày
    print("\n[Tình huống 4] Mượn thiết bị vượt quá thời hạn mượn tối đa của thiết bị:")
    slip_ex4 = BorrowingSlip("PM-EX-004", lecturer, "Phòng B104", borrowed_date=borrow_date)
    mic1.mark_as_available()
    try:
        slip_ex4.add_device(mic1, borrow_days=3)
    except InvalidBorrowPeriodException as ex:
        print(f"  => Bắt ngoại lệ InvalidBorrowPeriodException: {ex}")
    finally:
        print(f"  => [Tính nhất quán]: Thiết bị '{mic1.device_id}' vẫn sẵn sàng: {mic1.status.value}, phiếu rỗng: {len(slip_ex4.items)}")

    # Tình huống 5: Trả thiết bị không thuộc phiếu mượn
    print("\n[Tình huống 5] Yêu cầu trả một thiết bị không thuộc phiếu mượn:")
    slip_ex5 = BorrowingSlip("PM-EX-005", lecturer, "Phòng B105", borrowed_date=borrow_date)
    slip_ex5.add_device(mic1, borrow_days=1)
    try:
        slip_ex5.return_device("PR01", borrow_date + timedelta(days=1))
    except DeviceNotInSlipException as ex:
        print(f"  => Bắt ngoại lệ DeviceNotInSlipException: {ex}")

    # Tình huống 6: Trả cùng một thiết bị hai lần
    print("\n[Tình huống 6] Trả một thiết bị hai lần:")
    slip_ex6 = BorrowingSlip("PM-EX-006", lecturer, "Phòng B106", borrowed_date=borrow_date)
    ac1.mark_as_available()
    slip_ex6.add_device(ac1, borrow_days=1)
    slip_ex6.return_device("AC01", borrow_date + timedelta(days=1))
    try:
        slip_ex6.return_device("AC01", borrow_date + timedelta(days=1))
    except DeviceAlreadyReturnedException as ex:
        print(f"  => Bắt ngoại lệ DeviceAlreadyReturnedException: {ex}")

    # Tình huống 7: Trả thiết bị với ngày trả trước ngày mượn
    print("\n[Tình huống 7] Trả thiết bị với ngày trả trước ngày mượn:")
    slip_ex7 = BorrowingSlip("PM-EX-007", lecturer, "Phòng B107", borrowed_date=borrow_date)
    ac1.mark_as_available()
    slip_ex7.add_device(ac1, borrow_days=1)
    try:
        slip_ex7.return_device("AC01", borrow_date - timedelta(days=2))
    except BorrowingException as ex:
        print(f"  => Bắt ngoại lệ BorrowingException: {ex}")
    finally:
        print(f"  => [Tính nhất quán]: Thao tác trả thất bại, thiết bị '{ac1.device_id}' vẫn giữ trạng thái: {ac1.status.value}")
    
    print("\n")
    print("                         CHƯƠNG TRÌNH MÔ PHỎNG ĐÃ HOÀN THÀNH TẤT CẢ KỊCH BẢN")


if __name__ == "__main__":
    main()
