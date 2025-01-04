import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from rich import print


class MascotifyScraper:
    def __init__(self, base_url, max_workers=4):
        self.base_url = base_url
        self.superpet_parse = urlsplit(base_url)
        self.relevant_menu = []
        self.max_workers = max_workers  # Número de hilos para procesamiento en paralelo

    @staticmethod
    def get_soup(url: str) -> BeautifulSoup:
        """Obtiene el contenido HTML de una URL y lo convierte en un objeto BeautifulSoup."""
        html = requests.get(url).text
        return BeautifulSoup(html, "html.parser")

    def collect_relevant_menu(self):
        """Recolecta las categorías relevantes del menú."""
        html = requests.get(self.base_url).content
        soup = BeautifulSoup(html, "html.parser")
        mega_menu = soup.find("ul", id="mega-menu-primary")

        hrefs = [
            {"href": div.get("href", ""), "text": div.get_text()}
            for div in mega_menu.find_all("a", class_="mega-menu-link", href=True)
        ]

        for menu_href in hrefs:
            _url_split = urlsplit(menu_href.get("href"))
            _path = _url_split.path.split("/")
            if _url_split.netloc == self.superpet_parse.netloc and len(_path) > 2:
                if _path[2] != "":
                    menu_href["tipo"] = _path[1]
                    self.relevant_menu.append(menu_href)

    @staticmethod
    def products_first_page(url):
        """Obtiene productos y enlaces de páginas adicionales desde la primera página."""
        soup_page = MascotifyScraper.get_soup(url)

        pages_a = soup_page.find("ul", class_="page-numbers")
        pages_links = []
        if pages_a:
            pages_a = pages_a.find_all("a", href=True, class_="page-number")
            for page in pages_a:
                if page.get("href") not in pages_links:
                    pages_links.append(page.get("href"))
        return soup_page, pages_links

    @staticmethod
    def get_products_links(soup_page) -> list:
        """Obtiene los enlaces de productos de una página."""
        container_products = soup_page.find("div", class_="products")
        if not container_products:
            return []
        products = container_products.find_all("div", class_="image-zoom")
        return [
            product.find("a", href=True).get("href", "")
            for product in products
            if product.find("a", href=True)
        ]

    def get_all_data_products_in_category(self, url):
        """Obtiene todos los productos de una categoría."""
        soup_f_page, links = self.products_first_page(url)
        products = self.get_products_links(soup_f_page)

        if len(links) == 0:
            return products

        for page_link in links:
            soup_n_page = self.get_soup(page_link)
            products_n = self.get_products_links(soup_n_page)
            products.extend(products_n)
        return products

    def fetch_menu_products(self):
        """Asocia los productos con cada categoría en paralelo y muestra progreso."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(
                    self.get_all_data_products_in_category, menu["href"]
                ): menu
                for menu in self.relevant_menu
            }

            for future in tqdm(
                as_completed(futures), total=len(futures), desc="Procesando categorías"
            ):
                menu = futures[future]
                try:
                    menu["products"] = future.result()
                except Exception as e:
                    print(f"[red]Error procesando {menu['href']}: {e}[/red]")

    def save_data(self):
        """Guarda los datos en los archivos JSON requeridos."""
        if not os.path.exists("info/last"):
            os.makedirs("info/last")
        if not os.path.exists("info/history/mascotify"):
            os.makedirs("info/history/mascotify")

        # Guardar en info/last/mascotify.json
        with open("info/last/mascotify.json", "w") as last_file:
            json.dump(self.relevant_menu, last_file, indent=4)

        # Guardar en info/history/mascotify/Y-M-d.json
        today = datetime.now().strftime("%Y-%m-%d")
        history_path = f"info/history/mascotify/{today}.json"
        with open(history_path, "w") as history_file:
            json.dump(self.relevant_menu, history_file, indent=4)


# Uso de la clase
if __name__ == "__main__":
    scraper = MascotifyScraper("https://mascotify.pe/", max_workers=5)
    scraper.collect_relevant_menu()
    scraper.fetch_menu_products()
    scraper.save_data()
    print("[green]Datos recolectados y guardados exitosamente.[/green]")
