import playwright.sync_api
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page: Page = page

    def open(self, path: str = '') -> 'BasePage':
        self.page.goto(path)
        return self

    def authorize(self) -> 'BasePage':
        return self

    def click_cart_button(self) -> 'CartPage':
        with self.page.expect_response('...') as r:
            self.page.locator('#cart').click()
        cp: CartPage = CartPage(self.page)
        cp.items = r.value.json()
        return cp


class CartPage(BasePage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.items: dict | None = None

    def open(self, path: str = '') -> 'CartPage':
        with self.page.expect_response('...') as r:
            super().open(path)
        self.items = r.value.json()
        return self

    def choose_item(self, index: int = 0) -> 'CartPage':
        self.page.locator('#item').all()[index].click()
        return self

    def buy_items(self) -> 'CartPage':
        ...
        return self
