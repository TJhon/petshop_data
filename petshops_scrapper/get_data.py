import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from .utils import load_json_menu
from rich import print
from .mascota_veloz.product_info import information_product as mascota_veloz_cb
from .pharmivet.product_info import information_product as pharmivet_cb
from .mascotify.product_info import information_product as mascotify_cb
from .misterpet.product_info import information_product as misterpet_cb
from .superpet.product_info import information_product as supertpet_cb

NAMES = {
    "SuperPet": {"col": "id_s", "func": supertpet_cb},
    "MascotaVeloz": {"col": "products_href", "func": mascota_veloz_cb},
    "Mascotify": {"col": "products_href", "func": mascotify_cb},
    "PharmiVet": {"col": "products_href", "func": pharmivet_cb},
    "MisterPet": {
        "col": "products_href",
        "col_rel": "href",
        "func": misterpet_cb,
    }, 
}

class DataProcessor:
    def __init__(self, workers_per_company, names):
        self.workers_per_company = workers_per_company
        self.names = names

    def convert_to_df(self, name_key):
        data = load_json_menu(name=name_key, type="products")
        data = pd.DataFrame(data).drop(columns=["href"])

        col_expand = self.names.get(name_key).get("col")
        df_exploded = data.explode(col_expand)

        if name_key.lower() == "misterpet":
            df_exploded = pd.concat(
                [
                    df_exploded.drop(columns=[col_expand]),
                    df_exploded[col_expand].apply(pd.Series),
                ],
                axis=1,
            )

            df_exploded = df_exploded.dropna(subset="href")
            df_exploded = df_exploded.drop(columns=[0])
        
        df_exploded["companny_name"] = name_key
        # df_exploded = df_exploded.groupby('companny_name').sample(100)
        return df_exploded

    def process_row(self, row):
        key_i = row["companny_name"]
        name_values = self.names.get(key_i)
        relevant_col = name_values.get("col")
        CB = name_values.get("func")

        if name_values.get("col_rel"):
            relevant_col = name_values.get("col_rel")
        if not CB or pd.isna(row[relevant_col]):
            return None

        info = {}
        try:
            if key_i.lower() in ["mascotaveloz", "pharmivet", "mascotify", "misterpet"]:
                info = CB(row[relevant_col], category=row["category"], type=row["type"])
            else:
                info = CB(row[relevant_col], category=row["category"], type=row["type"])

            if key_i.lower() == "misterpet":
                info.update({
                    "type": row["type"],
                    "category": row["category"],
                    "href": row[relevant_col],
                    "last_price": row["last_price"],
                    "actual_price": row["actual_price"],
                })

            info["companny_name"] = row["companny_name"]
            return info
        except Exception as e:
            print(f"Error processing row {row.name}: {e}")
            return None

    def process_dataframe_parallel(self, df):
        results = []

        for company in df['companny_name'].unique():
            company_data = df[df['companny_name'] == company]

            max_workers = self.workers_per_company.get(company, 1)

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(self.process_row, row): i for i, row in company_data.iterrows()}

                for future in tqdm(as_completed(futures), total=len(futures), desc=f"Procesando {company}"):
                    try:
                        result = future.result()
                        if result is not None:
                            results.append(result)
                    except Exception as e:
                        print(f"Error procesando: {e}")

            company_data_info = pd.DataFrame(results).drop_duplicates()
            company_file_path = f"./raw_data/{company}.xlsx"
            company_data_info.to_excel(company_file_path, index=False)
            print(f"Archivo guardado: {company_file_path}")

        return results

    def process_all(self):
        data = [self.convert_to_df(n) for n in self.names.keys()]
        all_data = pd.concat(data, ignore_index=True)

        all_data.to_csv("./raw_data/0_products_ref.csv", index=False)
        print("Todos los productos de las empresas guardado en: ./raw_data/0_products_ref.csv")

        data_info_list = self.process_dataframe_parallel(all_data)
        data_info = pd.DataFrame(data_info_list).drop_duplicates()

        orden = [
            "companny_name", "type", "category", "brand", "product_name",
            "actual_price", "last_price", "price_min", "price_max",
            "range_qnts", "range_prices", "s_description", "l_description",
            "href", "id"
        ]
        data_info[orden].to_excel("./raw_data/1_data.xlsx")
        print("Archivo final guardado: ./raw_data/1_data.csv")
