import requests
from bs4 import BeautifulSoup
from rich import print
from ..utils import save_array, get_soup

base_url = 'https://www.misterpet.pe'


class MisterPetMenu:
    def __init__(self, url=base_url, drop_begin=2, drop_final=2):
        soup = get_soup(url)
        menu = self.drop_not_menu(soup, drop_begin, drop_final)
        data_menu = self.collect_relevant_menu(menu)
        save_array(data_menu, 'MisterPet', 'info/menu')
        self.data = data_menu
    
    def collect_relevant_menu(self, menu):
        a_s = []
        for m in menu:
            inside_a:list = m.find_all('a', href=True)
            _ai = [
                {
                    "href":  base_url + ref.get('href', ""),
                    "category": ref.get('title', ''),
                }
                for ref in inside_a
                if ref.get('href') != ""
            ]
            tipo = ''
            for i, a in enumerate(_ai):
                if a.get('href').strip().endswith('#'):
                    tipo = a.get('category')
                a['type'] = tipo
            _ai = [_a for _a in _ai if not _a.get('href').endswith('#')]

            a_s.extend(_ai)
        return a_s
    @staticmethod
    def drop_not_menu(soup, drop_b, drop_f):
        menu = soup.find_all('li', class_='nav-item')
        menu = menu[drop_b:-drop_f]
        return menu


