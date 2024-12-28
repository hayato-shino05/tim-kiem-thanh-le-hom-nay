import webbrowser
import requests
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import font
from PIL import Image, ImageTk
from io import BytesIO
import os
import sys

API_KEY = "AIzaSyBkgxxgxE6pp8DDnIBBTy52UMBt3fECEOM"
BASE_URL = "https://www.googleapis.com/youtube/v3/search"

videos_list = []
current_keyword = ""

def search_videos(keyword, max_results=5):
    """Tìm kiếm video trên YouTube dựa vào từ khóa"""
    params = {
        "key": API_KEY,
        "q": keyword,
        "part": "snippet",
        "type": "video",
        "maxResults": max_results,
        "order": "date",  
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        results = response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Lỗi", f"Không thể kết nối API: {e}")
        return []

    videos = []
    for item in results.get("items", []):
        video_id = item.get("id", {}).get("videoId")
        title = item.get("snippet", {}).get("title")
        thumbnail_url = item.get("snippet", {}).get("thumbnails", {}).get("high", {}).get("url")

        if video_id and title and thumbnail_url:
            videos.append({
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": thumbnail_url
            })
    return videos

def open_video(url):
    """Mở video trong trình duyệt và tắt chương trình"""
    webbrowser.open(url)
    sys.exit(0)  

def display_menu(videos, keyword):
    """Hiển thị menu danh sách video với ảnh thumbnail"""
    global videos_list
    global current_keyword

    videos_list = videos
    current_keyword = keyword

    menu_window = tk.Tk()
    menu_window.title("Tìm Kiếm Thánh Lễ Trực Tuyến By Hayato_shino05")
    menu_window.geometry("800x600")
    menu_window.configure(bg="#f9f9f9")
    menu_window.iconbitmap("3.ico")


    header_font = font.Font(family="Helvetica", size=16, weight="bold")
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    tk.Label(
        menu_window,
        text=f"Kết quả tìm kiếm cho: {keyword}",
        font=header_font,
        bg="#f9f9f9",
        fg="#333"
    ).pack(pady=10)

    frame_canvas = tk.Frame(menu_window)
    frame_canvas.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame_canvas, bg="#f9f9f9", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta / 120), "units"))

    for video in videos:
        try:
            thumbnail_response = requests.get(video["thumbnail"])
            thumbnail_response.raise_for_status()
            img_data = thumbnail_response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((150, 100), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            frame = tk.Frame(scrollable_frame, bg="#f9f9f9", highlightbackground="#ddd", highlightthickness=1)
            frame.pack(fill="x", padx=5, pady=10)

            label_img = tk.Label(frame, image=img, bg="#f9f9f9")
            label_img.image = img
            label_img.pack(side="left", padx=10)

            btn = tk.Button(
                frame,
                text=video["title"],
                wraplength=500,
                anchor="w",
                justify="left",
                font=button_font,
                bg="#4CAF50",
                fg="white",
                bd=0,
                padx=10,
                pady=10,
                command=lambda link=video["url"]: open_video(link)
            )
            btn.pack(side="left", fill="x", expand=True, padx=10, pady=5)

        except Exception as e:
            print(f"Lỗi khi tải thumbnail hoặc hiển thị: {e}")

    button_frame = tk.Frame(menu_window, bg="#f9f9f9")
    button_frame.pack(pady=10)

    def search_other_keyword():
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

    def load_more_videos():
        """Tải thêm video và hiển thị"""
        try:
            new_videos = search_videos(keyword, max_results=10)
            menu_window.destroy()
            display_menu(new_videos, keyword)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải thêm video.\n{e}")

    def exit_program():
        sys.exit(0)

    tk.Button(
        button_frame,
        text="Tìm kiếm từ khóa khác",
        font=button_font,
        bg="#2196F3",
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        command=search_other_keyword
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Hiển thị thêm video",
        font=button_font,
        bg="#FFA726",
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        command=load_more_videos
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Thoát",
        font=button_font,
        bg="#f44336",
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        command=exit_program
    ).pack(side="left", padx=10)

    menu_window.mainloop()

def main():
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
    try:
        import ctypes
        ctypes.windll.kernel32.FreeConsole()
    except Exception:
        pass

    main()
