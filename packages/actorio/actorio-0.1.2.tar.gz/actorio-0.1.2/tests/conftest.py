import asyncio

import pytest

import actorio


@pytest.fixture(autouse=True)
async def loop(event_loop) -> asyncio.AbstractEventLoop:
    try:
        yield event_loop
    finally:
        await asyncio.sleep(0)


@pytest.fixture()
def output_queue(loop):
    return asyncio.Queue(loop=loop)


@pytest.fixture()
async def test_reference(loop) -> actorio.Reference:
    return actorio.Reference()
