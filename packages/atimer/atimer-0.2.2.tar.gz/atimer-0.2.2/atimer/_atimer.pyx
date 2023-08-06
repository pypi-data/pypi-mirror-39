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

from posix.unistd cimport close
from libc.time cimport time_t

cdef extern from "<sys/timerfd.h>":
    enum: CLOCK_MONOTONIC
    enum: TFD_NONBLOCK

    struct timespec:
        time_t tv_sec
        long tv_nsec

    struct itimerspec:
        timespec it_interval
        timespec it_value

    int timerfd_create(int, int)
    int timerfd_settime(int, int, itimerspec*, itimerspec*)
    int timerfd_gettime(int, itimerspec*)


def atimer_init():
    # do not block on file descriptor, so in case of some error, we do not
    # block in event loop callback
    return timerfd_create(CLOCK_MONOTONIC, TFD_NONBLOCK)

def atimer_start(int fd, double interval):
    cdef itimerspec ts
    cdef time_t sec
    cdef long nsec

    sec = <int> interval
    nsec = (interval - sec) * int(1e9)

    ts.it_value.tv_sec = sec
    ts.it_value.tv_nsec = nsec
    ts.it_interval.tv_sec = sec
    ts.it_interval.tv_nsec = nsec

    return timerfd_settime(fd, 0, &ts, NULL)

def atimer_close(int fd):
    cdef int r
    cdef itimerspec ts

    ts.it_interval.tv_sec = 0
    ts.it_interval.tv_nsec = 0
    ts.it_value.tv_sec = 0
    ts.it_value.tv_nsec = 0

    r = timerfd_settime(fd, 0, &ts, NULL)
    close(fd)

    return r

# vim: sw=4:et:ai
