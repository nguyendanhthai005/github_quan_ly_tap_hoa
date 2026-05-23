import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from model.sanpham_model import SanphamModel


class BanHangPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        self.sp = SanphamModel(
            "data/sanpham.csv",
            ['id', 'ma_sp', 'ten_sp', 'so_luong', 'don_gia']
        )

        self.gio_hang = []

        self.cau_hinh()
        self.giao_dien()
        self.tai_san_pham()

    def cau_hinh(self):
        self.master.title("Quản lý bán hàng")
        self.master.geometry("1100x550")

    def giao_dien(self):
        menu_frame = tk.Frame(self.master, bg="#2c3e50", height=50)
        menu_frame.pack(fill="x")
        menu_frame.pack_propagate(False)

        tk.Button(
            menu_frame,
            text="📦 Quản lý hàng",
            command=self.app_manager.hien_thi_sanpham_page,
            bg="#2c3e50",
            fg="white",
            relief="flat",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10, pady=10)

        tk.Button(
            menu_frame,
            text="🛒 Bán hàng",
            command=self.app_manager.hien_thi_banhang_page,
            bg="#2c3e50",
            fg="white",
            relief="flat",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10)

        tk.Label(
            self.master,
            text="QUẢN LÝ BÁN HÀNG",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        frame_top = tk.Frame(self.master)
        frame_top.pack(fill="x", padx=10)

        tk.Label(frame_top, text="Chọn sản phẩm:").pack(side="left")

        self.cb_sanpham = ttk.Combobox(frame_top, width=40)
        self.cb_sanpham.pack(side="left", padx=10)

        tk.Label(frame_top, text="Số lượng:").pack(side="left")

        self.entry_sl = tk.Entry(frame_top, width=10)
        self.entry_sl.pack(side="left", padx=10)

        tk.Button(
            frame_top,
            text="➕ Thêm vào giỏ",
            command=self.them_vao_gio,
            bg="#27ae60",
            fg="white"
        ).pack(side="left")

        # Bảng giỏ hàng
        frame_gio = tk.Frame(self.master)
        frame_gio.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("ten_sp", "so_luong", "don_gia", "thanh_tien")

        self.tree = ttk.Treeview(frame_gio, columns=columns, show="headings")

        self.tree.heading("ten_sp", text="Tên sản phẩm")
        self.tree.heading("so_luong", text="Số lượng")
        self.tree.heading("don_gia", text="Đơn giá")
        self.tree.heading("thanh_tien", text="Thành tiền")

        self.tree.column("ten_sp", width=250)
        self.tree.column("so_luong", width=100, anchor="center")
        self.tree.column("don_gia", width=150, anchor="center")
        self.tree.column("thanh_tien", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # Tổng tiền
        frame_bottom = tk.Frame(self.master)
        frame_bottom.pack(fill="x", padx=10, pady=10)

        self.lbl_tong = tk.Label(
            frame_bottom,
            text="Tổng tiền: 0 VNĐ",
            font=("Arial", 14, "bold"),
            fg="red"
        )
        self.lbl_tong.pack(side="left")

        tk.Button(
            frame_bottom,
            text="💰 Thanh toán",
            command=self.thanh_toan,
            bg="#e67e22",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side="right", padx=5)

        tk.Button(
            frame_bottom,
            text="🗑 Xóa giỏ hàng",
            command=self.xoa_gio_hang,
            bg="#c0392b",
            fg="white"
        ).pack(side="right", padx=5)

    def tai_san_pham(self):
        data = pd.read_csv("data/sanpham.csv")

        self.ds_sanpham = data.to_dict("records")

        danh_sach = []
        for item in self.ds_sanpham:
            danh_sach.append(f"{item['ma_sp']} - {item['ten_sp']}")

        self.cb_sanpham["values"] = danh_sach

    def them_vao_gio(self):
        san_pham_chon = self.cb_sanpham.get()
        so_luong = self.entry_sl.get().strip()

        if san_pham_chon == "" or so_luong == "":
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin")
            return

        try:
            so_luong = int(so_luong)
        except:
            messagebox.showerror("Lỗi", "Số lượng phải là số")
            return

        ma_sp = san_pham_chon.split(" - ")[0]

        san_pham = None
        for item in self.ds_sanpham:
            if item['ma_sp'] == ma_sp:
                san_pham = item
                break

        if san_pham is None:
            return

        ton_kho = int(san_pham['so_luong'])

        if so_luong > ton_kho:
            messagebox.showerror("Lỗi", "Số lượng tồn kho không đủ")
            return

        don_gia = int(san_pham['don_gia'])
        thanh_tien = so_luong * don_gia

        self.gio_hang.append({
            "id": san_pham['id'],
            "ten_sp": san_pham['ten_sp'],
            "so_luong": so_luong,
            "don_gia": don_gia,
            "thanh_tien": thanh_tien
        })

        self.cap_nhat_gio_hang()

        self.entry_sl.delete(0, tk.END)

    def cap_nhat_gio_hang(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        tong = 0

        for item in self.gio_hang:
            tong += item['thanh_tien']

            self.tree.insert(
                "",
                "end",
                values=(
                    item['ten_sp'],
                    item['so_luong'],
                    f"{item['don_gia']:,}",
                    f"{item['thanh_tien']:,}"
                )
            )

        self.lbl_tong.config(text=f"Tổng tiền: {tong:,} VNĐ")

    def xoa_gio_hang(self):
        self.gio_hang = []
        self.cap_nhat_gio_hang()

    def thanh_toan(self):
        if len(self.gio_hang) == 0:
            messagebox.showwarning("Thông báo", "Giỏ hàng đang trống")
            return

        data = pd.read_csv("data/sanpham.csv")

        for item in self.gio_hang:
            index = data[data['id'].astype(str) == str(item['id'])].index

            if len(index) > 0:
                i = index[0]
                data.loc[i, 'so_luong'] = int(data.loc[i, 'so_luong']) - item['so_luong']

        data.to_csv("data/sanpham.csv", index=False)

        tong = sum(item['thanh_tien'] for item in self.gio_hang)

        messagebox.showinfo(
            "Thanh toán thành công",
            f"Khách cần trả: {tong:,} VNĐ"
        )

        self.gio_hang = []
        self.cap_nhat_gio_hang()
        self.tai_san_pham()