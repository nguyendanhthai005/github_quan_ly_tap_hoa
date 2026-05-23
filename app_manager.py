import tkinter as tk
from page.sanpham_page import SanphamPage
from page.banhang_page import BanHangPage
# from page.naphang_page import NhapHangPage

class QuanLyTapHoaManager:
    def __init__(self):
        self.goc = tk.Tk()
        self.goc.title("Ứng dụng Quản lý Tạp Hóa")
        self.goc.geometry("1000x500")
        self.trang_hien_tai = None
        self.hien_thi_sanpham_page()

    def xoa_trang_hien_tai(self):
        """Xóa tất cả widget của page hiện tại"""
        if self.trang_hien_tai:
            for widget in self.goc.winfo_children():
                widget.destroy()

    def hien_thi_sanpham_page(self):
        """Hiển thị trang quản lý sản phẩm"""
        self.xoa_trang_hien_tai()
        self.goc.geometry("1000x450")
        self.trang_hien_tai = SanphamPage(self.goc, self)

    def hien_thi_banhang_page(self):
        self.xoa_trang_hien_tai()
        self.goc.geometry("1100x550")
        self.trang_hien_tai = BanHangPage(self.goc, self)

    def hien_thi_naphang_page(self):
        """Chuyển đến trang Nhập hàng (sẽ phát triển sau)"""
        self.xoa_trang_hien_tai()
        tk.Label(self.goc, text="📥 Chức năng Nhập hàng\n(Đang được phát triển)", font=("Arial", 20)).pack(pady=150)
        tk.Button(self.goc, text="⬅ Quay lại", command=self.hien_thi_sanpham_page).pack(pady=10)

    def chay(self):
        """Chạy ứng dụng"""
        self.goc.mainloop()