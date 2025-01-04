from bs4 import BeautifulSoup
import requests
from rich import print
from urllib.parse import urlsplit
from ..utils import save_array

url = 'https://mascotaveloz.pe'

class MascotaVelozMenu:
    def __init__(self, url=url):
        soup = self.get_soup(url)
        menu = self.get_menu(soup)
        save_array(menu, 'MascotaVeloz', "info/menu")
        self.data = menu
    @staticmethod
    def get_soup(url):
        
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        return soup
    @staticmethod
    def get_menu(soup):
        menu = soup.find('ul', id='menu-principal')
        sub_menus = menu.find_all('a', href=True)

        menu_href = []
        for s in sub_menus:
            href = s.get('href')
            text = s.get_text().title()
            if not href.startswith("/"):
                url_split = urlsplit(href).path
                path = url_split.split("/")
                tipo = path[1]
                if len(path) < 3:
                    tipo = "otros"
                menu_href.append({"href": href, "type": tipo, "category": text})
        return menu_href

        
# MascotaVelozMenu()