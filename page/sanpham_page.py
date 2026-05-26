import tkinter as tk
from tkinter import messagebox, ttk, Toplevel
from model.sanpham_model import SanphamModel


class SanphamPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.sp = SanphamModel("data/sanpham.csv", ['id', 'ma_sp', 'ten_sp', 'so_luong', 'don_gia'])
        self.cau_hinh()
        self.xem_giao_dien()
        self.tai_du_lieu()

    def cau_hinh(self):
        self.master.title("Quản lý hàng hóa tạp hóa")
        self.master.geometry("1000x400")

    def xem_giao_dien(self):
        # Menu điều hướng trên cùng
        menu_frame = tk.Frame(self.master, bg="#2c3e50", height=50)
        menu_frame.pack(fill="x", side="top")
        menu_frame.pack_propagate(False)

        tk.Button(menu_frame, text="📦 Quản lý hàng", command=self.app_manager.hien_thi_sanpham_page, bg="#2c3e50",
                  fg="white", relief="flat", font=("Arial", 11, "bold")).pack(side="left", padx=15, pady=10)
        tk.Button(menu_frame, text="🛒 Bán hàng", command=self.app_manager.hien_thi_banhang_page, bg="#2c3e50",
                  fg="white", relief="flat", font=("Arial", 11, "bold")).pack(side="left", padx=10, pady=10)
        tk.Button(menu_frame, text="📥 Thống kê", command=self.app_manager.hien_thi_thongke_page, bg="#2c3e50",
                  fg="white", relief="flat", font=("Arial", 11, "bold")).pack(side="left", padx=10, pady=10)
        tk.Button(menu_frame, text="🔄 Làm mới", command=self.tai_du_lieu, bg="#27ae60", fg="white", relief="flat",
                  font=("Arial", 11)).pack(side="right", padx=15, pady=10)

        # Tiêu đề
        tk.Label(self.master, text="Danh sách sản phẩm trong kho", font=("Arial", 20, "bold")).pack(pady=10)

        # Frame nút chức năng
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="➕ Thêm sản phẩm", command=self.mo_form_them).pack(side="left", padx=5)
        tk.Button(button_frame, text="🔙 Quay lại", command=self.app_manager.hien_thi_sanpham_page).pack(side="right",  padx=5)

        # Bảng hiển thị (Treeview)
        tree_frame = tk.Frame(self.master)
        tree_frame.pack(expand=True, fill="both", padx=20, pady=10)

        columns = ("STT", "ma_sp", "ten_sp", "so_luong", "don_gia", "Sửa", "Xóa")
        self.bang_hang = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

        self.bang_hang.heading("STT", text="STT")
        self.bang_hang.heading("ma_sp", text="Mã SP")
        self.bang_hang.heading("ten_sp", text="Tên sản phẩm")
        self.bang_hang.heading("so_luong", text="Số lượng")
        self.bang_hang.heading("don_gia", text="Đơn giá (VNĐ)")
        self.bang_hang.heading("Sửa", text="Sửa")
        self.bang_hang.heading("Xóa", text="Xóa")

        self.bang_hang.column("STT", width=50, anchor="center")
        self.bang_hang.column("ma_sp", width=100, anchor="center")
        self.bang_hang.column("ten_sp", width=200, anchor="center")
        self.bang_hang.column("so_luong", width=100, anchor="center")
        self.bang_hang.column("don_gia", width=150, anchor="center")
        self.bang_hang.column("Sửa", width=70, anchor="center")
        self.bang_hang.column("Xóa", width=70, anchor="center")

        # Gắn sự kiện click chuột
        self.bang_hang.bind("<ButtonRelease-1>", self.xu_ly_nhan_chuot)

        # Thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.bang_hang.yview)
        self.bang_hang.configure(yscrollcommand=scrollbar.set)

        self.bang_hang.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        # Thanh trạng thái
        self.status_label = tk.Label(self.master, text="Sẵn sàng", relief="sunken", anchor="w")
        self.status_label.pack(side="bottom", fill="x")

    def tai_du_lieu(self):
        """Tải danh sách từ CSV và hiển thị lên bảng"""
        du_lieu = self.sp.danh_sach(1, 10000)

        # Xóa dữ liệu cũ trên bảng trước khi tải mới
        for i in self.bang_hang.get_children():
            self.bang_hang.delete(i)

        for i, item in enumerate(du_lieu["data"], start=1):
            self.bang_hang.insert("", "end", values=(i, item["ma_sp"], item["ten_sp"],
                                                     item["so_luong"], item["don_gia"],
                                                     "✏️ Sửa", "🗑️ Xóa"))

    def mo_form_them(self):
        """Mở cửa sổ mới để nhập thông tin sản phẩm"""
        form = Toplevel(self.master)
        form.title("Thêm sản phẩm mới")
        form.geometry("300x320")
        form.grab_set()  # Khóa cửa sổ chính cho đến khi đóng form

        tk.Label(form, text="Mã SP:").pack(pady=5)
        entry_ma = tk.Entry(form)
        entry_ma.pack()

        tk.Label(form, text="Tên SP:").pack(pady=5)
        entry_ten = tk.Entry(form)
        entry_ten.pack()

        tk.Label(form, text="Số lượng:").pack(pady=5)
        entry_sl = tk.Entry(form)
        entry_sl.pack()

        tk.Label(form, text="Đơn giá:").pack(pady=5)
        entry_gia = tk.Entry(form)
        entry_gia.pack()

        def xu_ly_luu():
            ma = entry_ma.get().strip()
            ten = entry_ten.get().strip()
            sl = entry_sl.get().strip()
            gia = entry_gia.get().strip()

            if not (ma and ten and sl and gia):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
                return

            new_data = {
                "id": str(self.sp.lay_id_tiep_theo()),
                "ma_sp": ma,
                "ten_sp": ten,
                "so_luong": sl,
                "don_gia": gia
            }
            self.sp.them(new_data)
            messagebox.showinfo("Thành công", "Đã thêm sản phẩm vào kho!")
            form.destroy()
            self.tai_du_lieu()

        tk.Button(form, text="💾 Lưu sản phẩm", command=xu_ly_luu, bg="#27ae60", fg="white").pack(pady=20)

    def xu_ly_nhan_chuot(self, event):
        """Xử lý khi người dùng click vào bảng"""
        region = self.bang_hang.identify_region(event.x, event.y)
        if region != "cell":
            return

        column = self.bang_hang.identify_column(event.x)
        row_id = self.bang_hang.identify_row(event.y)
        if not row_id:
            return

        col_index = int(column.replace("#", "")) - 1
        columns = ("STT", "ma_sp", "ten_sp", "so_luong", "don_gia", "Sửa", "Xóa")
        col_name = columns[col_index] if col_index < len(columns) else ""

        if col_name == "Sửa":
            self.mo_form_sua(row_id)
        elif col_name == "Xóa":
            if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sản phẩm này?"):
                id_sp = self.bang_hang.item(row_id)["values"][0]
                self.sp.xoa("id", str(id_sp))
                self.bang_hang.delete(row_id)
                messagebox.showinfo("Thành công", "Đã xóa sản phẩm!")

    def mo_form_sua(self, row_id):
        """Mở form sửa thông tin sản phẩm"""
        values = self.bang_hang.item(row_id)["values"]
        id_sp = str(values[0])

        form = Toplevel(self.master)
        form.title("Chỉnh sửa sản phẩm")
        form.geometry("300x320")
        form.grab_set()

        tk.Label(form, text="Mã SP:").pack(pady=5)
        entry_ma = tk.Entry(form)
        entry_ma.insert(0, str(values[1]))
        entry_ma.pack()

        tk.Label(form, text="Tên SP:").pack(pady=5)
        entry_ten = tk.Entry(form)
        entry_ten.insert(0, str(values[2]))
        entry_ten.pack()

        tk.Label(form, text="Số lượng:").pack(pady=5)
        entry_sl = tk.Entry(form)
        entry_sl.insert(0, str(values[3]))
        entry_sl.pack()

        tk.Label(form, text="Đơn giá:").pack(pady=5)
        entry_gia = tk.Entry(form)
        entry_gia.insert(0, str(values[4]))
        entry_gia.pack()

        def xu_ly_cap_nhat():
            new_data = [entry_ma.get().strip(), entry_ten.get().strip(),
                        entry_sl.get().strip(), entry_gia.get().strip()]
            title_edit = ["ma_sp", "ten_sp", "so_luong", "don_gia"]

            self.sp.cap_nhat("id", id_sp, title_edit, new_data)
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin sản phẩm!")
            form.destroy()
            self.tai_du_lieu()

        tk.Button(form, text="🔄 Cập nhật", command=xu_ly_cap_nhat, bg="#2980b9", fg="white").pack(pady=20)