from ..utils import get_soup, clean_numbers

def information_product(url, category=None, type=None):
    soup = get_soup(url)

    information = soup.find('div', class_='summary')
    brand = information.find('div')
    product_name = information.find('h1')

    description = product_name.find_next('div')

    prices = soup.find('p', class_='price')

    actual_price =  clean_numbers(prices.get_text())
    last_price = None

    if prices.find('ins'):
        actual_price = clean_numbers(prices.find('ins').get_text())
        last_price = clean_numbers(prices.find('del').get_text())
    return dict(
        type=type,
        category=category,
        brand = brand.get_text(),
        product_name = product_name.get_text(),
        s_description = description.get_text(),
        actual_price = actual_price,
        last_price = last_price,
        href = url
    )

# print(actual_price)

