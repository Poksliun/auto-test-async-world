import asyncio

from playwright.async_api import Page, expect
from src_fe.pages import BasePage as SyncBasePage
from src_fe.async_pages import CartPage, BasePage

from src_fe.utils import format_item_price


class TestAsyncCart:

    # region Сценарий 1
    async def test_buy_item_async(
            self,
            page,
            aiodb_add_item
    ) -> None:
        # region Arrange
        add_event = aiodb_add_item(name='Name 1', price='100.00')
        # endregion
        # region Act
        page = SyncBasePage(page)
        page.authorize()
        await add_event
        cart_page = page.click_cart_button()
        cart_page.choose_item()
        cart_page.buy_items()
        # endregion
        # region Assert
        ...
        # endregion

    # endregion

    # region Сценарий 2
    async def test_get_items_async(
            self,
            page: Page,
            check,
            aiodb_add_item
    ) -> None:
        # region Arrange
        add_events = [aiodb_add_item(name='Name 1', price='100.00'),
                      aiodb_add_item(name='Name 2', price='200.00'),
                      aiodb_add_item(name='Name 3', price='500.00'),
                      aiodb_add_item(name='Name 4', price='5.00')]
        # endregion
        # region Act
        base_page = BasePage(page)
        await base_page.open()
        [await i_task for i_task in add_events]
        cart_page = await base_page.click_cart_button()
        # endregion
        # region Assert
        expects = [
            asyncio.create_task(expect(cart_page.page.locator(f'#items[num={i}]')).to_be_visible())
            for i in range(1, 5)
        ]
        for exp in expects:
            with check:
                await exp
        # endregion

    # endregion

    # region Сценарий 3
    async def test_correct_item_price_async(
            self,
            page: Page,
            aiodb_add_item
    ):
        # region Arrange
        await aiodb_add_item(name='Name 1', price='100.00')
        # endregion
        # region Act
        cart_page = CartPage(page)
        await cart_page.route_items()
        await cart_page.open()
        items = await cart_page.items
        price = format_item_price(items[0].price)
        # endregion
        # region Assert
        await expect(cart_page.page.locator('.items[num=1]')).to_have_value(price)
        # endregion

    # endregion
