
+++++++
 Usage
+++++++

.. module:: trio_asyncio

Using :mod:`trio` from :mod:`asyncio`, or vice versa, requires two steps:

* :ref:`Set up a main loop that supports both <startup>`
* :ref:`Use cross-domain function calls <cross-calling>`

Because :mod:`trio` and :mod:`asyncio` differ in some key semantics, most
notably how they handle tasks and cancellation, usually their domains are
strictly separated – i.e. you need to call a wrapper that translates from
one to the other. While :mod:`trio_asyncio` includes a wrapper that
allows you ignore that separation, you probably should not use it in
non-trivial programs.

.. _startup:

----------------------
 Startup and shutdown
----------------------

.. _trio-loop:

Trio main loop
++++++++++++++

Typically, you start with a Trio program which you need to extend with
asyncio code.

Before::

    import trio

    trio.run(async_main, *args)

After::

    import trio
    import trio_asyncio
    
    trio_asyncio.run(async_main, *args)

Within ``async_main``, calls to :func:`asyncio.get_event_loop` will return
the currently-running :class:`trio_asyncio.TrioEventLoop` instance. See
:ref:`below <cross-calling>` on how to use it to actually call async code.

Equivalently, wrap your main loop (or any other code that needs to talk to
asyncio) in a :func:`trio_asyncio.open_loop` call::

    import trio
    import trio_asyncio

    async def async_main_wrapper(*args):
        async with trio_asyncio.open_loop() as loop:
            assert loop == asyncio.get_event_loop()
            await async_main(*args)

    trio.run(async_main_wrapper, *args)

Within the ``async with`` block, an asyncio mainloop is active. Note that
unlike a traditional :mod:`asyncio` mainloop, this loop will be
automatically closed (not just stopped) when the end of the ``with
open_loop`` block is reached.

As this code demonstrates, you don't need to pass the ``loop`` argument
around, as :func:`asyncio.get_event_loop` will retrieve it when you're in
the loop's context.

.. autofunction:: trio_asyncio.open_loop

.. autofunction:: trio_asyncio.run

.. autoclass:: trio_asyncio.TrioEventLoop

.. note:

   The ``async with open_loop()`` way of running ``trio_asyncio`` is
   useful for writing a library that can use ``asyncio`` code, supported by
   a "local" asyncio loop, without affecting the rest of your Trio program.

   Thus, under Trio you can have multiple concurrent ``asyncio`` loops.

Stopping
--------

The asyncio mainloop will be stopped automatically when the code within
``async with open_loop()`` / ``trio_asyncion.run()`` exits. Trio-asyncio
will process all outstanding callbacks and terminate. As in asyncio,
callbacks which are added during this step will be ignored.

You cannot restart the loop, nor would you want to.

Asyncio main loop.
++++++++++++++++++

If you'd like to keep your plain ``asyncio`` main loop and call Trio code
from it, there's one small problem: It won't work. Sorry.

There are two workarounds. One is to use ``asyncio``'s support for
threading and start a Trio loop in another thread. ``trio_asyncio`` might
learn some dedicated support for this mode, but basic ``trio`` and
``asyncio`` thread support is sufficient.

.. _native-loop:

The other way is to use a ``trio_asyncio`` main loop. You then run your
complete asyncio code in its context. In other words, you should transform
this code::

    def main():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(async_main())
    
or (Python 3.7 ++)::

    def main():
        asyncio.run(async_main())
    
to this::

    async def trio_main():
        await trio_asyncio.aio_as_trio(async_main)()

    def main():
        trio_asyncio.run(trio_main)

In real-world programs, this may be somewhat difficult. The good part is
that ``asyncio`` itself is transitioning towards the ``asyncio.run()`` way,
so the effort won't be wasted.

Compatibility issues
++++++++++++++++++++

Loop implementations
--------------------

There are replacements event loops for ``asyncio``, e.g. ``uvloop``.
``trio_asyncio`` is not compatible with them.

Multithreading
--------------

``trio_asyncio`` monkey-patches ``asyncio``'s loop policy to be thread-local.

This lets you use ``uvloop`` in one thread while running ``trio_asyncio``
in another.

Interrupting the asyncio loop
-----------------------------

