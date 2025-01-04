from ..utils import get_soup, load_json_menu, print, save_array
from .products_in_page import MascotifyPages
from .product_info import information_product
from tqdm import tqdm
import pandas as pd



NAME = 'Mascotify'

# data = load_json_menu(NAME)[:3]

class Mascotify:
    def __init__(self, save_products = "info/products"):
        self.data = load_json_menu(NAME, type="menu")
        self.save_products = save_products
    def fetch_product_online(self):
        for ref_data in self.data[:2]:
            href = ref_data.get("href")
            all_products_href =  MascotifyPages(href).get_all_hrefs()
            ref_data['products_href'] = all_products_href
        save_array(self.data, NAME, self.save_products)
        return self

    def fetch_all_information(self):
        data = self.data
        detailed_information = []
        for ref_data in data[:2]:
            try:
                products_href = ref_data.get("products_href", [])[:3]
                if len(products_href) == 0:
                    continue
                category = ref_data.get("category")
                type = ref_data.get('type')
                for product_href in tqdm(products_href):
                    info_products = information_product(product_href)
                    detailed_information.append(info_products)
            except:
                print(ref_data.get(ref_data))
        data_ = pd.DataFrame(detailed_information)
        return data_