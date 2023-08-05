[![pipeline status](https://gitlab.com/python-actorio/actorio/badges/master/pipeline.svg)](https://gitlab.com/python-actorio/actorio/commits/master)
[![coverage report](https://gitlab.com/python-actorio/actorio/badges/master/coverage.svg)](https://gitlab.com/python-actorio/actorio/commits/master)
[![PyPI version](https://badge.fury.io/py/actorio.svg)](https://badge.fury.io/py/actorio)
# Actorio - a simple actor framework for asyncio

Actorio is a Python asyncio implementation of the [actor model](https://en.wikipedia.org/wiki/Actor_model).

There already are Python actor model implementation such as
[Thespian](https://github.com/kquick/Thespian) or [Pykka](https://github.com/jodal/pykka)
but they're currently lacking asyncio support.

The main goal of the Actor model is to cleanly define the critical section 
without having to deal with lock or any other synchronization mechanism.

It also helps with the [Single responsibility principle](https://en.wikipedia.org/wiki/Single_responsibility_principle),
each `Actor` class should deal with one part of the fonctionnal requirements of the application and its API can be properly defined
(ie, what kind of message does this actor accept and what kind of message does it produce), hence making actor testing easier,
since you don't have to mock the surrounding systems and just check if the message sequence if correct. 


*Current API is crude and provisional and is likely to change as syntax and concepts evolve.*


### Rules of the actor model
- An actor is an execution unit that executes concurrently with other actors.

- An actor does not share state with anybody else, but it can have its own state.

- An actor can only communicate with other actors by sending and receiving messages. It can only send messages to actors whose address it has.

- When an actor receives a message it may take actions like:

  - altering its own state, e.g. so that it can react differently to a future message
  - sending messages to other actors
  - starting new actors

    None of the actions are required, and they may be applied in any order.

- An actor only processes one message at a time. In other words, a single actor does not give you any concurrency, and it does not need to use locks internally to protect its own state.

### Hello World
A Hello world example:

Let's start with the typical example of Hello World. In this case, we'll create an Actor, send it a message, wait for a response message, and print that response: 

```python
from actorio import Actor, Message, DataMessage, ask
import asyncio
class Greeter(Actor):
    # Here we override the handle_message method to send a `DataMessage` with the data "Hello World!".
    async def handle_message(self, message: Message):
        await message.sender.tell(DataMessage(data="Hello World!", sender=self))
        
        
async def main():
    # Let's create an instance of a Greeter actor and start it. 
    async with Greeter() as greeter:
        # Then we'll just send it an empty message and wait for a response
        reply : DataMessage = await ask(greeter, Message())
    print(reply.data)
        
asyncio.get_event_loop().run_until_complete(main())
```

### Actor spawning actors
Actor instances can spawn other actors during their execution. be it at startup, in the `mainloop_setup` async method or as a reaction to an event in any handler.

The actor should first be instanciated (with an `__init__` call) then be registered on its parent with a `register_child` async call.

Whenever a child dies, the parent `handle_child_stopped` async method is called with the child actor object and the `asyncio.task` object for its execution loop. This way, the parent can take any action required.

For example, if we had to handle blocking operations. we could do something like:
```python
import random
import asyncio
from actorio import Actor, Message, DataMessage, EndMainLoop, Reference
async def blocking_operation():
    #for the sake of this example, the blocking operation is a sleep
    sleep_time = random.randint(0,10)
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
            
async def main():
    # We create an inbox for us, this is not an actor,
    # just somewhere actors can send messages
    me = Reference()
    async with Manager() as manager:
        # Then we start 10 long computations
        for _ in range(10): await manager.tell(RequestMessage(sender=me))
        # Then we'll listen to our inbox
        # to get the responses as they come by
        for _ in range(10):
            message = await me.inbox.get()
            print("Got a response with result {}".format(message.data))
        
asyncio.get_event_loop().run_until_complete(main())

```
### Handling external blocking events
Using message is great, but, most of the time, we also need to use other APIs that don't provide a message-based interface.

It's possible to register external blocking event and handler for those with the `register_input_task` method.
This methods takes a factory function for a coroutine and an async function to handle the task result.

**The handler will not be called if the Actor is currently busy processing anything else
(like a message or any other task), this way, there is no concurrency issue
and each handler is called with a clean actor state**

*For now, the order in which those events will be handled is not necessarily the order in which they happened* 

For example, to use an `aiohttp` websocket :
```python
import aiohttp
from aiohttp import web
from actorio import Actor, EndMainLoop
import asyncio

class Client(Actor):
    def __init__(self, websocket: web.WebSocketResponse):
        self.websocket = websocket
        super().__init__()
    
    # Here we define an input task handler,
    # It will be called each time its registered event happens.
    # The resulting `asyncio.Task` object will be passed as argument,
    # this way, the handler can deal with any exception raised during event collection 
    async def handle_websocket_event(self, task: asyncio.Task):
        try:
            msg = task.result()
        except Exception as e:
            # In case of any exception, we just stop the Actor
            self.logger.exception(e)
            raise EndMainLoop()
        if msg.type == aiohttp.WSMsgType.TEXT:
            # if we receive text, we just send it back
            # We could also just send a message to our inbox
            await self.websocket.send_str(msg.data)
        else:
            # any other request just stops the Actor
            raise EndMainLoop()
            
    async def mainloop_setup(self):
        self.register_input_task(self.websocket.receive, self.handle_websocket_event)
        await super().mainloop_setup()
    


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    client_actor = Client(websocket=ws)

    async with client_actor:
        # We until the client's mainloop ends
        await client_actor

    return ws
    
app = web.Application()
app.add_routes([web.get('/', websocket_handler)])
web.run_app(app)
```

You can then connect to the websocket and send it some messages, it will act as an echo server.