Does not work: ``run_until_complete`` / ``run_forever`` are no longer
supported. You need to refactor your main loop. Broadly speaking, this
means that you need to replace this code::

    async def setup():
        pass # … start your services
    async def shutdown():
        pass # … terminate services and clean up
        loop.stop()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup)
    loop.run_forever()
        
with::

    stopped_event = trio.Event()
    async def setup():
        pass # … start your services
    async def cleanup():
        pass # … terminate services and clean up
    async def shutdown(): # no longer needs to be async
        stopped_event.set()

    async def async_main():
        await aio_as_trio(setup)()
        await stopped_event.wait()
        await aio_as_trio(cleanup)()
    trio_asyncio.run(async_main)

Detecting the loop context
--------------------------

:func:`sniffio.current_async_library` correctly reports "asyncio" when
running in an asyncio context. (This requires Python 3.7, for
:mod:`contextvars` support in :mod:`asyncio`).

However, this feature should not be necessary because 
your code either is running within a call to :func:`trio_asyncio.aio_as_trio`,
or it is not. There should not be any "maybe" here: you shouldn't indiscriminately
call async code from both contexts – they have different semantics, esp.
concerning cancellation.

The only reasonable use for detecting the loop context is as ::

    assert sniffio.current_async_library() == "trio"

(or "asyncio"), to detect mismatched contexts while porting code
from :mod:`asyncio` to :mod:`trio`.

.. _cross-calling:

---------------
 Cross-calling
---------------

First, a bit of background.

For historical reasons, calling an async function (of any
flavor) is a two-step process – that is, given ::

    async def proc():
        pass

a call to ``await proc()`` does two things:

  * ``proc()`` creates an ``awaitable``, i.e. something that has an
    ``__await__`` method.

  * ``await proc()`` then iterates this awaitable until it ends,
    supported by your event loop's runtime system.

:mod:`asyncio` traditionally uses awaitables for indirect procedure calls,
so you often see the pattern::

    async def some_code():
        pass
    async def run(proc):
        await proc
    await run(some_code())

This method has a problem: it decouples creating the awailable from running
it. If you decide to add code to ``run`` that retries running ``proc`` when
it encounters a specific error, you're out of luck.

Trio, in contrast, uses (async) callables::

    async def some_code():
        pass
    async def run(proc):
        await proc()
    await run(some_code)

Here, calling ``proc`` multiple times from within ``run`` is not a problem.

:mod:`trio_asyncio` adheres to Trio conventions, but the
:mod:`asyncio` way is also supported when possible.

Calling asyncio from Trio
+++++++++++++++++++++++++

Wrap the callable, awaitable, generator, or iterator in
:func:`trio_asyncio.aio_as_trio`.

Thus, you can call an :mod:`asyncio` function from :mod:`trio` thus::

    async def aio_sleep(sec=1):
        await asyncio.sleep(sec)
    async def trio_sleep(sec=2):
        await aio_as_trio(aio_sleep)(sec)
    trio_asyncio.run(trio_sleep, 3)

or pre-wrapped::

    @aio_as_trio
    async def aio_sleep(sec=1):
        await asyncio.sleep(sec)
    async def trio_sleep(sec=2):
        await aio_sleep(sec)
    trio_asyncio.run(trio_sleep, 3)

or as an awaitable::

    async def aio_sleep(sec=1):
        await asyncio.sleep(sec)
    async def trio_sleep(sec=2):
        await aio_as_trio(aio_sleep(sec))
    trio_asyncio.run(trio_sleep, 3)

This also works with :mod:`asyncio` Futures::

    async def aio_sleep(sec=1):
        await asyncio.sleep(sec)
        return 42
    async def trio_sleep(sec=2):
        f = aio_sleep(1)
        f = asyncio.ensure_future(f)
        r = await aio_as_trio(f)
        assert r == 42
    trio_asyncio.run(trio_sleep, 3)
    
You can wrap context handlers::

    class AsyncCtx:
        async def __aenter__(self):
            await asyncio.sleep(1)
            return self
        async def __aexit__(self, *tb):
            await asyncio.sleep(1)
        async def delay(self, sec=1):
            await asyncio.sleep(sec)
    async def trio_ctx():
        async with aio_as_trio(AsyncCtx()) as ctx:
            print("within")
            await aio_as_trio(ctx.delay)(2)
    trio_asyncio.run(trio_ctx)

