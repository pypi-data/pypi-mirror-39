import asyncio
import logging
from typing import Dict, Callable, Set, Optional

from ._abc import ActorABC, IdentifierABC, MessageABC, ActorReferenceABC
from ._async_utils import TaskContainer
from .errors import NoLongerScheduled, EndMainLoop, UnhandledMessage
from .interfaces import Identified
from .messaging import MessageQueue, Message
from .reference import ActorReference


class Actor(Identified, ActorABC):

    def __init__(self, *args, identifier: IdentifierABC = None, **kwargs) -> None:
        super().__init__(*args, identifier=identifier, **kwargs)
        self.mainloop_task: Optional[asyncio.Task] = None
        self.input_tasks: Dict[TaskContainer, Callable] = dict()
        self.children: Set[ActorABC] = set()
        self.inbox = MessageQueue()
        self.logger = logging.getLogger(self.identifier.as_string())
        self.reference = ActorReference(actor_inbox=self.inbox, actor_id=self.identifier)

    @property
    def started(self) -> bool:
        return self.mainloop_task is not None

    @property
    def stopped(self) -> bool:
        return self.started and not self.running

    @property
    def running(self) -> bool:
        return self.mainloop_task is not None and not self.mainloop_task.done()

    async def wait(self):
        await self.mainloop_task

    async def register_child(self, child: ActorABC) -> ActorReferenceABC:
        # FIXME: this is ugly, must find a better way
        self.register_input_task(child.wait, lambda task: self._handle_child_stopped(child, task), count=1)
        await child.start()
        self.children.add(child)
        return child.reference

    async def _handle_child_stopped(self, child: ActorABC, task: asyncio.Task):
        """Remove the child that just stopped from our supervision and call the `handle_child_stopped` async method
           This method should not be overridden, instead, override `handle_child_stopped` instead
        """
        self.children.remove(child)
        return await self.handle_child_stopped(child, task)

    async def handle_child_stopped(self, child: ActorABC, task: asyncio.Task):
        """Handle the death of a child, by default, this method only logs the fact that the child died
           then re-raise so that the exception can reach the caller (it's much easier to find bug if the exception is not hidden)

           just catch the exception when calling super() to handle it in your actor implementation
        """
        if task.exception():
            self.logger.error("Child {cid} died".format(cid=child.identifier))
            await child.wait()
        else:
            self.logger.info("Child {cid} stopped".format(cid=child.identifier))

    @property
    def _loop(self) -> asyncio.AbstractEventLoop:
        return asyncio.get_event_loop()

    async def _mainloop(self):
        await self.mainloop_setup()
        try:
            while True:
                await self._mainloop_iteration()
        except EndMainLoop:
            pass
        except Exception as e:
            self.logger.exception(e)
            raise
        finally:
            await self.mainloop_teardown()

    async def _wait_for_all_tasks(self):
        return await asyncio.wait([rt.task for rt in self.input_tasks], return_when=asyncio.FIRST_COMPLETED)

    async def _mainloop_iteration(self):
        # TODO: there should be a way to exit this using an asyncgenerator instead of raising an exception
        try:
            finished_tasks, _ = await self._wait_for_all_tasks()
        except asyncio.CancelledError:
            raise EndMainLoop()

        for task_container, coro_to_run in [(rt, coro) for rt, coro in self.input_tasks.items() if rt.task in finished_tasks]:
            task = self._loop.create_task(coro_to_run(task_container.task))
            try:
                await asyncio.shield(task)
                try:
                    task_container.reschedule()
                except NoLongerScheduled:
                    self.input_tasks.pop(task_container)
            except asyncio.CancelledError:
                await task
                raise EndMainLoop()

    async def mainloop_setup(self):
        self.register_input_task(self.inbox.get, self._handle_message)

    async def mainloop_teardown(self):
        for rt in self.input_tasks:
            rt.task.cancel()

        if self.children:
            await asyncio.wait([child.stop() for child in self.children], return_when=asyncio.ALL_COMPLETED)

    def register_input_task(self, input_task_factory: Callable, coro_to_run: Callable, *, count: int = None):
        self.input_tasks[TaskContainer(input_task_factory, count=count)] = coro_to_run

    async def _handle_message(self, task: asyncio.Task):
        message: Message = task.result()
        return await self.handle_message(message)

    async def handle_message(self, message: MessageABC):
        raise UnhandledMessage(message)

    async def start(self):
        self.mainloop_task = self._loop.create_task(self._mainloop())
        # TODO: find a better way to let the event loop create the task
        #       or confirm this one is right
        await asyncio.sleep(0)

    async def stop(self):
        self.mainloop_task.cancel()
        await self.wait()
