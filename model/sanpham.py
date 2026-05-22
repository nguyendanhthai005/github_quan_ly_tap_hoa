import csv
import os

# Đường dẫn tới file dữ liệu CSV
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sanpham.csv")

# Các cột trong file CSV
FIELDNAMES = ["id", "ten_sp", "loai", "gia", "so_luong", "nha_cung_cap"]


class SanPham:
    """
    Class đại diện cho một sản phẩm trong tạp hóa.
    Mỗi đối tượng SanPham lưu thông tin 1 sản phẩm.
    """

    def __init__(self, id, ten_sp, loai, gia, so_luong, nha_cung_cap):
        self.id = int(id)
        self.ten_sp = ten_sp
        self.loai = loai
        self.gia = int(gia)           # Giá tiền (VNĐ)
        self.so_luong = int(so_luong) # Số lượng tồn kho
        self.nha_cung_cap = nha_cung_cap


# ── Các hàm đọc / ghi CSV ──────────────────────────────────────────────────

def doc_du_lieu():
    """Đọc toàn bộ dữ liệu từ file CSV, trả về list các SanPham."""
    ds = []
    if not os.path.exists(DATA_FILE):
        return ds
    with open(DATA_FILE, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sp = SanPham(
                row["id"], row["ten_sp"], row["loai"],
                row["gia"], row["so_luong"], row["nha_cung_cap"]
            )
            ds.append(sp)
    return ds


def ghi_du_lieu(ds_sanpham):
    """Ghi toàn bộ danh sách SanPham xuống file CSV."""
    with open(DATA_FILE, encoding="utf-8", newline="") as f:
        pass  # kiểm tra file tồn tại (tạo nếu chưa có)
    with open(DATA_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for sp in ds_sanpham:
            writer.writerow({
                "id": sp.id,
                "ten_sp": sp.ten_sp,
                "loai": sp.loai,
                "gia": sp.gia,
                "so_luong": sp.so_luong,
                "nha_cung_cap": sp.nha_cung_cap,
            })


def sinh_id_moi():
    """Tạo ID tự động (lấy ID lớn nhất + 1)."""
    ds = doc_du_lieu()
    if not ds:
        return 1
    return max(sp.id for sp in ds) + 1


def them_san_pham(ten_sp, loai, gia, so_luong, nha_cung_cap):
    """Thêm một sản phẩm mới vào danh sách và lưu xuống CSV."""
    ds = doc_du_lieu()
    sp_moi = SanPham(sinh_id_moi(), ten_sp, loai, gia, so_luong, nha_cung_cap)
    ds.append(sp_moi)
    ghi_du_lieu(ds)
    return sp_moi


def sua_san_pham(id_can_sua, ten_sp, loai, gia, so_luong, nha_cung_cap):
    """Cập nhật thông tin sản phẩm theo ID."""
    ds = doc_du_lieu()
    for sp in ds:
        if sp.id == int(id_can_sua):
            sp.ten_sp = ten_sp
            sp.loai = loai
            sp.gia = int(gia)
            sp.so_luong = int(so_luong)
            sp.nha_cung_cap = nha_cung_cap
            break
    ghi_du_lieu(ds)


def xoa_san_pham(id_can_xoa):
    """Xóa sản phẩm theo ID."""
    ds = doc_du_lieu()
    ds = [sp for sp in ds if sp.id != int(id_can_xoa)]
    ghi_du_lieu(ds)


def tim_kiem(tu_khoa):
    """Tìm kiếm sản phẩm theo tên (không phân biệt hoa/thường)."""
    ds = doc_du_lieu()
    tu_khoa = tu_khoa.lower()
    return [sp for sp in ds if tu_khoa in sp.ten_sp.lower()]
