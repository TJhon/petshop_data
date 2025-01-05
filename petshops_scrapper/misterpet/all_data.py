from ..utils import get_soup, load_json_menu, print, save_array, exists_products
from .products_in_page import MisterPetPages
from .product_info import information_product
from tqdm import tqdm
import pandas as pd, os
from concurrent.futures import ThreadPoolExecutor

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
    def fetch_all_information(self, dir = 'raw_data'):
        data = self.data
        detailed_information = []

        # todo: borrar el limite
        for ref_data in data:
            type = ref_data.get('type')
            category = ref_data.get('category')
            try:
                products_href = ref_data.get('products_href', [])
    
                if len(products_href) == 0:
                    continue
                def process_product(product, category, type):
                    product_href = product.get('href')
                    last_price = product.get('last_price')
                    info_products = information_product(product_href, category=category, type=type)
                    info_products['last_price'] = last_price
                    return info_products
                with ThreadPoolExecutor(max_workers=self.n_workers) as executor:
                    futures = [
                        executor.submit(process_product, product, category, type)
                        # for 
                        for product in products_href
                    ]
                    for future in tqdm(futures):
                        result = future.result()
                        detailed_information.append(result)
        # todo: borrar el limite
                # for product in tqdm(products_href[:10]):
                #     product_href = product.get('href')
                #     last_price = product.get('last_price')
                #     info_products = information_product(product_href, category=category, type=type)
                #     info_products['last_price'] = last_price
                #     detailed_information.append(info_products)
            except:
                print(ref_data)
                pass

        data_ = pd.DataFrame(detailed_information)

        file_xlsx = os.path.join(dir, NAME +".xlsx")
        data_.to_excel(file_xlsx)
        return data_
    