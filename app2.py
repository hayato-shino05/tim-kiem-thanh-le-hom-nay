import webbrowser
import requests
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import font
from PIL import Image, ImageTk
from io import BytesIO
import os

# API Key của bạn từ Google Cloud Platform
API_KEY = "AIzaSyBkgxxgxE6pp8DDnIBBTy52UMBt3fECEOM"
BASE_URL = "https://www.googleapis.com/youtube/v3/search"

def search_videos(keyword, max_results=5):
    """Tìm kiếm video trên YouTube dựa vào từ khóa"""
    params = {
        "key": API_KEY,
        "q": keyword,
        "part": "snippet",
        "type": "video",
        "maxResults": max_results,
        "order": "date",  # Sắp xếp theo thời gian đăng tải
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    results = response.json()
    videos = []
    for item in results.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        thumbnail_url = item["snippet"]["thumbnails"]["high"]["url"]  # URL ảnh thumbnail

        videos.append({
            "title": title,
            "url": video_url,
            "thumbnail": thumbnail_url
        })
    return videos

def open_video(url):
    """Mở video trong trình duyệt và tắt chương trình"""
    webbrowser.open(url)
    os._exit(0)  # Thoát hoàn toàn chương trình

def display_menu(videos, keyword):
    """Hiển thị menu danh sách video với ảnh thumbnail"""
    menu_window = tk.Tk()
    menu_window.title("Tìm Kiếm Thánh Lễ Trực Tuyến By Hayato_shino05")
    menu_window.geometry("900x600")
    menu_window.configure(bg="#f9f9f9")
    menu_window.iconbitmap("3.ico")

    # Cài đặt font chữ
    header_font = font.Font(family="Helvetica", size=16, weight="bold")
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    # Tiêu đề
    tk.Label(
        menu_window,
        text=f"Kết quả tìm kiếm cho: {keyword}",
        font=header_font,
        bg="#f9f9f9",
        fg="#333"
    ).pack(pady=10)

    # Khung cuộn
    frame_canvas = tk.Frame(menu_window)
    frame_canvas.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame_canvas, bg="#f9f9f9", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_canvas, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    canvas.pack(side="top", fill="both", expand=True)
    scrollbar.pack(side="bottom", fill="x")

    # Hiển thị danh sách video
    for video in videos:
        # Tải ảnh thumbnail từ URL
        thumbnail_response = requests.get(video["thumbnail"])
        img_data = thumbnail_response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((120, 90), Image.LANCZOS)  # Resize ảnh
        img = ImageTk.PhotoImage(img)

        # Tạo khung cho mỗi video
        frame = tk.Frame(scrollable_frame, bg="#f9f9f9", highlightbackground="#ddd", highlightthickness=1)
        frame.pack(side="left", padx=5, pady=5)

        # Thêm ảnh thumbnail
        label_img = tk.Label(frame, image=img, bg="#f9f9f9")
        label_img.image = img  # Giữ tham chiếu tới ảnh
        label_img.pack()

        # Thêm nút tiêu đề video
        btn = tk.Button(
            frame,
            text=video["title"],
            wraplength=120,
            anchor="n",
            justify="center",
            font=button_font,
            bg="#4CAF50",
            fg="white",
            bd=0,
            padx=5,
            pady=5,
            command=lambda link=video["url"]: open_video(link)
        )
        btn.pack()

    # Nút "Hiển thị thêm video"
    def load_more_videos():
        """Tải thêm video và hiển thị"""
        try:
            new_videos = search_videos(keyword, max_results=10)
            menu_window.destroy()
            display_menu(new_videos, keyword)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải thêm video.\n{e}")

    tk.Button(
        menu_window,
        text="Hiển thị thêm video",
        font=button_font,
        bg="#FFA726",
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        command=load_more_videos
    ).pack(pady=10)

    # Nút "Tìm kiếm từ khóa khác"
    def search_other_keyword():
        """Cho phép người dùng nhập từ khóa khác để tìm kiếm"""
        keyword = simpledialog.askstring("Nhập từ khóa", "Nhập từ khóa bạn muốn tìm:")
        if not keyword:
            messagebox.showinfo("Thông báo", "Từ khóa không được để trống!")
            return
        try:
            videos = search_videos(keyword)
            if not videos:
                messagebox.showinfo("Thông báo", "Không tìm thấy video nào!")
                return
            menu_window.destroy()
            display_menu(videos, keyword)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm video.\n{e}")

    tk.Button(
        menu_window,
        text="Tìm kiếm từ khóa khác",
        font=button_font,
        bg="#2196F3",
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        command=search_other_keyword
    ).pack(pady=10)

    # Nút "Thoát"
    tk.Button(
        menu_window,
        text="Thoát",
        font=button_font,
        bg="#f44336",
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        command=lambda: os._exit(0)  # Thoát hoàn toàn chương trình
    ).pack(pady=10)

    menu_window.mainloop()

def main():
    """Tìm kiếm danh sách video dựa vào từ khóa mặc định và hiển thị ngay"""
    today = datetime.now().strftime("%d-%m-%Y")
    default_keyword = f"thánh lễ trực tuyến hôm nay {today}"
    try:
        videos = search_videos(default_keyword)
        if not videos:
            messagebox.showinfo("Thông báo", "Không tìm thấy video nào!")
            return
        display_menu(videos, default_keyword)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tìm kiếm video.\n{e}")

if __name__ == "__main__":
    # Ẩn cửa sổ CMD khi chạy file .bat
    import ctypes
    ctypes.windll.kernel32.FreeConsole()

    main()
