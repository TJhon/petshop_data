
from tqdm import tqdm
from ..utils import get_soup, find_max_pages

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


