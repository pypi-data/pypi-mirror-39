import pytest

import actorio
from actorio import Message, DataMessage, Actor, EndMainLoop, ActorReference
from actorio._abc import ReferenceABC


def test_actor_reference_is_a_subclass_of_reference_abc():
    assert issubclass(ActorReference, ReferenceABC)


@pytest.mark.asyncio
async def test_ask_function():
    from actorio import Actor, Message, DataMessage
    class Greeter(Actor):
        async def handle_message(self, message: Message):
            await message.sender.tell(DataMessage(data="Hello World!", sender=self.reference))

    async with Greeter() as greeter:
        reply: DataMessage = await actorio.wait_for(actorio.ask(greeter, Message()), timeout=0.5)
    assert reply.data == "Hello World!"


@pytest.mark.asyncio
async def test_reference_ask(test_reference):
    from actorio import Actor, Message, DataMessage
    class Greeter(Actor):
        async def handle_message(self, message: Message):
            await message.reply(DataMessage(data="Hello World!", sender=self.reference))

    async with Greeter() as greeter:
        reply: DataMessage = await actorio.wait_for(greeter.ask(Message(sender=test_reference)), timeout=0.5)
    assert reply.data == "Hello World!"


def test_reference_identifier_is_the_same_as_its_actor():
    a = Actor()
    assert a.reference.identifier == a.identifier


@pytest.mark.asyncio
async def test_reference_tell(test_reference):
    import random
    import asyncio
    async def blocking_operation():
        # for the sake of this example, the blocking operation is a sleep
        sleep_time = random.randint(0, 10) / 10
        await asyncio.sleep(sleep_time)
        return sleep_time

    class RequestMessage(Message):
        """
        A request to do some computation or blocking call
        """

    class ResponseMessage(DataMessage):
        """
        The result of a computation
        """

    class Worker(Actor):
        # Here we override the handle_message method to send a `ResponseMessage`
        # with the result of the blocking operation as its data.
        async def handle_message(self, message: Message):
            sleep_time = await blocking_operation()
            await message.sender.tell(ResponseMessage(data=sleep_time, sender=self))
            # This actor only deals with one message then stops,
            # raising an EndMainLoop exeception here will properly stop the actor
            raise EndMainLoop()

    class Manager(Actor):
        async def handle_message(self, message: Message):
            if isinstance(message, RequestMessage):
                # We spawn and register the new child, we get its reference back
                child = await self.register_child(Worker())
                # We just transfer the message to the child, that way,
                # we won't have to process its response
                await child.tell(message)

    async with Manager() as manager:
        # Then we start 10 long computations
        for _ in range(10): await manager.tell(RequestMessage(sender=test_reference))
        # Then we'll listen to our inbox
        # to get the responses as they come by
        last_value = 0
        for _ in range(10):
            message: DataMessage = await asyncio.wait_for(test_reference.inbox.get(), timeout=1)
            assert message.data >= last_value
            last_value = message.data
