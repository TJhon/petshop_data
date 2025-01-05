
from ..utils import save_array, get_soup, find_max_pages
from tqdm import tqdm

class PharmivetPages:
    def __init__(self, url):
        self.url = url
        soup = get_soup(url)
        self.max_pages = self.total_pages(soup)
        self.products_href = self.get_href_products_in_pages(soup)

    @staticmethod
    def total_pages(soup):
        navs = soup.find("ul", class_="page-list")
        if navs:
            pages = navs.find_all("a")
            max_pages = find_max_pages(pages)
            return max_pages 
        return None
    @staticmethod
    def get_href_products_in_pages(soup):
        products = soup.find("div", class_="products")
        a = products.find_all("a", href=True, class_="thumbnail")
        href = [_.get("href", "") for _ in a]
        return href
    def get_all_hrefs(self):
        total_pages = self.max_pages
        products = self.products_href
        if not total_pages:
            return products
        for n_page in tqdm(range(2, total_pages + 1)):
            new_url = self.url + f"?page={n_page}"
            soup_n = get_soup(new_url)
            products_n = self.get_href_products_in_pages(soup_n)
            products.extend(products_n)
        return products



# class MenuProductsPhamivet:
#     def __init__(self, url_menu=urls):
#         self.data_url = url_menu

#     @staticmethod
#     def get_soup(url):
#         content = requests.get(url).content
#         soup = BeautifulSoup(content, "html.parser")
#         return soup

#     @staticmethod
#     def find_products_in_page(soup):

#     @staticmethod
#     def find_max_pages(soup):
#         try:
#             nav_text = [clean_numbers(nav.get_text()) for nav in navs]
#             nav_text = [nav for nav in nav_text if nav is not None]
#             max_pages = int(max(nav_text))
#             return max_pages
#         except:
#             return None

    def get_products(self):
        data = self.data_url
        for menu in data[:2]:
            url_menu = menu.get("url")
            first_page = self.get_soup(url_menu)
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
#     def get_data(self):
#         self.data




# MenuProductsPhamivet().get_products()


# # https://pharmivet.pe/94-medicamentos?page=3
