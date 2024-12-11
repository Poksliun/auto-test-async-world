import asyncio
import sqlite3
from typing import Callable, Any, Awaitable, Coroutine

import aiosqlite
import pytest


@pytest.fixture(scope='session')
def connection() -> sqlite3.Connection:
    # todo: move
    with sqlite3.connect('') as conn:
        yield conn


@pytest.fixture(scope='session')
async def aio_connection() -> Awaitable[aiosqlite.Connection]:
    # todo: move
    with aiosqlite.connect('') as conn:
        yield conn


@pytest.fixture
def db_add_item(connection: sqlite3.Connection) -> Callable[..., None]:
    # todo: move
    def func_(data: dict[str, Any] | None = None, **kwargs) -> None:
        connection.cursor().execute('insert into ...', data if data else kwargs)

    return func_


@pytest.fixture
def aiodb_add_item(
        aio_connection: aiosqlite.Connection
) -> Callable[..., Coroutine[..., ..., Awaitable]]:
    # todo: move
    async def func_(data=None, **kwargs) -> Awaitable[None]:
        cursor = await aio_connection.cursor()
        return asyncio.create_task(cursor.execute('insert into ...', data if data else kwargs))

    return func_
