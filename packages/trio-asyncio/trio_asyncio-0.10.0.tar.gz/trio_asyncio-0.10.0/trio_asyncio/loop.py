# This code implements a clone of the asyncio mainloop which hooks into
# Trio.

import sys
import trio
import asyncio
import warnings
import threading

from .adapter import current_loop, current_policy
from .util import run_aio_future
from .async_ import TrioEventLoop, open_loop

try:
    from trio.hazmat import wait_for_child
except ImportError:
    from .child import wait_for_child

import logging
logger = logging.getLogger(__name__)

__all__ = [
    'run',
    'run_trio_task',
    'run_trio',
    'run_future',
    'run_aio_future',
    'run_coroutine',  # deprecated
    'run_aio_coroutine',
    'run_asyncio',
    'wrap_generator',
    'run_iterator',
    'TrioChildWatcher',
    'TrioPolicy',
]

_faked_policy = threading.local()

# We can monkey-patch asyncio's get_event_loop_policy but if asyncio is
# imported before Trio, the asyncio acceleration C code in 3.7+ caches
# get_event_loop_policy.
# Thus we always set our policy. After that, our monkeypatched
# setter stores the policy in a thread-local variable to which our policy
# will forward all requests when Trio is not running.


class _TrioPolicy(asyncio.events.BaseDefaultEventLoopPolicy):
    _loop_factory = TrioEventLoop

    def new_event_loop(self):
        try:
            trio.hazmat.current_task()
        except RuntimeError:
            if 'pytest' not in sys.modules:
                warnings.warn(
                    "trio_asyncio should be used from within a Trio event loop.",
                    DeprecationWarning,
                    stacklevel=2
                )
            real_policy = getattr(_faked_policy, 'policy', None)
            if real_policy is not None:
                return real_policy.new_event_loop()

            from .sync import SyncTrioEventLoop
            loop = SyncTrioEventLoop()
            return loop
        else:
            raise RuntimeError(
                "You're within a Trio environment.\n"
                "Use 'async with open_loop()' instead."
            )

    def get_event_loop(self):
        """Get the current event loop.

        Note that this will auto-generate an event loop if none exists, for
        compatibility with asyncio.

        To get a Trio-compatible asyncio loop, use
        ``async with trio_asyncio.open_loop() as loop:``.

        To test whether an event loop is running, check the loop policy's
        ``.current_event_loop`` property.
        """
        try:
            trio.hazmat.current_task()
        except RuntimeError:  # no Trio task is active
            # this creates a new loop in the main task
            real_policy = getattr(_faked_policy, 'policy', None)
            if real_policy is not None:
                return real_policy.get_event_loop()

            return super().get_event_loop()
        else:
            return current_loop.get()

    @property
    def current_event_loop(self):
        """The currently-running event loop, if one exists."""
        loop = current_loop.get()
        if loop is None:
            loop = super().get_event_loop()
        return loop

    def set_event_loop(self, loop):
        """Set the current event loop."""
        try:
            trio.hazmat.current_task()
        except RuntimeError:  # no Trio task is active
            # this creates a new loop in the main task
            real_policy = getattr(_faked_policy, 'policy', None)
            if real_policy is not None:
                return real_policy.set_event_loop(loop)
            return super().set_event_loop(loop)
        else:
            current_loop.set(loop)


from asyncio import events as _aio_event

#####

_orig_policy_get = _aio_event.get_event_loop_policy


def _new_policy_get():
    try:
        task = trio.hazmat.current_task()
    except RuntimeError:
        policy = getattr(_faked_policy, "policy", None)
        if policy is None:
            policy = _original_policy
    else:
        policy = task.context.get(current_policy, None)
        if policy is None:
            policy = _new_policy
    return policy


_aio_event.get_event_loop_policy = _new_policy_get
asyncio.get_event_loop_policy = _new_policy_get

#####

_orig_policy_set = _aio_event.set_event_loop_policy


def _new_policy_set(new_policy):
    if isinstance(new_policy, TrioPolicy):
        raise RuntimeError("You can't set the Trio loop policy manually")
    assert isinstance(new_policy, asyncio.AbstractEventLoopPolicy)
    _faked_policy.policy = new_policy

    try:
        task = trio.hazmat.current_task()
    except RuntimeError:
        policy = None
    else:
        policy = task.context.get(current_policy, None)
    if policy is None:
        policy = _orig_policy_get()
    return policy


_aio_event.set_event_loop_policy = _new_policy_set
asyncio.set_event_loop_policy = _new_policy_set

#####

try:
    _orig_run_get = _aio_event._get_running_loop

except AttributeError:
    pass

else:

    def _new_run_get():
        try:
            task = trio.hazmat.current_task()
        except RuntimeError:
            loop = _orig_run_get()
        else:
            loop = task.context.get(current_loop, None)
            if loop is None:
                raise RuntimeError("No trio_asyncio loop is active.")

        return loop

    _aio_event._get_running_loop = _new_run_get

#####

_orig_loop_get = _aio_event.get_event_loop


def _new_loop_get():
    loop = _new_run_get()
    if loop is None:
        loop = _orig_loop_get()
    return loop


_aio_event.get_event_loop = _new_loop_get
asyncio.get_event_loop = _new_loop_get


