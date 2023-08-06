#
# atimer - timer library for asyncio
#
# Copyright (C) 2016-2018 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import asyncio
import atimer
import time

N = 10
INTERVAL = 0.5

async def printer(timer):
    timer.start()
    prev = time.monotonic()
    for i in range(N):
        await timer
        current = time.monotonic()
        diff = current - prev
        print('{0:.3f}ms        {0:.6f}us'.format(diff))
        prev = current
        time.sleep(INTERVAL / 10)
    timer.close()


loop = asyncio.get_event_loop()
timer = atimer.Timer(INTERVAL)
#asyncio.ensure_future(timer)
loop.run_until_complete(printer(timer))

# vim: sw=4:et:ai
