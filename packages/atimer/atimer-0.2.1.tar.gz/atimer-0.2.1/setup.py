#!/usr/bin/env python
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

from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

setup(
    name='atimer',
    packages=find_packages('.'),
    version='0.2.1',
    description='atimer - timer library for asyncio',
    author='Artur Wroblewski',
    author_email='wrobell@riseup.net',
    url='https://wrobell.dcmod.org/atimer',
    classifiers=[
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
    ],
    ext_modules=cythonize([
        Extension('atimer._atimer', ['atimer/_atimer.pyx'])
    ]),
    license='GPLv3+',
    long_description="""\
The `atimer` library implements asynchronous timer Python coroutine, which
can be used with Python `asyncio <https://docs.python.org/3/library/asyncio.html>`_
module API.

The timer allows to schedule tasks at regular intervals and is implemented
on top of `timerfd <http://man7.org/linux/man-pages/man2/timerfd_create.2.html>`_
Linux kernel interface.

The `atimer` library is licensed under terms of GPL license, version 3, see
`COPYING <https://www.gnu.org/licenses/gpl-3.0.en.html>`_ file for details.
"""
)

# vim: sw=4:et:ai
