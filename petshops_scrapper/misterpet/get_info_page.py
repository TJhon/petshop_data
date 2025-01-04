import requests, re
from bs4 import BeautifulSoup
from rich import print
from tqdm import tqdm
def clean_numbers(text: str) -> float:
    "Extrae el primer número como flotante."
    match = re.search(r"\d+(\.\d+)?", text)
    if match:
        return float(match.group())
    return None


base_url = 'https://www.misterpet.pe'


def get_soup(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    return soup

def find_max_pages(soup):
    try:
        pages = soup.find('ul', class_='pagination').find_all('li')
        n_pages = [clean_numbers(n.get_text()) for n in pages]
        n_pages = [n for n in n_pages if n]
        total_pages = int(max(n_pages))
        return total_pages
    except:
        return None

def info_products_in_page(soup)-> list:

    products_div = soup.find_all('div', class_='bs-product')
    products = []
    for product in products_div:
        href = base_url+ product.find('a', href=True).get('href')
        old_price = product.find('div', class_='bs-product-old-price')
        actual_price = product.find('div', class_='bs-product-final-price').get_text()
        if old_price:
            old_price = clean_numbers(old_price.get_text())
        products.append(
            dict(href=href, old_price=old_price, actual_price=clean_numbers(actual_price))
            )
    return products

def all_info_category(url):

    soup_fp = get_soup(url)
    n_pages = find_max_pages(soup_fp)
    products = info_products_in_page(soup_fp)

    if not n_pages:
        return products

    for i in tqdm(range(2, n_pages+1)):
        new_url = url + f"?page={i}"
        soup_i = get_soup(new_url)
        products_i = info_products_in_page(soup_i)
        products.extend(products_i)
    return products
