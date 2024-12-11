def format_item_price(price: int | float) -> str:
    if price < 100:
        return str(int(price)) + '$'
    return str(float(price)) + '$'
