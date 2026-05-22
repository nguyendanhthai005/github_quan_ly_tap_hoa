import tkinter as tk
from tkinter import messagebox
from model.sanpham import doc_du_lieu, sua_san_pham


class TrangSua(tk.Frame):
    """
    Trang sửa thông tin sản phẩm đã có trong danh sách.
    Nhận id_sp từ TrangDanhSach để tải đúng dữ liệu.
    Thành viên phụ trách: Lê Văn C
    """

    LOAI_SP = ["Lương thực", "Gia vị", "Dầu ăn", "Mì gói", "Đồ uống",
               "Bánh kẹo", "Chăm sóc cá nhân", "Đồ gia dụng", "Khác"]

    def __init__(self, master, app):
        super().__init__(master, bg="#f0f0f0")
        self.app = app
        self.id_sp_dang_sua = None
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        # --- Tiêu đề ---
        tk.Label(
            self,
            text="✏️  SỬA THÔNG TIN SẢN PHẨM",
            font=("Arial", 16, "bold"),
            bg="#e67e22", fg="white", pady=10
        ).pack(fill="x")

        # --- Hiển thị ID (chỉ đọc) ---
        frame_id = tk.Frame(self, bg="#f0f0f0", pady=10)
        frame_id.pack()
        tk.Label(frame_id, text="ID sản phẩm:", font=("Arial", 12), bg="#f0f0f0").pack(side="left")
        self.nhan_id = tk.Label(frame_id, text="---", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#333")
        self.nhan_id.pack(side="left", padx=8)

        # --- Form sửa ---
        frame_form = tk.Frame(self, bg="#f0f0f0")
        frame_form.pack()

        nhan_cot = [
            ("Tên sản phẩm (*)", "ten_sp"),
            ("Loại sản phẩm (*)", "loai"),
            ("Giá bán (VNĐ) (*)", "gia"),
            ("Số lượng tồn kho (*)", "so_luong"),
            ("Nhà cung cấp", "nha_cung_cap"),
        ]

        self.cac_o = {}
        self.bien_loai = tk.StringVar(value=self.LOAI_SP[0])

        for i, (nhan, ten_bien) in enumerate(nhan_cot):
            tk.Label(
                frame_form, text=nhan,
                font=("Arial", 12), bg="#f0f0f0", anchor="e", width=22
            ).grid(row=i, column=0, padx=10, pady=8, sticky="e")

            if ten_bien == "loai":
                o = tk.OptionMenu(frame_form, self.bien_loai, *self.LOAI_SP)
                o.config(font=("Arial", 11), width=22, bg="white")
                o.grid(row=i, column=1, padx=10, pady=8, sticky="w")
                self.cac_o[ten_bien] = self.bien_loai
            else:
                o = tk.Entry(frame_form, font=("Arial", 12), width=25)
                o.grid(row=i, column=1, padx=10, pady=8)
                self.cac_o[ten_bien] = o

        # --- Nút bấm ---
        frame_nut = tk.Frame(self, bg="#f0f0f0")
        frame_nut.pack(pady=20)

        tk.Button(
            frame_nut, text="💾  Lưu thay đổi",
            font=("Arial", 12, "bold"), bg="#e67e22", fg="white",
            width=16, command=self._luu
        ).grid(row=0, column=0, padx=15)

        tk.Button(
            frame_nut, text="↩️  Quay lại",
            font=("Arial", 12, "bold"), bg="#888", fg="white",
            width=16, command=self._quay_lai
        ).grid(row=0, column=1, padx=15)

    # ── Tải dữ liệu sản phẩm cần sửa vào form ─────────────────────────────

    def tai_du_lieu(self, id_sp=None, **kwargs):
        """Tìm sản phẩm theo id và điền vào các ô nhập."""
        if id_sp is None:
            return

        self.id_sp_dang_sua = int(id_sp)
        self.nhan_id.config(text=str(self.id_sp_dang_sua))

        # Tìm sản phẩm trong danh sách
        ds = doc_du_lieu()
        sp = None
        for item in ds:
            if item.id == self.id_sp_dang_sua:
                sp = item
                break

        if sp is None:
            messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm!")
            self._quay_lai()
            return

        # Điền dữ liệu vào form
        self._set_entry("ten_sp", sp.ten_sp)
        self.bien_loai.set(sp.loai if sp.loai in self.LOAI_SP else self.LOAI_SP[-1])
        self._set_entry("gia", str(sp.gia))
        self._set_entry("so_luong", str(sp.so_luong))
        self._set_entry("nha_cung_cap", sp.nha_cung_cap)

    def _set_entry(self, ten_bien, gia_tri):
        """Tiện ích: xóa rồi nhập giá trị mới vào Entry."""
        o = self.cac_o[ten_bien]
        if isinstance(o, tk.Entry):
            o.delete(0, "end")
            o.insert(0, gia_tri)

    # ── Xử lý lưu ─────────────────────────────────────────────────────────

    def _luu(self):
        ten_sp = self.cac_o["ten_sp"].get().strip()
        loai = self.bien_loai.get()
        gia_str = self.cac_o["gia"].get().strip()
        sl_str = self.cac_o["so_luong"].get().strip()
        ncc = self.cac_o["nha_cung_cap"].get().strip()

        if not ten_sp:
            messagebox.showwarning("Lỗi", "Tên sản phẩm không được để trống!")
            return
        if not gia_str.isdigit():
            messagebox.showwarning("Lỗi", "Giá bán phải là số nguyên dương!")
            return
        if not sl_str.isdigit():
            messagebox.showwarning("Lỗi", "Số lượng phải là số nguyên dương!")
            return

        sua_san_pham(self.id_sp_dang_sua, ten_sp, loai, int(gia_str), int(sl_str), ncc)
        messagebox.showinfo("Thành công", f"Đã cập nhật sản phẩm '{ten_sp}'!")
        self._quay_lai()

    def _quay_lai(self):
        self.app.hien_trang("danh_sach")
