import asyncio

import pytest

from actorio import Actor
from actorio._abc import ActorABC


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


class BadActor(Actor):
    async def _mainloop(self):
        await asyncio.sleep(0)
        raise RuntimeError("foo")


class Application(Actor):
    async def mainloop_setup(self):
        self.actor1 = Actor()
        self.actor2 = Actor()
        self.bad_actor = BadActor()

        await self.register_child(self.actor1)
        await self.register_child(self.actor2)
        await self.register_child(self.bad_actor)

        return await super().mainloop_setup()


@pytest.mark.asyncio
async def test_all_actors_should_be_stopped_if_one_fails():
    a = Application()
    with pytest.raises(RuntimeError, match="foo"):
        await asyncio.wait_for(a.run_until_stopped(), timeout=1)
    assert a.actor1.stopped
    assert a.actor2.stopped
    assert a.bad_actor.stopped
