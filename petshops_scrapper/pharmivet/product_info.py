import requests
from bs4 import BeautifulSoup
from ..utils import get_soup, clean_numbers


url = 'https://pharmivet.pe/alimentos/431-hill_s-canine-id-85-lb-x-385-kg-8240302008.html'
# url = 'https://pharmivet.pe/promocion/1511-liquidacion_pd-feline-onc-care-ckn_vg-stew-29-oz-82-g-82403020531.html'

def information_product(url, category = None, type = None):
    try:
        soup = get_soup(url)

        name_product = soup.find('h1')

        prices = name_product.find_next('div', class_ = 'current-price')
        actual_price = clean_numbers(prices.find('span', itemprop='price').get_text())
        last_price = prices.find('span', class_='regular-price')
        if last_price:
            last_price = clean_numbers(last_price.get_text())
        description = name_product.find_next('div', class_ = 'product-information').find('div')


        return dict(
            type=type,
            category=category,
            product_name = name_product.get_text(),
            s_description = description.get_text(),
            actual_price = actual_price,
            last_price = last_price,
            href = url
            )
    except:
        print(url)
        pass