class TrioPolicy(_TrioPolicy, asyncio.DefaultEventLoopPolicy):
    """This is the loop policy that's active whenever we're in a Trio context."""

    def _init_watcher(self):
        with asyncio.events._lock:
            if self._watcher is None:  # pragma: no branch
                self._watcher = TrioChildWatcher()
                if isinstance(threading.current_thread(), threading._MainThread):
                    self._watcher.attach_loop(current_loop.get())

        if self._watcher is not None and \
                isinstance(threading.current_thread(), threading._MainThread):
            self._watcher.attach_loop(current_loop.get())

    def set_child_watcher(self, watcher):
        if watcher is not None:
            if not isinstance(watcher, TrioChildWatcher):
                # raise RuntimeError("You must use a TrioChildWatcher here. "
                #                    "Sorry.")
                # warnings.warn("You must use a TrioChildWatcher.")
                #
                loop = watcher._loop  # ugh.
                watcher.close()
                watcher = TrioChildWatcher()
                watcher.attach_loop(loop)
        super().set_child_watcher(watcher)


_original_policy = _orig_policy_get()
_new_policy = TrioPolicy()
_orig_policy_set(_new_policy)


class TrioChildWatcher(asyncio.AbstractChildWatcher if sys.platform != 'win32' else object):
    # AbstractChildWatcher not available under Windows
    def __init__(self):
        super().__init__()
        self._callbacks = {}  # pid => handler

    def attach_loop(self, loop):
        self._loop = loop

    async def _waitpid(self, pid, callback, *args):
        returncode = await wait_for_child(pid)
        callback(pid, returncode, *args)

    def add_child_handler(self, pid, callback, *args):
        """Add a callback to run when a child process terminates."""
        h = self._loop.run_trio(self._waitpid, pid, callback, *args)
        self._callbacks[pid] = h

    def remove_child_handler(self, pid):
        """Remove the callback to run when a child process terminates."""
        h = self._callbacks.pop(pid, None)
        if h is None:
            return False
        h.cancel()
        return True

    def close(self):
        for pid in list(self._callbacks):
            h = self._callbacks.pop(pid, None)
            if h is None:
                continue
            h.cancel()
        self._loop = None

    def __enter__(self):
        return self

    def __exit__(self, *tb):
        self.close()


def wrap_generator(proc, *args):
    """Run an asyncio generator from Trio.
    """
    loop = current_loop.get()
    if loop is None:
        raise RuntimeError("You are not within a trio_asyncio loop")
    return loop.wrap_generator(proc, *args)


def run_iterator(aiter):
    """Run an asyncio iterator from Trio.
    """
    loop = current_loop.get()
    if loop is None:
        raise RuntimeError("You are not within a trio_asyncio loop")
    return loop.run_iterator(aiter)


def wrap_trio_context(ctx):
    """Run a Trio context manager from asyncio.
    """
    loop = current_loop.get()
    if loop is None:
        raise RuntimeError("You are not within a trio_asyncio loop")
    return loop.wrap_trio_context(ctx)


async def run_asyncio(proc, *args):
    """Run an asyncio function or method from Trio.

    :return: whatever the procedure returns.
    :raises: whatever the procedure raises.

    This is a Trio coroutine.
    """

    loop = current_loop.get()
    if loop is None:
        raise RuntimeError("You are not within a trio_asyncio loop")
    return await loop.run_asyncio(proc, *args)


async def run_aio_coroutine(fut):
    """Wait for an asyncio future/coroutine.

    Cancelling the current Trio scope will cancel the future/coroutine.

    Cancelling the future/coroutine will cause an
    ``asyncio.CancelledError``.

    This is a Trio coroutine.
    """

    loop = current_loop.get()
    if loop is None:
        raise RuntimeError("You are not within a trio_asyncio loop")
    return await loop.run_aio_coroutine(fut)


async def run_coroutine(fut):
    """ deprecated"""
    loop = current_loop.get()
    if loop is None:
        raise RuntimeError("You are not within a trio_asyncio loop")
    return await loop.run_aio_coroutine(fut)


async def run_future(fut):
    """ deprecated"""
    warnings.warn("Use 'await run_aio_future(fut)' instead'", DeprecationWarning)
    return await run_aio_future(fut)


def run_trio(proc, *args):
    """Call an asynchronous Trio function from asyncio.

    Returns a Future with the result / exception.

    Cancelling the future will cancel the Trio task running your
    function, or prevent it from starting if that is still possible.

    You need to handle errors yourself.
    """
    loop = current_loop.get()
    if loop is None:
        raise RuntimeError("You are not within a trio_asyncio loop")
    return loop.run_trio(proc, *args)


def run_trio_task(proc, *args):
    """Call an asynchronous Trio function from sync context.

    This method queues the task and returns immediately.
    It does not return a value.

    An uncaught error will propagate to, and terminate, the trio-asyncio loop.
    """
    loop = current_loop.get()
    if loop is None:
        raise RuntimeError("You are not within a trio_asyncio loop")
    loop.run_trio_task(proc, *args)


def run(proc, *args, queue_len=None):
    """Like :func:`trio.run`, but adds a context that supports asyncio.
    """

    async def _run_task(proc, args):
        async with open_loop(queue_len=queue_len):
            return await proc(*args)

    trio.run(_run_task, proc, args)
