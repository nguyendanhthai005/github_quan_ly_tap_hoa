"""
=======================================================
  BÀI TẬP LỚN: QUẢN LÝ TẠP HÓA
=======================================================
  Môn học : Lập trình Python
  Nhóm    : 4 thành viên
    - Nguyễn Văn T  (nhóm trưởng) - TrangDanhSach
    - Trần Thị B                   - TrangThem
    - Lê Văn C                     - TrangSua
    - Phạm Thị D                   - Model & CSV

  Mô tả   : Ứng dụng quản lý tạp hóa gồm các chức năng:
              + Xem danh sách sản phẩm
              + Thêm sản phẩm mới
              + Sửa thông tin sản phẩm
              + Xóa sản phẩm
              + Tìm kiếm sản phẩm
              + Xem thống kê kho hàng
  Công cụ : Python 3.x + tkinter (giao diện) + CSV (lưu trữ)
=======================================================
"""

import sys
import os

# Đảm bảo Python tìm đúng thư mục gốc khi chạy từ PyCharm
sys.path.insert(0, os.path.dirname(__file__))

from app_manager import AppManager
from page.sanpham_page import TrangDanhSach
from page.themsanpham import TrangThem
from page.suasanpham import TrangSua


def main():
    # 1. Tạo AppManager (cửa sổ chính)
    app = AppManager()

    # 2. Tạo các trang và đăng ký vào app
    trang_ds = TrangDanhSach(app.root, app)
    trang_them = TrangThem(app.root, app)
    trang_sua = TrangSua(app.root, app)

    app.them_trang("danh_sach", trang_ds)
    app.them_trang("them", trang_them)
    app.them_trang("sua", trang_sua)

    # 3. Hiện trang đầu tiên
    app.hien_trang("danh_sach")

    # 4. Chạy ứng dụng
    app.chay()


if __name__ == "__main__":
    main()
