import requests
from requests import session
from bs4 import BeautifulSoup as BSP
from rich import print
from urllib import parse
import time
from .utils import save_array

URL_SUPERPET = "https://www.superpet.pe/"
superpet_parse = parse.urlsplit(URL_SUPERPET)


main_content = requests.get(URL_SUPERPET)

soup = BSP(main_content.content, "html.parser")
mega_menu = soup.find("div", id="mega-menu")


if mega_menu:
    divs = [div for div in mega_menu.find_all("div", class_="mega-title")]
    hrefs = [
        {"text": div.get_text(), "href": div.find("a", href=True).get("href", "")}
        for div in divs
    ]
    # hrefs = [a['href'] for a in mega_menu.find_all('a', href=True)]
else:
    print("No se encontró el div con id 'mega-menu'.")

# print(texts)

relevant_menu = []

for menu_href in hrefs:
    _url_split = parse.urlsplit(menu_href.get("href"))
    _path = _url_split.path.split("/")
    if _url_split.netloc == superpet_parse.netloc and len(_path) > 2:
        if _path[2] != "":
            menu_href["tipo"] = _path[1]
            relevant_menu.append(menu_href)


def get_content(url):
    relevant_page = requests.get(url)
    soup_page = BSP(relevant_page.content, "html.parser")
    return soup_page


def get_products_id(soup_page):
    productos = soup_page.find_all("div", class_="product")
    resultados = [
        str(producto["data-pid"]) for producto in productos if "data-pid" in producto.attrs
    ]
    return resultados


def find_more_button(soup_page):
    more_button = soup_page.find(
        "button", class_="btn btn-secondary-low col-12 col-sm-4"
    )
    if more_button is None:
        return None
    data_url = more_button.get("data-url", "")
    query_params = parse.parse_qs(parse.urlparse(data_url).query)
    cgid = query_params.get("cgid", [None])[0]
    return cgid


def fetch_results(cgid, start=12, sz=1000):
    # Construir la URL con los parámetros
    base_url = "https://www.superpet.pe/on/demandware.store/Sites-SuperPet-Site/es_PE/Search-UpdateGrid"
    params = {"cgid": cgid, "start": start, "sz": sz}

    response = requests.get(base_url, params=params)

    try:
        soup_n = BSP(response.content, "html.parser")
        rest = get_products_id(soup_n)
        return rest, soup_n
    except:
        return [], None

a = time.time()

def get_all_products_by_relevance(url):

    # url = relevant_menu[1].get("href")
    # print(url)
    s = get_content(url)
    products = get_products_id(s)
    cgdid = find_more_button(s)


    if cgdid is not None:
        print(cgdid)
        more_products = fetch_results(cgdid)
        products +=  more_products[0]
        # print(len(more_products[0]))
        # print(more_products)
    total_time = time.time() - a
    print(total_time, len(products))
    # print(len(all_products))
    time.sleep(2)
    return products




for menu in relevant_menu:
    url = menu.get('href')
    menu['products_id'] = get_all_products_by_relevance(url)

save_array(relevant_menu, 'superpet')