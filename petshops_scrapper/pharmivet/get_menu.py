import requests, re
from bs4 import BeautifulSoup
from rich import print
from tqdm import tqdm

main = requests.get("https://pharmivet.pe/94-medicamentos")
urls = [
    {"type": "medicamentos", "url": "https://pharmivet.pe/94-medicamentos"},
    {"type": "alimentos", "url": "https://pharmivet.pe/95-alimentos"},
    {"type": "suplementos", "url": "https://pharmivet.pe/96-suplementos"},
    {"type": "antipulgas", "url": "https://pharmivet.pe/97-antipulgas"},
    {"type": "oculares", "url": "https://pharmivet.pe/98-oculares"},
    {"type": "cardiologicos", "url": "https://pharmivet.pe/99-cardiologicos"},
    {"type": "oticos", "url": "https://pharmivet.pe/101-oticos"},
    {"type": "higiene_cuidado", "url": "https://pharmivet.pe/102-higiene-y-cuidado"},
    {"type": "perros", "url": "https://pharmivet.pe/136-perros"},
    {"type": "gatos", "url": "https://pharmivet.pe/137-gatos"},
    {"type": "promocion", "url": "https://pharmivet.pe/215-promocion"},
    {"type": "ultimas_unidades", "url": "https://pharmivet.pe/230-ultimas-unidades"},
]


def clean_numbers(text: str) -> float:
    "Extrae el primer número como flotante."
    match = re.search(r"\d+(\.\d+)?", text)
    if match:
        return float(match.group())
    return None


class MenuProductsPhamivet:
    def __init__(self, url_menu=urls):
        self.data_url = url_menu

    @staticmethod
    def get_soup(url):
        content = requests.get(url).content
        soup = BeautifulSoup(content, "html.parser")
        return soup

    @staticmethod
    def find_products_in_page(soup):
        products = soup.find("div", class_="products")
        a = products.find_all("a", href=True, class_="thumbnail")
        href = [_.get("href", "") for _ in a]
        return href

    @staticmethod
    def find_max_pages(soup):
        try:
            navs = soup.find("ul", class_="page-list").find_all("a")
            nav_text = [clean_numbers(nav.get_text()) for nav in navs]
            nav_text = [nav for nav in nav_text if nav is not None]
            max_pages = int(max(nav_text))
            return max_pages
        except:
            return None

    def get_products(self):
        data = self.data_url
        for menu in data[:2]:
            url_menu = menu.get("url")
            first_page = self.get_soup(url_menu)
            # navs = first_page.find("ul", class_="page-list").find_all("a")
            # nav_text = [clean_numbers(nav.get_text()) for nav in navs]
            # print(nav_text)
            total_pages = self.find_max_pages(first_page)
            products_fp = self.find_products_in_page(first_page)
            pages_url = [url_menu + f"?page={n}" for n in list(range(2, total_pages + 1))]
            menu['url_pages'] = pages_url 
            menu['products'] = products_fp
        for menu in data[:2]:
            actual_products = menu.get('products')
            url_pages = menu.get('url_pages')
            if len(url_pages) < 1:
                continue
            for url_page in tqdm(url_pages):
                soup_page = self.get_soup(url_page)
                products_page = self.find_products_in_page(soup_page)
                actual_products.extend(products_page)

        self.data = data
    def get_data(self):
        self.data




MenuProductsPhamivet().get_products()


# https://pharmivet.pe/94-medicamentos?page=3
