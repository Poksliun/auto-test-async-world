from playwright.sync_api import Page, expect
from src_fe.pages import BasePage, CartPage
from src_fe.utils import format_item_price


class TestCart:

    # region Сценарий 1
    def test_buy_item(
            self,
            page,
            db_add_item
    ) -> None:
        # region Arrange
        db_add_item(name='Name 1', price='100$')
        # endregion
        # region Act
        page = BasePage(page)
        page.authorize()
        cart_page = page.click_cart_button()
        cart_page.choose_item()
        cart_page.buy_items()
        # endregion
        # region Assert
        ...
        # endregion
    # endregion

    # region Сценарий 2
    def test_get_items(
            self,
            page: Page,
            check,
            db_add_item
    ):
        # region Arrange
        db_add_item(name='Name 1', price='100.00')
        db_add_item(name='Name 2', price='200.00')
        db_add_item(name='Name 3', price='500.00')
        db_add_item(name='Name 4', price='5.00')
        # endregion
        # region Act
        cart_page = CartPage()
        cart_page.open()
        # endregion
        # region Assert
        with check:
            expect(page.locator('.items[num=1]')).to_be_visible()
        with check:
            expect(page.locator('.items[num=2]')).to_be_visible()
        with check:
            expect(page.locator('.items[num=3]')).to_be_visible()
        with check:
            expect(page.locator('.items[num=4]')).to_be_visible()
        # endregion
    # endregion

    # region Сценарий 3
    def test_correct_item_name(
            self,
            page: Page,
            db_add_item
    ) -> None:
        # region Arrange
        db_add_item(name='Name 1', price='100$')
        # endregion
        # region Act
        cart_page = CartPage()
        cart_page.open()
        price = format_item_price(cart_page.items[0].price)
        # endregion
        # region Assert
        expect(page.locator('.items[num=1]')).to_have_value(price)
        # endregion
    # endregion
