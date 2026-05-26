import tkinter as tk
from tkinter import ttk
import pandas as pd
import os


class ThongKePage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        self.cau_hinh()
        self.giao_dien()
        self.tai_du_lieu()

    def cau_hinh(self):
        self.master.title("Thống kê bán hàng")
        self.master.geometry("1200x600")

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

        tk.Button(
            menu_frame,
            text="📊 Thống kê",
            command=self.app_manager.hien_thi_thongke_page,
            bg="#2c3e50",
            fg="white",
            relief="flat",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10)

        tk.Label(
            self.master,
            text="THỐNG KÊ & LỊCH SỬ BÁN HÀNG",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        # Frame thống kê
        frame_tk = tk.Frame(self.master)
        frame_tk.pack(fill="x", padx=20, pady=10)

        self.lbl_so_don = tk.Label(
            frame_tk,
            text="Số đơn hàng: 0",
            font=("Arial", 14, "bold"),
            fg="blue"
        )
        self.lbl_so_don.pack(side="left", padx=20)

        self.lbl_doanh_thu = tk.Label(
            frame_tk,
            text="Doanh thu: 0 VNĐ",
            font=("Arial", 14, "bold"),
            fg="red"
        )
        self.lbl_doanh_thu.pack(side="left", padx=20)

        # Bảng lịch sử
        frame_table = tk.Frame(self.master)
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        columns = (
            "ngay_gio",
            "ten_sp",
            "so_luong",
            "don_gia",
            "thanh_tien"
        )

        self.tree = ttk.Treeview(
            frame_table,
            columns=columns,
            show="headings"
        )

        self.tree.heading("ngay_gio", text="Ngày giờ")
        self.tree.heading("ten_sp", text="Tên sản phẩm")
        self.tree.heading("so_luong", text="Số lượng")
        self.tree.heading("don_gia", text="Đơn giá")
        self.tree.heading("thanh_tien", text="Thành tiền")

        self.tree.column("ngay_gio", width=180)
        self.tree.column("ten_sp", width=300)
        self.tree.column("so_luong", width=100, anchor="center")
        self.tree.column("don_gia", width=150, anchor="center")
        self.tree.column("thanh_tien", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(
            frame_table,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def tai_du_lieu(self):
        file_lichsu = "data/lichsu_banhang.csv"

        if not os.path.exists(file_lichsu):
            df = pd.DataFrame(columns=[
                'ngay_gio',
                'ten_sp',
                'so_luong',
                'don_gia',
                'thanh_tien'
            ])
            df.to_csv(file_lichsu, index=False)

        data = pd.read_csv(file_lichsu)

        for item in self.tree.get_children():
            self.tree.delete(item)

        tong_doanh_thu = 0

        for _, row in data.iterrows():
            tong_doanh_thu += int(row['thanh_tien'])

            self.tree.insert(
                "",
                "end",
                values=(
                    row['ngay_gio'],
                    row['ten_sp'],
                    row['so_luong'],
                    f"{int(row['don_gia']):,}",
                    f"{int(row['thanh_tien']):,}"
                )
            )

        self.lbl_so_don.config(
            text=f"Số đơn hàng: {len(data)}"
        )

        self.lbl_doanh_thu.config(
            text=f"Doanh thu: {tong_doanh_thu:,} VNĐ"
        )
