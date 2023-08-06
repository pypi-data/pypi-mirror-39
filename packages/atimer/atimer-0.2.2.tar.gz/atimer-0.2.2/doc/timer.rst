Timer
=====
Timer instance is created with :py:class:`atimer.Timer` class. The timer
object itself is a~coroutine object and to wait for timer expiration the
object should be awaited with `await` expression. The result of the
expression is number of expirations.

Example usage::

    async def start(timer):
        timer.start()
        while True:
            expirations = await timer
            print(time.monotonic())

    loop = asyncio.get_event_loop()
    timer = atimer.Timer(1)
    loop.run_until_complete(start(timer))

.. vim: sw=4:et:ai
