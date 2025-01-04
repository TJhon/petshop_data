import os
import json
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def clean_text(text: str) -> str:
    "Elimina espacios innecesarios."
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_numbers(text: str) -> float:
    "Extrae el primer número como flotante."
    match = re.search(r"\d+(\.\d+)?", text)
    if match:
        return float(match.group())
    return None

def get_soup(url: str) -> BeautifulSoup:
    "Obtiene el HTML de una URL."
    html = requests.get(url).text
    return BeautifulSoup(html, "html.parser")

class ProductScraper:
    "Extrae información de productos."

    def __init__(self, url: str):
        self.url = url
        self.soup = get_soup(url)

    def scrape_product(self) -> dict:
        "Extrae los detalles de un producto."
        try:
            category_nav = self.soup.find("nav", id="breadcrumbs")
            if category_nav:
                categories = category_nav.find_all("a")
                categories = [cat.get_text() for cat in categories]
                menu = categories[1]
                category = " - ".join(categories[2:])
            else:
                menu, category = None, None

            h1 = self.soup.find("h1", class_="product-title")
            brand = (
                h1.find_next("div", class_="marca-product-page")
                .find_next("div")
                .get_text()
            )
            short_description = h1.find_next(
                "div", class_="product-short-description"
            ).get_text()
            long_description_divs = self.soup.find("div", class_="panel entry-content")

            last_price = h1.find_next("del")
            actual_price = h1.find_next("ins")

            price_min, price_max, qnts, prices = None, None, [], []
            prices_str, qnts_str = None, None

            if last_price:
                last_price = clean_numbers(last_price.get_text())

            if actual_price:
                actual_price = clean_numbers(actual_price.get_text())

            variation_data = self.soup.find("form", class_="variations_form")
            if variation_data:
                variation_json = variation_data.get("data-product_variations")
                variations = json.loads(variation_json)

                for variation in variations:
                    qnt_i = variation["attributes"]["attribute_pa_presentacion"]
                    qnts.append(qnt_i)
                    price = variation["display_price"]
                    prices.append(price)
                price_min = min(prices)
                price_max = max(prices)

                prices_str = " - ".join(map(str, prices))
                qnts_str = " - ".join(qnts)

            return {
                "menu": menu,
                "category": category,
                "name": clean_text(h1.get_text()),
                "brand": clean_text(brand),
                "price": actual_price,
                "last_precio": last_price,
                "price_min": price_min,
                "price_max": price_max,
                "range_prices": prices_str,
                "range_qnts": qnts_str,
                "s_description": clean_text(short_description),
                "l_description": clean_text(
                    long_description_divs.get_text() if long_description_divs else ""
                ),
                "url": self.url,
            }
        except Exception:
            return {}

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