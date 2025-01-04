import os
import json
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from ..utils import clean_text, clean_numbers, get_soup, find_max_pages

# obtenet todos los href de los products
url = 'https://mascotify.pe/perros/alimento/alimento-seco/'

class MascotifyPages:
    def __init__(self, url):
        self.url = url
        soup = get_soup(url)
        self.total_pages = self.total_pages(soup)
        self.products_href = self.get_href_products_in_page(soup)
        # self.total_pages =
    @staticmethod
    def total_pages(soup):
        
        pages_ul = soup.find("ul", class_="page-numbers")
        if pages_ul:
            pages = pages_ul.find_all('a')
            max_pages = find_max_pages(pages)
            return max_pages
        return None
    @staticmethod
    def get_href_products_in_page(soup):
        container_products = soup.find("div", class_="products")
        if not container_products:
            return []
        products = container_products.find_all("div", class_="image-zoom")
        return [
            product.find("a", href=True).get("href", "")
            for product in products
            if product.find("a", href=True)
        ]
    def get_all_hrefs(self):
        total_pages = self.total_pages
        products = self.products_href
        if not total_pages:
            return products
        for n_page in tqdm(range(2, total_pages + 1)):
            if not self.url.endswith("/"):
                self.url = self.url + "/"
            new_url = self.url + f"page/{n_page}/"
            soup_n = get_soup(new_url)
            products_n = self.get_href_products_in_page(soup_n)
            products.extend(products_n)
        return products



    # @staticmethod
    # def products_first_page(url):
    #     """Obtiene productos y enlaces de páginas adicionales desde la primera página."""
    #     soup_page = get_soup(url)

    #     pages_links = []
    #     if pages_a:
    #         pages_a = pages_a.find_all("a", href=True, class_="page-number")
    #         for page in pages_a:
    #             if page.get("href") not in pages_links:
    #                 pages_links.append(page.get("href"))
    #     return soup_page, pages_links


# pass

class MascotifyDataProcessor:
    "Procesa productos y guarda en Excel."

    def __init__(self, last_json_path, output_path, max_workers=4):
        self.last_json_path = last_json_path
        self.output_path = output_path
        self.max_workers = max_workers
        self.product_urls = []

    def load_product_urls(self, filtro_text=None, filtro_tipo=None):
        "Carga las URLs de productos con filtros opcionales."
        with open(self.last_json_path, "r") as file:
            data = json.load(file)

        for category in data:
            if filtro_text and filtro_text not in category["text"].lower():
                continue

            for product in category.get("products", []):
                if filtro_tipo and filtro_tipo not in product.lower():
                    continue
                self.product_urls.append(product)
        print(f"Total URLs cargadas: {len(self.product_urls)}")

    def process_products(self):
        "Procesa los productos y guarda los resultados."
        results = []
        
        
        pbar = tqdm(total=len(self.product_urls), desc="Procesando productos")
        
        def process_url(url):
            try:
                result = ProductScraper(url).scrape_product()
                pbar.update(1)  #
                if result:
                    return result
            except Exception as e:
                print(f"Error procesando {url}: {str(e)}")
                pbar.update(1)  
                return None

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            
            futures = list(executor.map(process_url, self.product_urls))
            
            
            results = [r for r in futures if r]

        pbar.close()  

        df = pd.DataFrame(results)
        df.rename(
            columns={
                "menu": "Menu",
                "category": "Categoria",
                "name": "Nombre",
                "brand": "Marca",
                "price": "Precio",
                "last_precio": "Precio Anterior (Descuento)",
                "price_min": "Precio Minimo por Pequeña Cantidad",
                "price_max": "Precio Maximo por Grande Cantidad",
                "range_prices": "Precios para Cada Cantidad",
                "range_qnts": "Cantidades Disponibles",
                "s_description": "Descripcion Corta",
                "l_description": "Descripcion Larga",
                "url": "URL",
            },
            inplace=True,
        )

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        df.to_excel(self.output_path, index=False)

if __name__ == "__main__":
    processor = MascotifyDataProcessor(
        last_json_path="info/last/mascotify.json",
        output_path="raw_data/mascotify.xlsx",
        max_workers=30,
    )

    processor.load_product_urls()
    processor.process_products()