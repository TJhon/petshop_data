import requests

from bs4 import BeautifulSoup 
from urllib import parse

from ..utils import get_soup, clean_numbers


class SuperPetPage:
    def __init__(self, url):
        self.url = url
        soup = get_soup(url)
        self.total_resultados  = self.total_result(soup)
        # print(self.total_resultados)
        # obtiene los id para hacer la peticion al json
        self.products = self.get_products_in_page(soup)
        self.cgid = self.find_more_button(soup)
        
    @staticmethod
    def total_result(soup):
        resultados = soup.find('div', class_='result-count').get_text()
    
        return clean_numbers(resultados)

    @staticmethod
    def find_more_button(soup_page):
        more_button = soup_page.find(
            "button", class_="btn btn-secondary-low col-12 col-sm-4"
        )
        if more_button is None:
            return None
        data_url = more_button.get("data-url", "")
        query_params = parse.parse_qs(parse.urlparse(data_url).query)
        cgid = query_params.get("cgid", [None])[0]
        return cgid

    @staticmethod
    def get_products_in_page(soup_page):
        productos = soup_page.find_all("div", class_="product")
        resultados = [
            str(producto["data-pid"]) for producto in productos if "data-pid" in producto.attrs
        ]
        return resultados
    @staticmethod
    def fetch_new_page(cgid, cb, start=12, sz=1000):
        # Actualizar los 
        # Construir la URL con los parámetros
        base_url = "https://www.superpet.pe/on/demandware.store/Sites-SuperPet-Site/es_PE/Search-UpdateGrid"
        params = {"cgid": cgid, "start": start, "sz": sz}

        response = requests.get(base_url, params=params)
        try:
            soup_n = BeautifulSoup(response.content, "html.parser")
            products = cb(soup_n)
            return products, soup_n
        except:
            return [], None

    def fetch_all_ids(self):
        products = self.products
        cgid = self.cgid
        
        total_n = 1000
        if total_n:
            total_n = self.total_resultados

        if not cgid:
            return products
        new_products, soup = self.fetch_new_page(cgid, self.get_products_in_page, sz=total_n)
        products.extend(new_products)
        return products
