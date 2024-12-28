from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.network.urlrequest import UrlRequest
import webbrowser

API_KEY = "AIzaSyC14GlOtrF7XScPuBLRhsoG6AVOqquA60"
BASE_URL = "https://www.googleapis.com/youtube/v3/search"

class YouTubeSearchApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.search_bar = TextInput(hint_text="Nhập từ khóa tìm kiếm...", size_hint_y=None, height=50)
        self.search_button = Button(text="Tìm kiếm", size_hint_y=None, height=50, on_press=self.search_videos)
        self.scroll_view = ScrollView()

        self.result_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))

        self.scroll_view.add_widget(self.result_layout)

        self.root.add_widget(self.search_bar)
        self.root.add_widget(self.search_button)
        self.root.add_widget(self.scroll_view)

        return self.root

    def search_videos(self, instance):
        keyword = self.search_bar.text
        if not keyword:
            self.show_message("Vui lòng nhập từ khóa tìm kiếm!")
            return

        params = {
            "key": API_KEY,
            "q": keyword,
            "part": "snippet",
            "type": "video",
            "maxResults": 5,
            "order": "date"
        }

        url = f"{BASE_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        UrlRequest(url, on_success=self.display_results, on_error=self.on_error, on_failure=self.on_error)

    def display_results(self, req, result):
        self.result_layout.clear_widgets()

        videos = result.get("items", [])
        if not videos:
            self.show_message("Không tìm thấy video nào!")
            return

        for video in videos:
            video_id = video["id"]["videoId"]
            title = video["snippet"]["title"]
            thumbnail_url = video["snippet"]["thumbnails"]["high"]["url"]

            video_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=120, padding=5, spacing=10)

            thumbnail = AsyncImage(source=thumbnail_url, size_hint_x=None, width=150)
            video_button = Button(
                text=title,
                halign='left',
                valign='middle',
                on_press=lambda instance, url=f"https://www.youtube.com/watch?v={video_id}": self.open_video(url)
            )
            video_button.text_size = (video_button.width - 20, None)

            video_layout.add_widget(thumbnail)
            video_layout.add_widget(video_button)

            self.result_layout.add_widget(video_layout)

    def on_error(self, req, error):
        self.show_message(f"Lỗi khi tìm kiếm: {error}")

    def open_video(self, url):
        webbrowser.open(url)

    def show_message(self, message):
        self.result_layout.clear_widgets()
        self.result_layout.add_widget(Label(text=message, size_hint_y=None, height=50))

if __name__ == '__main__':
    YouTubeSearchApp().run()
