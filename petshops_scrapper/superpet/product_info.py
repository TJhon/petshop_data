import requests 
PRODUCT_VIEW = "https://www.superpet.pe/on/demandware.store/Sites-SuperPet-Site/es_PE/Product-ShowQuickView?pid={pid}"

def information_product(_id, type=None, category=None):
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
        href = 'https://www.superpet.pe' + product_json_requests.get('productUrl', "")
        data_row = dict(
            type = type,
            category = category,
            product_name = name,
            brand = marca,
            actual_price = price_sale,
            last_price = price_last,
            min_price = price_min,
            max_price = price_max,
            variation_qnt = variation_qnt,
            s_description = short_description,
            long_description = long_description,
            href = href,
            id = _id
        )
        return data_row
        
    except:
        print(_id)
        pass


