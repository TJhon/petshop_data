import requests
from bs4 import BeautifulSoup
from rich import print
from ..utils import save_array

base_url = 'https://www.misterpet.pe'

DROP_BEGIN = 2 
DROP_FINAL = 2 # contacto, trabaja con notrosl
def get_soup(url=base_url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    return soup

def drop_not_menu(soup, drop_b=DROP_BEGIN, drop_f=DROP_FINAL):
    menu = soup.find_all('li', class_='nav-item')
    menu = menu[drop_b:-drop_f]
    return menu

# menu = menu[:-]

def get_menu(menu):
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


class MisterPetMenu:
    def __init__(self, url=base_url):
        soup = get_soup(url)
        menu = drop_not_menu(soup)
        data_menu = get_menu(menu)
        save_array(data_menu, 'MisterPet', 'info/menu')
        self.data = data_menu