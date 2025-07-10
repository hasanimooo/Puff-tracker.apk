
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
import time

store = JsonStore('puff_data.json')

def today():
    return datetime.now().strftime("%Y-%m-%d")

class PuffTracker(BoxLayout):
    sabah = NumericProperty(0)
    ogle = NumericProperty(0)
    gece = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.load_data()
        self.create_ui()
        self.start_time = None

    def load_data(self):
        key = today()
        if store.exists(key):
            data = store.get(key)
            self.sabah = data.get('sabah', 0)
            self.ogle = data.get('ogle', 0)
            self.gece = data.get('gece', 0)

    def save_data(self):
        store.put(today(), sabah=self.sabah, ogle=self.ogle, gece=self.gece)

    def create_ui(self):
        self.sabah_label = Label(text=f"Sabah: {self.sabah}")
        self.ogle_label = Label(text=f"Öğle: {self.ogle}")
        self.gece_label = Label(text=f"Gece: {self.gece}")
        self.total_label = Label(text=f"Toplam: {self.sabah + self.ogle + self.gece}")

        self.add_widget(self.sabah_label)
        self.add_widget(Button(text="+1 Sabah", on_press=lambda _: self.update_count('sabah')))

        self.add_widget(self.ogle_label)
        self.add_widget(Button(text="+1 Öğle", on_press=lambda _: self.update_count('ogle')))

        self.add_widget(self.gece_label)
        self.add_widget(Button(text="+1 Gece", on_press=lambda _: self.update_count('gece')))

        self.add_widget(Button(text="⬇️ Basılı Tut: Puff Çekimi Başlat", on_press=self.start_timer, on_release=self.stop_timer))

        self.add_widget(self.total_label)

    def update_count(self, section, amount=1):
        if section == 'sabah':
            self.sabah += amount
            self.sabah_label.text = f"Sabah: {self.sabah}"
        elif section == 'ogle':
            self.ogle += amount
            self.ogle_label.text = f"Öğle: {self.ogle}"
        elif section == 'gece':
            self.gece += amount
            self.gece_label.text = f"Gece: {self.gece}"

        self.total_label.text = f"Toplam: {self.sabah + self.ogle + self.gece}"
        self.save_data()

    def start_timer(self, instance):
        self.start_time = time.time()

    def stop_timer(self, instance):
        if self.start_time:
            duration = time.time() - self.start_time
            self.start_time = None
            puff_count = 0

            if 0 < duration <= 1:
                puff_count = 1
            elif 1 < duration <= 2:
                puff_count = 2
            elif 2 < duration <= 3:
                puff_count = 3
            elif duration >= 4:
                self.show_warning("Uyarı: Çok uzun çekim! (4 saniye +)")

            self.update_count('gece', puff_count)

    def show_warning(self, message):
        content = FloatLayout()
        popup = Popup(title='Uyarı', content=Label(text=message), size_hint=(0.6, 0.3))
        popup.open()

class PuffTrackerApp(App):
    def build(self):
        return PuffTracker()

if __name__ == '__main__':
    PuffTrackerApp().run()
