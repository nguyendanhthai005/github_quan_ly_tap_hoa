import tkinter as tk
from page.sanpham_page import SanphamPage
from page.banhang_page import BanHangPage
from page.thongke_page import ThongKePage


class QuanLyTapHoaManager:
    def __init__(self):
        self.goc = tk.Tk()
        self.goc.title("Ứng dụng Quản lý Tạp Hóa")
        self.goc.geometry("1000x500")
        self.trang_hien_tai = None

        self.hien_thi_sanpham_page()

    def xoa_trang_hien_tai(self):
        if self.trang_hien_tai:
            for widget in self.goc.winfo_children():
                widget.destroy()

    def hien_thi_sanpham_page(self):
        self.xoa_trang_hien_tai()
        self.goc.geometry("1000x450")
        self.trang_hien_tai = SanphamPage(self.goc, self)

    def hien_thi_banhang_page(self):
        self.xoa_trang_hien_tai()
        self.goc.geometry("1100x550")
        self.trang_hien_tai = BanHangPage(self.goc, self)

    def hien_thi_thongke_page(self):
        self.xoa_trang_hien_tai()
        self.goc.geometry("1200x600")
        self.trang_hien_tai = ThongKePage(self.goc, self)

    def chay(self):
        self.goc.mainloop()