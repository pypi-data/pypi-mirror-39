import asyncio

import pytest

from actorio import Message
from actorio import Actor, UnhandledMessage


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