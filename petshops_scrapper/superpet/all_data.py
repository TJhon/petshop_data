from ..utils import load_json_menu, print, save_array, exists_products
from .products_in_page import SuperPetPage
from tqdm import tqdm
NAME = 'SuperPet'


class SuperPet:
    def __init__(self, local=True, n_workers=10, save_products = "info/products"):
        print(f'{NAME} ====================== ')
        self.data = load_json_menu(NAME, type="menu")
        self.save_products = save_products
        self.n_workers=n_workers
        if not local or not exists_products(NAME):
            self.fetch_product_online()
        else:
            self.data = load_json_menu(NAME, type='products')

    def fetch_product_online(self):

        print(f'{NAME}: Extrayendo Lista de productos')
        for ref_data in tqdm(self.data):
            href = ref_data.get("href")
            all_ids = SuperPetPage(href).fetch_all_ids()
            ref_data['id_s'] = all_ids
        save_array(self.data, NAME, self.save_products)
        return self
