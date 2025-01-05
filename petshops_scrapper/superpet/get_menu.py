from ..utils import get_soup, save_array
from urllib import parse

URL_SUPERPET = "https://www.superpet.pe/"
superpet_parse = parse.urlsplit(URL_SUPERPET)


# main_content = requests.get(URL_SUPERPET)
class SuperPetMenu:
    def __init__(self, url = URL_SUPERPET):
        soup = get_soup(url)
        self.soup = soup
        data = self.find_menu()
        self.data = data
        save_array(data, 'SuperPet', "info/menu")
    def find_menu(self):
        soup = self.soup

        mega_menu = soup.find("div", id="mega-menu")


        if mega_menu:
            divs = [div for div in mega_menu.find_all("div", class_="mega-title")]
            hrefs = [
                {"category": div.get_text(), "href": div.find("a", href=True).get("href", "")}
                for div in divs
            ]
        else:
            print("No se encontró el div con id 'mega-menu'.")



        relevant_menu = []

        for menu_href in hrefs:
            _url_split = parse.urlsplit(menu_href.get("href"))
            _path = _url_split.path.split("/")
            if _url_split.netloc == superpet_parse.netloc and len(_path) > 2:
                if _path[2] != "":
                    menu_href["type"] = _path[1]
                    relevant_menu.append(menu_href)
        return relevant_menu
