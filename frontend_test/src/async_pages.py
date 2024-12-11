import asyncio

from playwright.async_api import Page, Route, APIResponse


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page: Page = page

    async def open(self, path: str = '') -> 'BasePage':
        await self.page.goto(path)
        return self

    async def authorize(self) -> 'BasePage':
        ...
        return self

    async def click_cart_button(self) -> 'CartPage':
        await self.page.click('#cart_button')
        return CartPage(self.page)


class CartPage(BasePage):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.items: asyncio.Future[list[dict] | dict | None] = asyncio.Future()

    async def route_items(self) -> None:
        async def route_(route: Route) -> None:
            resp = await route.fetch()
            self.items.set_result(await resp.json())
            await route.fulfill()

        await self.page.route('url', route_)

    async def choose_item(self, index: int = 0) -> 'CartPage':
        items = await self.page.locator('#item').all()
        await items[index].click()
        return self

    async def buy_items(self) -> 'CartPage':
        ...
        return self
























