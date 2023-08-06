import asyncio

import pytest

from actorio._async_utils import TaskContainer


@pytest.fixture()
def queue(event_loop):
    return asyncio.Queue(loop=event_loop)


@pytest.fixture()
def reusable_task(event_loop, queue):
    return TaskContainer(coro_factory=queue.get, loop=event_loop)


@pytest.mark.asyncio
async def test_reusable_task_is_awaitable(queue, reusable_task):
    reusable_task.reschedule()
    await queue.put("a")
    assert "a" == await reusable_task.task


@pytest.mark.asyncio
async def test_reusable_task_is_no_longer_awaitable_after_rearm(queue, reusable_task):
    reusable_task.reschedule()
    await queue.put("a")
    assert "a" == await reusable_task.task

    reusable_task.reschedule()

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(reusable_task.task, timeout=0.01)


@pytest.mark.asyncio
async def test_reusable_task_only_rearm_if_necessary(queue, reusable_task):
    reusable_task.reschedule()
    task = reusable_task.task
    reusable_task.reschedule()
    assert task == reusable_task.task


@pytest.mark.asyncio
async def test_reusable_task_is_eq_to_inner_task(queue, reusable_task):
    reusable_task.reschedule()
    assert reusable_task == reusable_task.task


@pytest.mark.asyncio
async def test_reusable_task_is_eq_to_inner_task_other_side(queue, reusable_task):
    reusable_task.reschedule()
    assert reusable_task.task == reusable_task

@pytest.mark.asyncio
async def test_reusable_task_is_not_eq_to_other_object(reusable_task):
    assert not reusable_task == object()


@pytest.mark.asyncio
async def test_reusable_task_cancels_task_on_cm_exit(queue, reusable_task):
    async with reusable_task as rt:
        rt.reschedule()
        assert not rt.task.done()
        assert not rt.task.cancelled()
    assert rt.task.done()
    assert rt.task.cancelled()


@pytest.mark.asyncio
async def test_reusable_task_usable_in_asyncio_wait(queue, reusable_task):
    async with reusable_task as rt:
        rt.reschedule()
        done, pending = await asyncio.wait([queue.put("a"), rt.task], return_when=asyncio.ALL_COMPLETED, timeout=0.1)
        assert rt.task in done

