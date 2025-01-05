import json

from ..utils import clean_text, clean_numbers, get_soup


def information_product(url, **kwargs) -> dict:
        soup = get_soup(url)

    # try:
        category_nav = soup.find("nav", id="breadcrumbs")
        if category_nav:
            categories = category_nav.find_all("a")
            categories = [cat.get_text() for cat in categories]
            menu = categories[1]
            category = " - ".join(categories[2:])
        else:
            menu, category = None, None

        h1 = soup.find("h1", class_="product-title")
        brand = (
            h1.find_next("div", class_="marca-product-page")
            .find_next("div")
            .get_text()
        )
        short_description = h1.find_next(
            "div", class_="product-short-description"
        ).get_text()
        long_description_divs = soup.find("div", class_="panel entry-content")

        last_price = h1.find_next("del")
        actual_price = h1.find_next("ins")

        price_min, price_max, qnts, prices = None, None, [], []
        prices_str, qnts_str = None, None

        if last_price:
            last_price = clean_numbers(last_price.get_text())

        if actual_price:
            actual_price = clean_numbers(actual_price.get_text())

        variation_data = soup.find("form", class_="variations_form")
        if variation_data:
            variation_json = variation_data.get("data-product_variations")
            variations = json.loads(variation_json)
            # return variations

            for variation in variations:
                qnt_i = ""
                var = variation["attributes"]
                keys_var_presentation = list(var.keys())
                for presentation in keys_var_presentation:
                     qnt_i = var.get(presentation)
                qnts.append(qnt_i)
                price = variation["display_price"]
                prices.append(price)
            price_min = min(prices)
            price_max = max(prices)

            prices_str = " - ".join(map(str, prices))
            qnts_str = " - ".join(qnts)

        return {
            "type": menu,
            "category": category,
            "brand": clean_text(brand),
            "product_name": clean_text(h1.get_text()),
            "actual_price": actual_price,
            "last_price": last_price,
            "price_min": price_min,
            "price_max": price_max,
            "range_prices": prices_str,
            "range_qnts": qnts_str,
            "s_description": clean_text(short_description),
            "l_description": clean_text(
                long_description_divs.get_text() if long_description_divs else ""
            ),
            "href": url,
        }
    # except Exception:
    #     pass