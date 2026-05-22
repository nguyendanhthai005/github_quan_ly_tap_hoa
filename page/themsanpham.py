import tkinter as tk
from tkinter import messagebox
from model.sanpham import them_san_pham


class TrangThem(tk.Frame):
    """
    Trang thêm sản phẩm mới vào tạp hóa.
    Thành viên phụ trách: Trần Thị B
    """

    # Danh sách loại sản phẩm gợi ý
    LOAI_SP = ["Lương thực", "Gia vị", "Dầu ăn", "Mì gói", "Đồ uống",
               "Bánh kẹo", "Chăm sóc cá nhân", "Đồ gia dụng", "Khác"]

    def __init__(self, master, app):
        super().__init__(master, bg="#f0f0f0")
        self.app = app
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        # --- Tiêu đề ---
        tk.Label(
            self,
            text="➕  THÊM SẢN PHẨM MỚI",
            font=("Arial", 16, "bold"),
            bg="#27ae60", fg="white", pady=10
        ).pack(fill="x")

        # --- Form nhập liệu ---
        frame_form = tk.Frame(self, bg="#f0f0f0", pady=20)
        frame_form.pack()

        # Các nhãn và ô nhập
        nhan_cot = [
            ("Tên sản phẩm (*)", "ten_sp"),
            ("Loại sản phẩm (*)", "loai"),
            ("Giá bán (VNĐ) (*)", "gia"),
            ("Số lượng tồn kho (*)", "so_luong"),
            ("Nhà cung cấp", "nha_cung_cap"),
        ]

        self.cac_o = {}  # Lưu các widget nhập liệu

        for i, (nhan, ten_bien) in enumerate(nhan_cot):
            tk.Label(
                frame_form, text=nhan,
                font=("Arial", 12), bg="#f0f0f0", anchor="e", width=22
            ).grid(row=i, column=0, padx=10, pady=8, sticky="e")

            if ten_bien == "loai":
                # Dùng OptionMenu cho loại sản phẩm
                bien_loai = tk.StringVar(value=self.LOAI_SP[0])
                o = tk.OptionMenu(frame_form, bien_loai, *self.LOAI_SP)
                o.config(font=("Arial", 11), width=22, bg="white")
                o.grid(row=i, column=1, padx=10, pady=8, sticky="w")
                self.cac_o[ten_bien] = bien_loai  # Lưu StringVar
            else:
                o = tk.Entry(frame_form, font=("Arial", 12), width=25)
                o.grid(row=i, column=1, padx=10, pady=8)
                self.cac_o[ten_bien] = o

        # Ghi chú
        tk.Label(
            frame_form,
            text="(*) Trường bắt buộc",
            font=("Arial", 10, "italic"),
            bg="#f0f0f0", fg="#888"
        ).grid(row=len(nhan_cot), column=0, columnspan=2, pady=5)

        # --- Nút bấm ---
        frame_nut = tk.Frame(self, bg="#f0f0f0")
        frame_nut.pack(pady=15)

        tk.Button(
            frame_nut, text="💾  Lưu sản phẩm",
            font=("Arial", 12, "bold"), bg="#27ae60", fg="white",
            width=16, command=self._luu
        ).grid(row=0, column=0, padx=15)

        tk.Button(
            frame_nut, text="↩️  Quay lại",
            font=("Arial", 12, "bold"), bg="#888", fg="white",
            width=16, command=self._quay_lai
        ).grid(row=0, column=1, padx=15)

    # ── Xử lý lưu ─────────────────────────────────────────────────────────

    def _luu(self):
        # Lấy giá trị từ các ô nhập
        ten_sp = self.cac_o["ten_sp"].get().strip()
        loai = self.cac_o["loai"].get()          # StringVar -> .get()
        gia_str = self.cac_o["gia"].get().strip()
        sl_str = self.cac_o["so_luong"].get().strip()
        ncc = self.cac_o["nha_cung_cap"].get().strip()

        # Kiểm tra dữ liệu đầu vào
        if not ten_sp:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên sản phẩm!")
            return
        if not gia_str.isdigit():
            messagebox.showwarning("Lỗi", "Giá bán phải là số nguyên dương!")
            return
        if not sl_str.isdigit():
            messagebox.showwarning("Lỗi", "Số lượng phải là số nguyên dương!")
            return

        # Thêm vào CSV
        them_san_pham(ten_sp, loai, int(gia_str), int(sl_str), ncc)
        messagebox.showinfo("Thành công", f"Đã thêm sản phẩm '{ten_sp}' thành công!")
        self._xoa_form()
        self._quay_lai()

    def _xoa_form(self):
        """Xóa toàn bộ nội dung trong các ô nhập."""
        for ten_bien, widget in self.cac_o.items():
            if isinstance(widget, tk.Entry):
                widget.delete(0, "end")
            # OptionMenu (StringVar) thì không cần xóa

    def _quay_lai(self):
        self.app.hien_trang("danh_sach")

    def tai_du_lieu(self, **kwargs):
        """Được gọi khi mở trang - xóa form cũ nếu có."""
        self._xoa_form()
