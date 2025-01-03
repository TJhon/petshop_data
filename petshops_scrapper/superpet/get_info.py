import requests 
import pandas as pd
from tqdm import tqdm
from rich import print
PRODUCT_VIEW = "https://www.superpet.pe/on/demandware.store/Sites-SuperPet-Site/es_PE/Product-ShowQuickView?pid={pid}"
data_products_id = requests.get(
    "https://raw.githubusercontent.com/TJhon/petshop_data/refs/heads/main/info/last/superpet.json"
).json()


data = []

for type_product in data_products_id:
    # print(type_product.keys())
    ids_products = type_product.get("products_id", [])
    type_objetivo = type_product.get("tipo", "")
    category = type_product.get("text", "")
    # print(ids_products)
    for _id in tqdm(ids_products):
        try:
            product_json_requests = requests.get(PRODUCT_VIEW.format(pid=_id)).json()
            product = product_json_requests.get("product")
            name = product.get("productName", "")
            marca = product.get("brand", "")
            price_dict = product.get("price", {})

            variations = product.get("variationAttributes")

            variation_qnt = ""
            price_min = None
            price_max = None


            if variations is not None:
                price_min = price_dict.get("min", {}).get("sales", {}).get("value")
                price_max = price_dict.get("max", {}).get("sales", {}).get("value")
                variation_dict = variations[0]
                variations = variation_dict.get("values", {})
                for var in variations:
                    variation_qnt += var.get("value", "") + " - "
            price_sale = price_dict.get("sales", {}).get("value", None)

            price_last = price_dict.get("list", None)
            if price_last is not None:
                price_last = price_last.get("value", None)
            short_description = product.get("shortDescription", "")
            long_description = product.get("longDescription", "")
            data_row = [
                type_objetivo,
                category,
                name,
                marca,
                price_sale,
                price_last,
                price_min,
                price_max,
                variation_qnt,
                short_description,
                # long_description,
                _id
            ]
            columns_name = [
                "Menu",
                "Categoria",
                "Nombre",
                "Marca",
                "Precio",
                "Precio Anterior (Descuento)",
                "Precio mínimo por pequeña cantidad",
                "Precio máximo por grande cantidad",
                "Variacion de cantidades",
                "Descripcion corta",
                # "Descripcion",
                "id_product"
            ]
            data.append(data_row)
        except:
            print(_id)

pd.DataFrame(data, columns=columns_name).to_excel("./raw_data/superpet.xlsx")
        # pass
