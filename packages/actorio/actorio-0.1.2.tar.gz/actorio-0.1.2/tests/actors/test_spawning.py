import asyncio

import pytest

from actorio import Actor


@pytest.mark.asyncio
async def test_actor_starts_child_actor_on_register():
    a = Actor()
    async with a:
        child = Actor()
        await a.register_child(child)
        assert child.started, "Child should be started on register"
        assert child.running, "Child should be running on register"
    assert not child.running, "Child should have been stopped when parent actor stopped"


@pytest.mark.asyncio
async def test_parent_actor_is_properly_registered_on_child():
    a = Actor()
    async with a:
        child = Actor()
        await a.register_child(child)
        assert child in a.children


@pytest.fixture
def test_child_class():
    class TestChild(Actor):


        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.called_stop = False

        async def stop(self):
            self.called_stop = True
            return await super().stop()

        async def _mainloop(self):
            await asyncio.sleep(0)

    return TestChild


@pytest.fixture
def test_parent_class(test_child_class):
    class TestParent(Actor):

        def __init__(self, *args, output_queue: asyncio.Queue, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.output_queue = output_queue

        async def handle_child_stopped(self, child: Actor, task: asyncio.Task):
            await self.output_queue.put(child)

        async def start(self):
            child = test_child_class()
            await self.register_child(child)
            return await super().start()

    return TestParent


@pytest.mark.asyncio
async def test_parent_actor_is_notified_when_a_child_stops(output_queue, test_parent_class):
    actor = test_parent_class(output_queue=output_queue)
    async with actor:
        await asyncio.wait_for(output_queue.get(), timeout=0.5)


@pytest.mark.asyncio
async def test_parent_actor_calls_child_stop_method(output_queue, test_parent_class):
    actor = test_parent_class(output_queue=output_queue)
    async with actor:
        child = list(actor.children)[0]
        await asyncio.wait_for(output_queue.get(), timeout=0.5)
        assert child.called_stop, "child stop method was not called"
