from ..utils import get_soup, find_max_pages, print
from tqdm import tqdm

# url = 'https://mascotaveloz.pe/perros/alimento-perros/'
# soup = get_soup(url)

class MascotaVelozPages:
    def __init__(self, url):
        self.url = url
        soup = get_soup(url)
        self.total_pages = self.total_pages(soup)
        self.products_href = self.get_href_products_in_page(soup)
    @staticmethod
    def total_pages(soup):
        pages_ul = soup.find('ul', class_='page-numbers')
        if pages_ul:
            pages = pages_ul.find_all('li')
            max_pages = find_max_pages(pages)
            return max_pages
        return None

    @staticmethod
    def get_href_products_in_page(soup):
        products_title = soup.find('ul', class_='products').find_all('h2')
        products = [product.find('a', href=True).get('href') for product in products_title]
        return products
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



    

# print(soup.prettify())

