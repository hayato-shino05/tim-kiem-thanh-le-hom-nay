from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
import requests
from datetime import datetime

API_KEY = "AIzaSyC14GlOtrF7XScPuBLRhsoG6AVOqquA60U"
BASE_URL = "https://www.googleapis.com/youtube/v3/search"

class VideoSearchApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation='vertical')
        
        # Header with search functionality
        self.header = BoxLayout(size_hint_y=0.1, padding=10, spacing=10)
        self.search_input = TextInput(hint_text="Enter keyword", multiline=False)
        self.search_button = Button(text="Search", size_hint_x=0.2, on_press=self.search_videos)
        self.header.add_widget(self.search_input)
        self.header.add_widget(self.search_button)
        
        # Scrollable video list
        self.scroll_view = ScrollView()
        self.video_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.video_list.bind(minimum_height=self.video_list.setter('height'))
        self.scroll_view.add_widget(self.video_list)

        self.root_layout.add_widget(self.header)
        self.root_layout.add_widget(self.scroll_view)

        # Default search
        self.default_keyword = f"thánh lễ trực tuyến hôm nay {datetime.now().strftime('%d-%m-%Y')}"
        self.perform_search(self.default_keyword)

        return self.root_layout

    def search_videos(self, instance):
        keyword = self.search_input.text.strip()
        if keyword:
            self.perform_search(keyword)

    def perform_search(self, keyword):
        params = {
            "key": API_KEY,
            "q": keyword,
            "part": "snippet",
            "type": "video",
            "maxResults": 10,
            "order": "date",
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            results = response.json()

            self.display_videos(results.get("items", []), keyword)

        except requests.exceptions.RequestException as e:
            self.show_popup("Error", f"Failed to connect to YouTube API: {e}")

    def display_videos(self, videos, keyword):
        self.video_list.clear_widgets()
        if not videos:
            self.show_popup("No Results", "No videos found.")
            return

        for item in videos:
            video_id = item.get("id", {}).get("videoId")
            snippet = item.get("snippet", {})

            if not video_id or not snippet:
                continue

            title = snippet.get("title", "Untitled")
            thumbnail_url = snippet.get("thumbnails", {}).get("high", {}).get("url")
            description = snippet.get("description", "No description available.")
            
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            video_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=120, padding=5)
            
            if thumbnail_url:
                thumbnail = AsyncImage(source=thumbnail_url, size_hint_x=0.3)
                video_box.add_widget(thumbnail)

            info_box = BoxLayout(orientation='vertical')
            info_box.add_widget(Label(text=title, size_hint_y=0.5))
            info_box.add_widget(Label(text=description[:100] + '...', size_hint_y=0.5))

            play_button = Button(text="Play", size_hint_x=0.2, on_press=lambda instance, url=video_url: self.open_video(url))
            video_box.add_widget(info_box)
            video_box.add_widget(play_button)

            self.video_list.add_widget(video_box)

    def open_video(self, url):
        import webbrowser
        webbrowser.open(url)

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message))
        close_button = Button(text="Close", size_hint_y=0.2, on_press=lambda instance: popup.dismiss())
        popup_layout.add_widget(close_button)
        
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup.open()

if __name__ == '__main__':
    VideoSearchApp().run()
