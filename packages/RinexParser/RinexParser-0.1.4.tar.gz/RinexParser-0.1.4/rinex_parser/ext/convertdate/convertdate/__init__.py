#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of convertdate.
# http://github.com/fitnr/convertdate

# Licensed under the MIT license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2016, fitnr <fitnr@fakeisthenewreal>

# Most of this code is ported from Fourmilab's javascript calendar converter
# http://www.fourmilab.ch/documents/calendar/
# which was developed by John Walker
#
# The algorithms are believed to be derived from the following source:
# Meeus, Jean. Astronomical Algorithms . Richmond: Willmann-Bell, 1991. ISBN 0-943396-35-2.
#    The essential reference for computational positional astronomy.
#
from . import bahai
from . import daycount
from . import dublin
from . import gregorian
from . import hebrew
from . import holidays
from . import indian_civil
from . import islamic
from . import iso
from . import julian
from . import julianday
from . import mayan
from . import ordinal
from . import persian


__version__ = '2.0.7'

__all__ = [
    'holidays', 'bahai', 'dublin',
    'daycount',
    'french_republican', 'gregorian', 'hebrew',
    'indian_civil', 'islamic', 'iso',
    'julian', 'julianday',
    'mayan', 'persian', 'mayan',
    'ordinal',
]
