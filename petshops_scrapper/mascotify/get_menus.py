from urllib.parse import urlsplit
from ..utils import get_soup, save_array

class MascotifyMenu:
    def __init__(self, url="https://mascotify.pe/"):
        self.soup = get_soup(url)
        self.relevant_menu = []
        self.superpet_parse = urlsplit(url)
        self.collect_relevant_menu()
        save_array(self.relevant_menu, "Mascotify", 'info/menu')
        
    def collect_relevant_menu(self):
        
        mega_menu = self.soup.find("ul", id="mega-menu-primary")

        hrefs = [
            {"href": div.get("href", ""), "category": div.get_text()}
            for div in mega_menu.find_all("a", class_="mega-menu-link", href=True)
        ]

        for menu_href in hrefs:
            _url_split = urlsplit(menu_href.get("href"))
            _path = _url_split.path.split("/")
            if _url_split.netloc == self.superpet_parse.netloc and len(_path) > 2:
                if _path[2] != "":
                    menu_href["type"] = _path[1]
                    self.relevant_menu.append(menu_href)
