# obtener todos los hrefs
from ..utils import get_soup, find_max_pages, clean_numbers
from tqdm import tqdm

url = "https://www.misterpet.pe/collection/alimento-seco-para-perro"


class MisterPetPages:
    def __init__(self, url, base_url = 'https://www.misterpet.pe'):
        self.url = url
        soup = get_soup(url)
        self.soup = soup
        self.base_url = base_url
        self.total_pages = self.total_pages(soup)
        self.products = self.info_products_in_page(soup, base_url)

    @staticmethod
    def total_pages(soup):
        pagination = soup.find("ul", class_="pagination")
        if not pagination:
            return None
        pages = pagination.find_all("li")
        total_pages = find_max_pages(pages)
        return total_pages

    @staticmethod
    def info_products_in_page(soup, url) -> list:

        products_div = soup.find_all("div", class_="bs-product")
        products = []
        for product in products_div:
            href = url + product.find("a", href=True).get("href")
            old_price = product.find("div", class_="bs-product-old-price")
            actual_price = product.find(
                "div", class_="bs-product-final-price"
            ).get_text()
            if old_price:
                old_price = clean_numbers(old_price.get_text())
            products.append(
                dict(
                    href=href,
                    last_price=old_price,
                    actual_price=clean_numbers(actual_price),
                )
            )
        return products
    def get_all_hrefs(self):
        total_pages = self.total_pages
        products = self.products

        if not total_pages:
            return products
        for n_page in tqdm(range(2, total_pages + 1)):
            new_url = url + f"?page={n_page}"
            soup_i = get_soup(new_url)
            products_i = self.info_products_in_page(soup_i, self.base_url)
            products.extend(products_i)
        return products
        

