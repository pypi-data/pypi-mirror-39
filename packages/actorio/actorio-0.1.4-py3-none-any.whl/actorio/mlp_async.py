from asyncio import Task, get_event_loop, AbstractEventLoop, CancelledError


def wait_for(fut, timeout, *, loop=None, shield=False):
    import asyncio
    if shield:
        fut = asyncio.shield(fut)
    return asyncio.wait_for(fut, timeout=timeout, loop=loop)


class ReusableTask:
    __slots__ = ["_coro_factory", "_task", '_loop']

    def __init__(self, coro_factory, *, loop: AbstractEventLoop = None):
        self._loop = loop or get_event_loop()
        self._coro_factory = coro_factory
        self._task: Task = None

    @property
    def task(self):
        if not self._task:
            self.arm()
        return self._task

    def arm(self):
        if self._task and not self.task.done():
            return
        self._arm()

    def _arm(self):
        self._task = self._loop.create_task(self._coro_factory())

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.task == other
        raise NotImplemented()

    def __hash__(self):
        return hash(self._coro_factory)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except CancelledError:
                pass
