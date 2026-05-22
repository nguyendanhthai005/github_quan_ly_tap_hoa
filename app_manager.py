import tkinter as tk


class AppManager:
    """
    Lớp quản lý ứng dụng:
    - Tạo cửa sổ chính (root)
    - Điều hướng giữa các trang (Frame)
    - Mỗi lần chỉ hiện 1 trang
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🛒  Quản Lý Tạp Hóa")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")

        # Từ điển chứa các trang đã tạo  {tên_trang: đối_tượng_Frame}
        self.cac_trang = {}

        # Trang hiện đang hiện
        self.trang_hien_tai = None

    def them_trang(self, ten_trang, trang):
        """Đăng ký một trang mới vào app."""
        self.cac_trang[ten_trang] = trang

    def hien_trang(self, ten_trang, **kwargs):
        """
        Ẩn trang đang hiện và hiện trang mới.
        kwargs dùng để truyền dữ liệu vào trang (vd: truyền object sản phẩm cần sửa).
        """
        # Ẩn trang cũ
        if self.trang_hien_tai:
            self.trang_hien_tai.pack_forget()

        # Lấy trang mới
        trang = self.cac_trang[ten_trang]

        # Nếu trang có hàm 'tai_du_lieu' thì gọi để làm mới nội dung
        if hasattr(trang, "tai_du_lieu"):
            trang.tai_du_lieu(**kwargs)

        trang.pack(fill="both", expand=True)
        self.trang_hien_tai = trang

    def chay(self):
        """Khởi chạy vòng lặp giao diện."""
        self.root.mainloop()
