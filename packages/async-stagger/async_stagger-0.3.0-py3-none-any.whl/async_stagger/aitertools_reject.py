import asyncio
import collections.abc
import itertools
from typing import (
    AsyncIterable, AsyncIterator, Awaitable, Iterable, TypeVar,
    Optional)

from .aitertools import aiter, anext


_sentinel = object()
T = TypeVar('T')


class _OneOffPreloader:
    """Kickstart an async iterator."""

    def __init__(
            self,
            aiterable: AsyncIterable,
            *,
            loop: asyncio.AbstractEventLoop = None,
    ):
        self._aiterator = aiter(aiterable)
        self._loop = loop or asyncio.get_event_loop()
        self._preload_task = self._loop.create_task(anext(self._aiterator))

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._preload_task is not None:
            preload_task = self._preload_task
            self._preload_task = None
            return await preload_task
        return await anext(self._aiterator)

    def __repr__(self):
        return (f'<{self.__class__.__name__} wrapping {self._aiterator!r}, '
                f'preload_task={self._preload_task}>')


class _HandoffPreloader:
    """Preload and cache one item from an async iterable."""

    def __init__(
            self,
            aiterable: AsyncIterable,
            *,
            loop: asyncio.AbstractEventLoop = None
    ):
        self._aiterable = aiterable
        self._loop = loop or asyncio.get_event_loop()

        self._put_done = asyncio.Event(loop=self._loop)
        self._get_done = asyncio.Event(loop=self._loop)
        self._handover = None
        self._get_done.set()
        self._exhausted = False
        self._preloader_task = self._loop.create_task(self.preloader())

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._exhausted:
            raise StopAsyncIteration
        await self._put_done.wait()
        item = self._handover
        self._put_done.clear()
        self._get_done.set()
        # XXX

    async def preloader(self):
        try:
            async for item in self._aiterable:
                await self._get_done.wait()
                self._handover = item
                self._get_done.clear()
                self._put_done.set()
        finally:
            await self._get_done.wait()
            self._handover = _sentinel
            self._get_done.clear()
            self._put_done.set()


async def preload(
        aiterable: AsyncIterable[T],
        n_preload: Optional[int] = 0,
        *,
        loop: asyncio.AbstractEventLoop = None,
) -> AsyncIterator[T]:
    """Iterate through an async iterable early and cache results.

    Take an async iterable and starts to iterate it immediately, caching the
    results, so that when the output iterator is iterated the results
    may be available immediately.

    Args:
        aiterable: the input async iterable.

        n_preload: number of items to cache. If ``0`` or negative, cache
            an unlimited number of items.
    """
    if not isinstance(n_preload, int):
        raise TypeError(
            f'integer argument expected, got {type(n_preload).__name__}')
    loop = loop or asyncio.get_event_loop()

    if n_preload == 1:
        put_done = asyncio.Event()
        get_done = asyncio.Event()
        get_done.set()
        handover = None

        async def preloader():
            nonlocal handover
            try:
                async for item in aiterable:
                    await get_done.wait()
                    handover = item
                    get_done.clear()
                    put_done.set()
            finally:
                await get_done.wait()
                handover = _sentinel
                get_done.clear()
                put_done.set()

        preloader_task = loop.create_task(preloader())

        try:
            while True:
                await put_done.wait()
                item = handover
                put_done.clear()
                get_done.set()
                if item is not _sentinel:
                    yield item
                else:
                    assert preloader_task.done()
                    # raise preloader_task's exception if any
                    preloader_task.result()
                    break
        finally:
            preloader_task.cancel()
    else:
        q = asyncio.Queue(maxsize=n_preload-1)

        async def preloader():
            try:
                async for item in aiterable:
                    await q.put(item)
            finally:
                await q.put(_sentinel)

        preloader_task = loop.create_task(preloader())

        try:
            while True:
                item = await q.get()
                if item is not _sentinel:
                    yield item
                else:
                    assert preloader_task.done()
                    preloader_task.result()
                    break
        finally:
            preloader_task.cancel()


async def chain_from_iterable(
        aiterables: Iterable[AsyncIterable[T]],
) -> AsyncIterator[T]:
    for aiterable in aiterables:
        async for item in aiterable:
            yield item


async def chain(*aiterables: AsyncIterable[T]) -> AsyncIterator[T]:
    for aiterable in aiterables:
        async for item in aiterable:
            yield item