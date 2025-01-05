from ..utils import get_soup, clean_numbers

def information_product(url, category=None, type=None):
    try:
        soup = get_soup(url)

        product_name = soup.find('h1')
        brand = product_name.find_next("a")

        description = product_name.find_next('section', class_='bs-product-description')
        actual_price = product_name.find_next('span', class_='h2')

        info_product = dict(
            type=type,
            category=category,
            brand = brand.find('img').get('title', None),
            product_name = product_name.get_text(),
            actual_price = clean_numbers(actual_price.get_text()),
            description = description.get_text(),
        )

        return info_product
    except:
        print(url)
        pass