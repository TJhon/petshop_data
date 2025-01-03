import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from rich import print

url = "https://mascotify.pe/"
superpet_parse = urlsplit(url)
html = requests.get(url).content

soup = BeautifulSoup(html, "html.parser")


mega_menu = soup.find("ul", id="mega-menu-primary")


hrefs = [
    {"href": div.get("href", "")}
    for div in mega_menu.find_all("a", class_="mega-menu-link", href=True)
]


def get_soup(url: str) -> BeautifulSoup:
    """Obtiene el contenido HTML de una URL y lo convierte en un objeto BeautifulSoup."""
    html = requests.get(url).text
    return BeautifulSoup(html, "html.parser")


relevant_menu = []
for menu_href in hrefs:
    _url_split = urlsplit(menu_href.get("href"))
    _path = _url_split.path.split("/")
    if _url_split.netloc == superpet_parse.netloc and len(_path) > 2:
        if _path[2] != "":
            menu_href["tipo"] = _path[1]
            relevant_menu.append(menu_href)

# print(relevant_menu)
url_sample = "https://mascotify.pe/gatos/accesorios-y-otros-gatos/"
# url_sample = 'https://mascotify.pe/otros/aves/'

N = 20


def products_first_page(url):
    soup_page = get_soup(url)

    pages_a = soup_page.find("ul", class_="page-numbers")
    pages_links = []
    if pages_a:
        pages_a = pages_a.find_all("a", href=True, class_="page-number")
        pages_links = []
        for page in pages_a:
            if page.get("href") not in pages_links:
                pages_links.append(page.get("href"))
    return soup_page, pages_links


def get_products_links(soup_page) -> list:
    container_products = soup_page.find("div", class_="products")
    products = container_products.find_all("div", class_="image-zoom")
    anclas_products = [
        product.find("a", href=True).get("href", "") for product in products
    ]
    # retornar los productos, more_products?, total_pages
    return anclas_products


def get_all_data_products_in_category(url):

    soup_f_page, links = products_first_page(url)
    products = get_products_links(soup_f_page)
    if len(links) == 0:
        return products

    for page_link in links:

        soup_n_page = get_soup (page_link)
        products_n = get_products_links(soup_n_page)
        products.extend(products_n)
    return products


data = get_all_data_products_in_category('https://mascotify.pe/gatos/accesorios-y-otros-gatos/?swoof=1&product_cat=transportadores-gatos&really_curr_tax=82-product_cat')
print(data)
