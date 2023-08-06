import asyncio
import collections
import itertools
import socket
from typing import AsyncIterator, Tuple, Iterable, List, Optional, Iterator

from .typing import AddrInfoType, HostType, PortType


RESOLUTION_DELAY = 0.05  # seconds
FIRST_ADDRESS_FAMILY_COUNT = 1


async def _async_builtin_resolver_old(
        host,
        port,
        *,
        type_: int = 0,
        proto: int = 0,
        flags: int = 0,
        resolution_delay: float = RESOLUTION_DELAY,
        first_addr_family_count: int = FIRST_ADDRESS_FAMILY_COUNT,
        loop: asyncio.AbstractEventLoop = None,
) -> AsyncIterator[AddrInfoType]:
    loop = loop or asyncio.get_event_loop()

    # Determine whether host is an IP address literal
    addrinfos = _ipaddr_info(host, port, socket.AF_UNSPEC, type_, proto)
    if addrinfos is not None:
        for addrinfo in addrinfos:
            yield addrinfo
        return

    addrinfos = collections.deque()
    yielded = 0

    async def resolve_ipv6():
        infos = collections.deque(await _getaddrinfo_raise_on_empty(
            host, port, family=socket.AF_INET6,
            type_=type_, proto=proto, flags=flags, loop=loop))
        if not addrinfos:
            addrinfos.extend(infos)
            return
        v4_infos = addrinfos.copy()
        addrinfos.clear()
        for _ in range(first_addr_family_count):
            addrinfos.append(infos.popleft())
        addrinfos.extend(_roundrobin(v4_infos, infos))

    v6_resolve_task = loop.create_task(resolve_ipv6())  # type: asyncio.Task

    async def resolve_ipv4():
        infos = collections.deque(await _getaddrinfo_raise_on_empty(
            host, port, family=socket.AF_INET,
            type_=type_, proto=proto, flags=flags, loop=loop))
        if not addrinfos:
            addrinfos.extend(infos)
        else:
            v6_infos = addrinfos.copy()
            addrinfos.clear()
            for _ in range(first_addr_family_count - yielded):
                addrinfos.append(v6_infos.popleft())
            addrinfos.extend(_roundrobin(infos, v6_infos))
        if not v6_resolve_task.done():
            await asyncio.wait(
                (v6_resolve_task,), loop=loop, timeout=resolution_delay)

    v4_resolve_task = loop.create_task(resolve_ipv4())  # type: asyncio.Task

    pending = {v6_resolve_task, v4_resolve_task}

    try:
        while True:
            if not addrinfos:
                # No addresses are ready to be yielded
                if not pending:
                    # Both resolve tasks are done
                    assert v6_resolve_task.done()
                    assert v4_resolve_task.done()
                    if yielded:
                        # If we have already yielded something, exit normally
                        return
                    # Otherwise, raise exception
                    raise OSError(
                        f'Address resolution failed, '
                        f'IPv6: <{v6_resolve_task.exception()!r}>, '
                        f'IPv4: <{v4_resolve_task.exception()!r}>')
                # Some resolve tasks are not done yet, wait for one of them
                # and try again
                _, pending = await asyncio.wait(
                    pending, return_when=asyncio.FIRST_COMPLETED)
                continue
            # XXX
    finally:
        v6_resolve_task.cancel()
        v4_resolve_task.cancel()