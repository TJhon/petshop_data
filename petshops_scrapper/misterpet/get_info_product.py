import requests
from bs4 import BeautifulSoup

def get_product_info(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    product_name = soup.find('h1')
    brand = product_name.find_next("a")

    description = product_name.find_next('section', class_='bs-product-description')
    actual_price = product_name.find_next('span', class_='h2')

    info_product = dict(
        product_name = product_name.get_text(),
        brand = brand.find('img').get('title', None),
        description = description,
        actual_price = actual_price
    )

    return info_product