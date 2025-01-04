import requests
from bs4 import BeautifulSoup

url = 'https://pharmivet.pe/alimentos/431-hill_s-canine-id-85-lb-x-385-kg-8240302008.html'
url = 'https://pharmivet.pe/promocion/1511-liquidacion_pd-feline-onc-care-ckn_vg-stew-29-oz-82-g-82403020531.html'
soup = BeautifulSoup(requests.get(url).content, 'html.parser')

name_product = soup.find('h1')

prices = name_product.find_next('div', class_ = 'current-price')
actual_price = prices.find('span', itemprop='price')
last_price = prices.find('span', class_='regular-price')
description = name_product.find_next('div', class_ = 'product-information').find('div')

print(name_product.get_text(), actual_price.get_text(), last_price.get_text())#, description.get_text())

