import requests, json, re
from bs4 import BeautifulSoup
from rich import print

def clean_text(text: str) -> str:
    """Elimina espacios innecesarios en un texto."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_numbers(text: str) -> float:
    """Extrae el primer número de un texto como flotante."""
    match = re.search(r"\d+(\.\d+)?", text)
    if match:
        return float(match.group())
    return None

def get_soup(url: str) -> BeautifulSoup:
    """Obtiene el contenido HTML de una URL y lo convierte en un objeto BeautifulSoup."""
    html = requests.get(url).text
    return BeautifulSoup(html, "html.parser")

class MascotifyScraper:
    """Clase para extraer información de productos desde una página web."""

    def __init__(self, url: str):
        self.url = url
        self.soup = get_soup(url)

    def find_basic_elements(self) -> dict:
        """Extrae los elementos básicos de un producto."""
        category_nav = self.soup.find('nav', id = 'breadcrumbs')
        if category_nav:
            categories = category_nav.find_all('a')
            categories = [cat.get_text() for cat in categories]
            menu = categories[1]
            category = " - ".join(categories[2:])

        h1 = self.soup.find("h1", class_="product-title")
        brand = h1.find_next("div", class_="marca-product-page").find_next("div").get_text()
        short_description = h1.find_next(
            "div", class_="product-short-description"
        ).get_text()
        long_description_divs = self.soup.find('div', class_='panel entry-content')

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
            try:
                variation_json = variation_data.get("data-product_variations")
                variations = json.loads(variation_json)

                for variation in variations:
                    qnt_i = variation["attributes"]["attribute_pa_presentacion"]
                    qnts.append(qnt_i)
                    price = variation["display_price"]
                    prices.append(price)
                price_min = min(prices)
                price_max = max(prices)

                prices_str = " - ".join([str(x) for x in prices])
                qnts_str = " - ".join(qnts)
            except Exception as e:
                print(f"Error parsing variations: {e}")

        return {
            "menu": menu,
            "category": category,
            "name": clean_text(h1.get_text()),
            "brand": clean_text(brand),
            "precio": actual_price,
            "last_precio": last_price,
            "price_min": price_min,
            "price_max": price_max,
            "range_prices": prices_str,
            "range_qnts": qnts_str,
            "s_description": clean_text(short_description),
            "l_description": clean_text(long_description_divs.get_text() if long_description_divs else "")
        }

# Ejemplo de uso
url = "https://mascotify.pe/gatos/accesorios-y-otros-gatos/juguetes-gatos/catit-groovy-fish-juguete-para-gatos/"
url = 'https://mascotify.pe/gatos/alimento-gatos/leches-y-formulas-gatos/petag-kmr-sustituto-de-leche-en-polvo-para-gatitos/'
url = 'https://mascotify.pe/otros/conejos/brit-animals-rabbit-adult-complete/'
url = 'https://mascotify.pe/perros/accesorios-y-otros/platos-bebederos/ferplast-contenedor-feedy-para-comida-seca/'
scraper = MascotifyScraper(url)
data = scraper.find_basic_elements()
print(data)
