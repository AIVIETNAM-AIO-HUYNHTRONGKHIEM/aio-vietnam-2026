import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import ImageTk, Image

# Author information
AUTHOR_NAME = "Google Gemini AI - Visual Studio Code"
VERSION = "1.0.1"
RELEASE_DATE = "2026-02-01"

def show_about():
    """Show window with author information."""
    about_text = (
        f"Trình tạo mã QR sạch - Phiên bản {VERSION}\n"
        f"Ngày phát hành: {RELEASE_DATE}\n"
        f"Tác giả: {AUTHOR_NAME}"
    )
    messagebox.showinfo("Giới thiệu", about_text)

# Generate QR code function
def generate_qr():
    link = entry.get()
    if not link.strip():
        messagebox.showwarning("Lỗi", "Vui lòng dán link Google Drive vào ô trống!")
        return

    try:
        # Cấu hình mã QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        # Tạo ảnh
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Cho phép người dùng chọn nơi lưu và tên file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile="Ma_QR_Google_Drive"
        )
        
        if file_path:
            img.save(file_path)
            messagebox.showinfo("Thành công", f"Đã lưu mã QR tại:\n{file_path}")
            
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

# Thiết lập cửa sổ chính
root = tk.Tk()
root.title("Trình tạo mã QR sạch - 2026")
root.geometry("400x250")
root.resizable(False, False)

# Giao diện
label = tk.Label(root, text="Dán link Google Drive hoặc URL bất kỳ:", font=("Arial", 10))
label.pack(pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 10))
entry.pack(pady=5)
entry.focus_set()

btn_generate = tk.Button(root, text="Tạo và Lưu Mã QR", command=generate_qr, 
                         bg="#4CAF50", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5)
btn_generate.pack(pady=20)

footer = tk.Label(root, text="Công cụ không quảng cáo, chạy Offline", fg="gray")
footer.pack(side="bottom", pady=5)

tk.Label(root, text=f"Phiên bản {VERSION} | © 2026", fg="gray", font=("Arial", 8)).pack(side="bottom")
# --- MENU BAR --- 
menu_bar = tk.Menu(root)

# Menu system file
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Thoát", command=root.quit)
menu_bar.add_cascade(label="Hệ thống", menu=file_menu)

# Menu thông tin
info_menu = tk.Menu(menu_bar, tearoff=0)
info_menu.add_command(label="Giới thiệu", command=show_about)
menu_bar.add_cascade(label="Thông tin", menu=info_menu)

root.config(menu=menu_bar)
root.mainloop()