As you can see, while :func:`trio_asyncio.aio_as_trio` trio-izes the actual
context, it doesn't know about the context's methods. You still need to
treat them as :mod:`asyncio` methods and wrap them appropriately when you
call them.

Note that *creating* the async context handler is not itself an
asynchronous process, i.e. ``AsyncCtx.__init__`` is a normal
synchronous procedure. Only the actual context handlers (the ``__aenter__``
and ``__aexit__`` methods) are asynchronous. This is why you need to wrap
the context handler itself – unlike simple procedure calls, you cannot wrap
the call for generating the context handler.

Thus, the following code **will not work**::

    async def trio_ctx():
        async with aio_as_trio(AsyncCtx)() as ctx:
            print("within")

You can also wrap async generators or iterators::

    async def aio_slow():
        n = 0
        while True:
            await asyncio.sleep(n)
            yield n
            n += 1
    async def printer():
        async for n in aio_as_trio(aio_slow()):
            print(n)
    trio_asyncio.run(printer)

As above, *creating* the async iterator is not itself an asynchronous
process, i.e. the ``__aiter__`` method that creates the generator or
iterator is a normal synchronous procedure. Only the actual iteration
step (the iterator's ``__anext__`` method) is asynchronous. Again, you need
to wrap the iterator, not the code creating it – the following code
**will not work**::

    async def printer():
        async for n in aio_as_trio(aio_slow)():
            print(n)

.. autofunction:: trio_asyncio.aio_as_trio


Too complicated?
----------------

There's also a somewhat-magic wrapper (:func:`trio_asyncio.allow_asyncio`)
which, as the name implies, allows you to directly call :mod:`asyncio`
functions. It also works for awaiting futures and for using generators or
context managers::

    async def hybrid():
        await trio.sleep(1)
        await asyncio.sleep(1)
        print("Well, that worked")
    trio_asyncio.run(trio_asyncio.allow_asyncio, hybrid)

This method works for one-off code. However, there are a couple of
semantic differences between :mod:`asyncio` and :mod:`trio` which
:func:`trio_asyncio.allow_asyncio` is unable to account for.

Worse, :func:`trio_asyncio.allow_asyncio` can be used to auto-adapt asyncio
code to Trio callers, but not vice versa.

Thus, you really should not use it for "real" programs or libraries.

.. autofunction:: trio_asyncio.allow_asyncio

Calling Trio from asyncio
+++++++++++++++++++++++++

Wrap the callable, awaitable, generator, or iterator in
:func:`trio_asyncio.trio_as_aio`.

Thus, you can call a :mod:`trio` function from :mod:`asyncio` thus::

    async def trio_sleep(sec=1):
        await trio.sleep(sec)
    async def aio_sleep(sec=2):
        await aio_as_trio(trio_sleep)(sec)
    trio_asyncio.run(aio_as_trio, aio_sleep, 3)

or pre-wrapped::

    @trio_as_aio
    async def trio_sleep(sec=1):
        await trio.sleep(sec)
    async def aio_sleep(sec=2):
        await trio_sleep(sec)
    trio_asyncio.run(aio_as_trio, aio_sleep, 3)

In contrast to :func:`trio_asyncio.aio_as_trio`, using an awaitable is not
supported because that's not an idiom :mod:`trio` uses.

Calling a function wrapped with :func:`trio_asyncio.trio_as_aio` returns a
regular :class:`asyncio.Future`. Thus, you can call it from a synchronous
context (e.g. a callback hook). Of course, you're responsible for catching
any errors – either arrange to ``await`` the future, or use
``.add_done_callback()`` ::

    async def trio_sleep(sec=1):
        await trio.sleep(sec)
        return 42
    def cb(f):
        assert f.result == 42
    async def aio_sleep(sec=2):
        f = trio_as_aio(trio_sleep)(1)
        f.add_done_callback(cb)
        r = await f
        assert r == 42
    trio_asyncio.run(aio_as_trio, aio_sleep, 3)

You can wrap context handlers::

    class TrioCtx:
        async def __aenter__(self):
            await trio.sleep(1)
            return self
        async def __aexit__(self, *tb):
            await trio.sleep(1)
        async def delay(self, sec=1):
            await trio.sleep(sec)
    async def aio_ctx():
        async with trio_as_aio(AsyncCtx()) as ctx:
            print("within")
            await trio_as_aio(ctx.delay)(2)
    trio_asyncio.run(aio_as_trio, aio_ctx)

You can also wrap async generators or iterators::

    async def trio_slow():
        n = 0
        while True:
            await trio.sleep(n)
            yield n
            n += 1
    async def printer():
        async for n in trio_as_aio(aio_slow()):
            print(n)
    trio_asyncio.run(aio_as_trio, printer)

.. autofunction:: trio_as_aio


Trio background tasks
---------------------

If you want to start a Trio task that shall be monitored by ``trio_asyncio``
(i.e. an uncaught error will propagate to, and terminate, the asyncio event
loop) instead of a :class:`asyncio.Future`, use
:meth:`trio_asyncio.TrioEventLoop.run_trio_task`.

.. automethod:: trio_asyncio.TrioEventLoop.run_trio_task

Multiple asyncio loops
++++++++++++++++++++++

Trio-asyncio supports running multiple concurrent asyncio loops in the same
thread. You may even nest them.

This means that you can write a trio-ish wrapper around an asyncio-using
library without regard to whether the main loop or another library also use
trio-asyncio.

You can use :meth:`trio_asyncio.TrioEventLoop.autoclose` to tell trio-asyncio to auto-close
a file descriptor when the loop terminates. This setting only applies to
file descriptors that have been submitted to a loop's
:meth:`trio_asyncio.TrioEventLoop.add_reader` or
:meth:`trio_asyncio.TrioEventLoop.add_writer` methods. As such, this
method is mainly useful for servers and should be used as supplementing,
but not replacing, a ``finally:`` handler or an ``async with aclosing():``
block.

.. automethod:: trio_asyncio.TrioEventLoop.autoclose

.. automethod:: trio_asyncio.TrioEventLoop.add_reader
.. automethod:: trio_asyncio.TrioEventLoop.remove_reader

.. automethod:: trio_asyncio.TrioEventLoop.add_writer
.. automethod:: trio_asyncio.TrioEventLoop.remove_writer

Errors and cancellations
++++++++++++++++++++++++

Errors and cancellations are propagated almost-transparently.

For errors, this is straightforward.

Cancellations are also propagated whenever possible. This means

* the task started with ``run_trio()`` is cancelled when you cancel
  the future which ``run_trio`` returns

* when the task started with ``run_trio()`` is cancelled, 
  the future gets cancelled

* the future used in ``run_aio_future()`` is cancelled when the Trio code
  calling it is cancelled

* However, when the future passed to ``run_aio_future()`` is cancelled (i.e.
  when the task associated with it raises ``asyncio.CancelledError``), that
  exception is passed along unchanged.

  This asymmetry is intentional since the code that waits for the future
  often is not within the cancellation context of the part that
  created it. Cancelling the future would thus impact the wrong (sub)task.

----------------
 Deferred Calls
----------------

:meth:`python:asyncio.loop.call_soon` and friends work as usual.

----------------
 Worker Threads
----------------

:meth:`python:asyncio.loop.run_in_executor` works as usual.

There is one caveat: the executor must be either ``None`` or an instance of
:class:`trio_asyncio.TrioExecutor`. The constructor of this class accepts one
argument: the number of workers.

.. autoclass:: trio_asyncio.TrioExecutor

------------------
 File descriptors
------------------

:meth:`python:asyncio.loop.add_reader` and
:meth:`python:asyncio.loop.add_writer` work as usual, if you really
need them. Behind the scenes, these calls create a Trio task which runs the
callback.

You might consider converting code using these calls to native Trio tasks.

---------
 Signals
---------

:meth:`python:asyncio.loop.add_signal_handler` works as usual.

------------
Subprocesses
------------

:func:`asyncio.create_subprocess_exec` and
:func:`asyncio.create_subprocess_shell` work as usual.

You might want to convert these calls to native Trio subprocesses.

.. note:

   The class that watches for child processes must be an instance of
   :class:`trio_asyncio.TrioChildWatcher`. Trio-Asyncio enforces this.

