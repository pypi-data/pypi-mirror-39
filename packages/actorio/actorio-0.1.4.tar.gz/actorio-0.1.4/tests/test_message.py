import asyncio

import pytest

from actorio import Actor, UnhandledMessage
from actorio import Message, ActorioException
from actorio.messaging import MessageQueue


@pytest.mark.asyncio
async def test_message_queue_base_methods(test_reference):
    m = Message(sender=test_reference)
    q = MessageQueue()
    q.put_nowait(m)
    assert m is q.get_nowait()

    await q.put(m)
    assert m is await q.get()


@pytest.mark.asyncio
async def test_message_input_actor_raises_exception_on_unknown_message(test_reference):
    actor = Actor()
    with pytest.raises(UnhandledMessage):
        async with actor:
            await actor.inbox.put(Message(sender=test_reference))
            await asyncio.sleep(.05)


@pytest.mark.asyncio
async def test_message_converts_actor_to_a_reference(test_reference):
    actor = Actor()
    m = Message(sender=actor)
    assert m.sender is actor.reference


@pytest.mark.asyncio
async def test_message_cannot_be_sent_without_a_sender(test_reference):
    m = Message()
    q = MessageQueue()
    with pytest.raises(ActorioException):
        await q.put(m)

    with pytest.raises(ActorioException):
        q.put_nowait(m)
