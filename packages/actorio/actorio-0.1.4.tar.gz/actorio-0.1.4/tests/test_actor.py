import asyncio
from collections import deque

import pytest

from actorio import Actor, EndMainLoop
from actorio import wait_for


@pytest.fixture()
def simple_custom_actor_class():
    class CustomActor(Actor):
        def __init__(self, *args, output_queue: asyncio.Queue, **kwargs):
            super().__init__(*args, **kwargs)
            self.output_queue = output_queue
            self._counter_1 = 0
            self._counter_2 = 0

        async def start(self):
            self.register_input_task(self.test_task_1, coro_to_run=self.test_coro_1)
            self.register_input_task(self.test_task_2, coro_to_run=self.test_coro_2)
            self.register_input_task(self.test_task_3, coro_to_run=self.nop)
            return await super().start()

        async def test_task_3(self):
            f = asyncio.Future()
            await f

        async def nop(self, task: asyncio.Task):
            pass

        async def test_task_1(self):
            await asyncio.sleep(0.001)

        async def test_coro_1(self, task: asyncio.Task):
            await self.output_queue.put((1, self._counter_1))
            self._counter_1 += 1

        async def test_task_2(self):
            await asyncio.sleep(0.001)

        async def test_coro_2(self, task: asyncio.Task):
            await self.output_queue.put((2, self._counter_2))
            self._counter_2 += 1

    return CustomActor


@pytest.mark.asyncio
async def test_multiple_tasks_are_collected(output_queue, simple_custom_actor_class):
    actor = simple_custom_actor_class(output_queue=output_queue)
    async with actor:
        await asyncio.sleep(0.05)
    output = deque()

    while not output_queue.empty():
        output.append(output_queue.get_nowait())

    a_members = filter(lambda x: x[0] == 1, output)
    b_members = filter(lambda x: x[0] == 2, output)

    for (_,a),(_,b) in zip(a_members, b_members):
        assert a == b



@pytest.mark.asyncio
async def test_all_input_tasks_are_cancelled(output_queue, simple_custom_actor_class):
    actor = simple_custom_actor_class(output_queue=output_queue)
    async with actor:
        await asyncio.sleep(0.05)

    for task in actor.input_tasks:
        t = task._task
        if t is not None:
            assert t.done() or t.cancelled(), "all input tasks should either be done or cancelled"


@pytest.fixture()
def long_coro_actor_class():
    class CustomActor(Actor):
        def __init__(self, *args, output_queue: asyncio.Queue, future_to_wait: asyncio.Future, **kwargs):
            super().__init__(*args, **kwargs)
            self.future_to_wait = future_to_wait
            self.output_queue = output_queue

        async def start(self):
            self.register_input_task(self.test_task, coro_to_run=self.test_coro)
            return await super().start()

        async def test_task(self):
            pass

        async def test_coro(self, task: asyncio.Task):
            await self.future_to_wait
            await self.output_queue.put(None)

    return CustomActor


@pytest.mark.asyncio
async def test_actor_blocking_coro(long_coro_actor_class, output_queue, loop):
    f = loop.create_future()
    actor = long_coro_actor_class(output_queue=output_queue, future_to_wait=f)
    async with actor:
        with pytest.raises(asyncio.TimeoutError, message="Queue should not be fed until we set the future"):
            await asyncio.wait_for(output_queue.get(), timeout=0.1)
        f.set_result(None)
        await asyncio.wait_for(output_queue.get(), timeout=0.1)


@pytest.mark.asyncio
async def test_actor_blocking_coro_is_not_cancelled_on_aexit(long_coro_actor_class, output_queue, loop):
    f = loop.create_future()
    actor = long_coro_actor_class(output_queue=output_queue, future_to_wait=f)
    await actor.start()
    with pytest.raises(asyncio.TimeoutError, message="Queue should not be fed until we set the future"):
        await asyncio.wait_for(output_queue.get(), timeout=0.1)
    # noinspection PyAsyncCall
    loop.create_task(actor.stop())
    with pytest.raises(asyncio.TimeoutError, message="Actor main loop should not be able to stop until its latest task is done"):
        await wait_for(actor, timeout=0.1, shield=True)
    f.set_result(None)
    await asyncio.wait_for(actor, timeout=1)


@pytest.fixture()
def self_stoping_actor_class():
    class CustomActor(Actor):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        async def start(self):
            self.register_input_task(self.test_task, coro_to_run=self.test_coro)
            return await super().start()

        async def test_task(self):
            pass

        async def test_coro(self, task: asyncio.Task):
            raise EndMainLoop()

    return CustomActor


@pytest.mark.asyncio
async def test_mainloop_stops_properly_on_endmainloop(self_stoping_actor_class):
    a = self_stoping_actor_class()
    async with a:
        await asyncio.wait_for(a, timeout=0.5)
