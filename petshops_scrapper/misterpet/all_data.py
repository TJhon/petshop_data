from ..utils import get_soup, load_json_menu, print, save_array, exists_products
from .products_in_page import MisterPetPages
NAME = "MISTERPET"

class MisterPet:
    def __init__(self, local=True, n_workers=10,  save_products = 'info/products'):

        print(f'{NAME} ====================== ')
        self.data = load_json_menu(NAME, type='menu')
        self.save_products = save_products
        self.n_workers = n_workers
        if not local or not exists_products(NAME):
            self.fetch_product_online()
        else:
            self.data = load_json_menu(NAME, type="products")
    def fetch_product_online(self):

        # print('Extrayendo Lista de productos')

        print(f'{NAME}: Extrayendo Lista de productos')
        for ref_data in self.data:
            href = ref_data.get("href")
            all_products_href =  MisterPetPages(href).get_all_hrefs()
            ref_data['products_href'] = all_products_href
        save_array(self.data, NAME, self.save_products)
        return self
  