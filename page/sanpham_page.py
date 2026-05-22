import tkinter as tk
from tkinter import ttk, messagebox
from model.sanpham import doc_du_lieu, xoa_san_pham, tim_kiem


class TrangDanhSach(tk.Frame):
    """
    Trang chính: hiển thị danh sách toàn bộ sản phẩm.
    Có nút: Thêm, Sửa, Xóa, Tìm kiếm, Làm mới.
    Thành viên phụ trách: Nguyễn Văn A (nhóm trưởng)
    """

    def __init__(self, master, app):
        super().__init__(master, bg="#f0f0f0")
        self.app = app  # Tham chiếu tới AppManager để điều hướng
        self._tao_giao_dien()

    # ── Tạo giao diện ─────────────────────────────────────────────────────

    def _tao_giao_dien(self):
        # --- Tiêu đề ---
        tk.Label(
            self,
            text="🛒  QUẢN LÝ TẠP HÓA",
            font=("Arial", 18, "bold"),
            bg="#2c6fad", fg="white",
            pady=12
        ).pack(fill="x")

        # --- Khu vực tìm kiếm ---
        frame_tk = tk.Frame(self, bg="#f0f0f0", pady=8)
        frame_tk.pack(fill="x", padx=15)

        tk.Label(frame_tk, text="Tìm kiếm:", font=("Arial", 11), bg="#f0f0f0").pack(side="left")
        self.o_tim_kiem = tk.Entry(frame_tk, font=("Arial", 11), width=25)
        self.o_tim_kiem.pack(side="left", padx=6)
        tk.Button(
            frame_tk, text=" Tìm", font=("Arial", 11),
            bg="#2483BD", fg="white", command=self._tim_kiem
        ).pack(side="left", padx=4)
        tk.Button(
            frame_tk, text=" Làm mới", font=("Arial", 11),
            bg="#888", fg="white", command=self._lam_moi
        ).pack(side="left", padx=4)

        # --- Bảng dữ liệu (Treeview) ---
        frame_bang = tk.Frame(self, bg="#f0f0f0")
        frame_bang.pack(fill="both", expand=True, padx=15, pady=5)

        cot = ("ID", "Tên sản phẩm", "Loại", "Giá (VNĐ)", "Số lượng", "Nhà cung cấp")
        self.bang = ttk.Treeview(frame_bang, columns=cot, show="headings", height=18)

        # Đặt tiêu đề và độ rộng mỗi cột
        do_rong = [40, 180, 100, 100, 80, 180]
        for col, w in zip(cot, do_rong):
            self.bang.heading(col, text=col)
            self.bang.column(col, width=w, anchor="center")

        # Thanh cuộn dọc
        thanh_cuon = ttk.Scrollbar(frame_bang, orient="vertical", command=self.bang.yview)
        self.bang.configure(yscrollcommand=thanh_cuon.set)
        self.bang.pack(side="left", fill="both", expand=True)
        thanh_cuon.pack(side="right", fill="y")

        # --- Khu vực nút bấm ---
        frame_nut = tk.Frame(self, bg="#f0f0f0", pady=10)
        frame_nut.pack()

        tk.Button(
            frame_nut, text="➕  Thêm sản phẩm",
            font=("Arial", 11, "bold"), bg="#27ae60", fg="white",
            width=17, command=self._mo_them
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            frame_nut, text="✏️  Sửa sản phẩm",
            font=("Arial", 11, "bold"), bg="#e67e22", fg="white",
            width=17, command=self._mo_sua
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            frame_nut, text="🗑️  Xóa sản phẩm",
            font=("Arial", 11, "bold"), bg="#c0392b", fg="white",
            width=17, command=self._xoa
        ).grid(row=0, column=2, padx=8)

        tk.Button(
            frame_nut, text="📊  Thống kê",
            font=("Arial", 11, "bold"), bg="#8e44ad", fg="white",
            width=17, command=self._thong_ke
        ).grid(row=0, column=3, padx=8)

        # --- Nhãn thông tin ở cuối ---
        self.nhan_tt = tk.Label(self, text="", font=("Arial", 10), bg="#f0f0f0", fg="#555")
        self.nhan_tt.pack(pady=4)

    # ── Tải dữ liệu lên bảng ──────────────────────────────────────────────

    def tai_du_lieu(self, **kwargs):
        """Đọc từ CSV và hiện lên bảng. Được gọi mỗi khi quay về trang này."""
        self._xoa_bang()
        ds = doc_du_lieu()
        for sp in ds:
            self.bang.insert("", "end", values=(
                sp.id, sp.ten_sp, sp.loai,
                f"{sp.gia:,}", sp.so_luong, sp.nha_cung_cap
            ))
        self.nhan_tt.config(text=f"Tổng số sản phẩm: {len(ds)}")

    def _xoa_bang(self):
        """Xóa toàn bộ dòng trong bảng."""
        for row in self.bang.get_children():
            self.bang.delete(row)

    # ── Xử lý tìm kiếm ────────────────────────────────────────────────────

    def _tim_kiem(self):
        tu_khoa = self.o_tim_kiem.get().strip()
        if not tu_khoa:
            self.tai_du_lieu()
            return
        self._xoa_bang()
        ket_qua = tim_kiem(tu_khoa)
        for sp in ket_qua:
            self.bang.insert("", "end", values=(
                sp.id, sp.ten_sp, sp.loai,
                f"{sp.gia:,}", sp.so_luong, sp.nha_cung_cap
            ))
        self.nhan_tt.config(text=f"Tìm thấy: {len(ket_qua)} sản phẩm")

    def _lam_moi(self):
        self.o_tim_kiem.delete(0, "end")
        self.tai_du_lieu()

    # ── Lấy sản phẩm đang chọn ────────────────────────────────────────────

    def _lay_sp_chon(self):
        """Trả về (id, ten_sp, ...) của dòng đang chọn, hoặc None."""
        chon = self.bang.selection()
        if not chon:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một sản phẩm trong bảng!")
            return None
        return self.bang.item(chon[0])["values"]

    # ── Điều hướng trang ──────────────────────────────────────────────────

    def _mo_them(self):
        self.app.hien_trang("them")

    def _mo_sua(self):
        values = self._lay_sp_chon()
        if values:
            self.app.hien_trang("sua", id_sp=values[0])

    # ── Xóa sản phẩm ──────────────────────────────────────────────────────

    def _xoa(self):
        values = self._lay_sp_chon()
        if not values:
            return
        xac_nhan = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa sản phẩm:\n'{values[1]}'?"
        )
        if xac_nhan:
            xoa_san_pham(values[0])
            messagebox.showinfo("Thành công", "Đã xóa sản phẩm!")
            self.tai_du_lieu()

    # ── Thống kê đơn giản ─────────────────────────────────────────────────

    def _thong_ke(self):
        ds = doc_du_lieu()
        if not ds:
            messagebox.showinfo("Thống kê", "Chưa có dữ liệu.")
            return
        tong_sp = len(ds)
        tong_ton_kho = sum(sp.so_luong for sp in ds)
        tri_gia = sum(sp.gia * sp.so_luong for sp in ds)
        sp_het = [sp.ten_sp for sp in ds if sp.so_luong == 0]

        noi_dung = (
            f"📦 Tổng số loại sản phẩm : {tong_sp}\n"
            f"📊 Tổng tồn kho           : {tong_ton_kho} đơn vị\n"
            f"💰 Tổng trị giá kho       : {tri_gia:,} VNĐ\n"
        )
        if sp_het:
            noi_dung += f"\n⚠️  Sản phẩm hết hàng:\n" + "\n".join(f"   - {t}" for t in sp_het)

        messagebox.showinfo("Thống kê kho hàng", noi_dung)
