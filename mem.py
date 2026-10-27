from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButton
from kivy_garden.mapview import MapView, MapMarker
from kivy.network.urlrequest import UrlRequest
import urllib.parse

class NavigacioKepernyo(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Alapértelmezett térkép (Magyarország közepére illesztve)
        self.mapview = MapView(zoom=11, lat=47.4979, lon=19.0402)
        self.add_widget(self.mapview)
        
        # Felső magyar keresősáv
        self.search_field = MDTextField(
            hint_text="Keresés (pl. Eger, Dobó tér)...",
            size_hint_x=0.85,
            pos_hint={'center_x': 0.5, 'top': 0.98},
            mode="round",
            fill_color_normal=(1, 1, 1, 0.9)
        )
        self.search_field.bind(on_text_validate=self.kereses_inditasa)
        self.add_widget(self.search_field)
        
        # Lebegő GPS gomb a jobb alsó sarokban
        self.gps_btn = MDFloatingActionButton(
            icon="crosshairs-gps",
            pos_hint={'right': 0.95, 'y': 0.05},
            on_release=self.sajat_pozicio
        )
        self.add_widget(self.gps_btn)
        
        self.marker = None

    def kereses_inditasa(self, instance):
        szoveg = self.search_field.text
        if not szoveg:
            return
        
        # Magyar nyelvű keresés a Nominatim API-val
        encoded = urllib.parse.quote(szoveg)
        url = f"https://nominatim.openstreetmap.org/search?q={encoded}&format=json&accept-language=hu&limit=1"
        headers = {'User-Agent': 'SajatNavigacioApp/1.0'}
        
        UrlRequest(url, req_headers=headers, on_success=self.talalat_feldolgozasa)

    def talalat_feldolgozasa(self, request, result):
        if result and len(result) > 0:
            lat = float(result[0]['lat'])
            lon = float(result[0]['lon'])
            
            # Térkép mozgatása a kiválasztott koordinátára
            self.mapview.center_on(lat, lon)
            self.mapview.zoom = 15
            
            # Jelölő elhelyezése
            if self.marker:
                self.mapview.remove_marker(self.marker)
            self.marker = MapMarker(lat=lat, lon=lon)
            self.mapview.add_marker(self.marker)

    def sajat_pozicio(self, instance):
        # Példa koordináta (Eger) a GPS teszteléséhez
        self.mapview.center_on(47.9026, 20.3732)
        self.mapview.zoom = 15

class NavigacioApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return NavigacioKepernyo()

if __name__ == '__main__':
    NavigacioApp().run()
