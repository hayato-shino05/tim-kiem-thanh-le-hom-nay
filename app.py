import webbrowser
import requests

# API Key của bạn từ Google Cloud Platform
API_KEY = "AIzaSyBkgxxgxE6pp8DDnIBBTy52UMBt3fECEOM"
BASE_URL = "https://www.googleapis.com/youtube/v3/search"

def search_videos(keyword):
    """Tìm kiếm video trên YouTube dựa vào từ khóa"""
    params = {
        "key": API_KEY,
        "q": keyword,
        "part": "snippet",
        "type": "video",
        "maxResults": 5,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    results = response.json()
    videos = []
    for item in results.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        videos.append((title, f"https://www.youtube.com/watch?v={video_id}"))
    return videos

def main():
    # Nhập từ khóa tìm kiếm
    keyword = input("Nhập từ khóa tìm kiếm: ").strip()
    if not keyword:
        print("Từ khóa không được để trống!")
        return

    # Tìm kiếm video
    try:
        videos = search_videos(keyword)
        if not videos:
            print("Không tìm thấy video nào!")
            return
        
        # Hiển thị danh sách video
        print("\nKết quả tìm kiếm:")
        for i, (title, url) in enumerate(videos, 1):
            print(f"{i}. {title} - {url}")

        # Chọn video để mở
        choice = int(input("\nChọn video (số): "))
        if 1 <= choice <= len(videos):
            _, url = videos[choice - 1]
            print(f"Mở video: {url}")
            webbrowser.open(url)
        else:
            print("Lựa chọn không hợp lệ!")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()
