#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of convertdate.
# http://github.com/fitnr/convertdate

# Licensed under the GPL-v3.0 license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2016, fitnr <fitnr@fakeisthenewreal>
from calendar import isleap as leap, monthrange
from .utils import floor, monthcalendarhelper, jwday

EPOCH = 1721425.5

INTERCALATION_CYCLE_YEARS = 400
INTERCALATION_CYCLE_DAYS = 146097

LEAP_SUPPRESSION_YEARS = 100
LEAP_SUPPRESSION_DAYS = 36524

LEAP_CYCLE_YEARS = 4
LEAP_CYCLE_DAYS = 1461

HAVE_30_DAYS = (4, 6, 9, 11)
HAVE_31_DAYS = (1, 3, 5, 7, 8, 10, 12)


def legal_date(year, month, day):
    '''Check if this is a legal date in the Gregorian calendar'''
    if month == 2:
        daysinmonth = 29 if leap(year) else 28
    else:
        daysinmonth = 30 if month in HAVE_30_DAYS else 31

    if not (0 < day <= daysinmonth):
        raise IndexError("Month {} doesn't have a day {}".format(month, day))

    return True


def to_jd2(year, month, day):
    '''Gregorian to Julian Day Count for years between 1801-2099'''
    # http://quasar.as.utexas.edu/BillInfo/JulianDatesG.html

    legal_date(year, month, day)

    if month <= 2:
        year = year - 1
        month = month + 12

    a = floor(year / 100)
    b = floor(a / 4)
    c = 2 - a + b
    e = floor(365.25 * (year + 4716))
    f = floor(30.6001 * (month + 1))
    return c + day + e + f - 1524.5


def to_jd(year, month, day):
    legal_date(year, month, day)

    if month <= 2:
        leap_adj = 0
    elif leap(year):
        leap_adj = -1
    else:
        leap_adj = -2

    return (
        EPOCH - 1 + (365 * (year - 1)) +
        floor((year - 1) / 4) + (-floor((year - 1) / 100)) +
        floor((year - 1) / 400) + floor((((367 * month) - 362) / 12) + leap_adj + day)
    )


def from_jd(jd):
    '''Return Gregorian date in a (Y, M, D) tuple'''
    wjd = floor(jd - 0.5) + 0.5
    depoch = wjd - EPOCH

    quadricent = floor(depoch / INTERCALATION_CYCLE_DAYS)
    dqc = depoch % INTERCALATION_CYCLE_DAYS

    cent = floor(dqc / LEAP_SUPPRESSION_DAYS)
    dcent = dqc % LEAP_SUPPRESSION_DAYS

    quad = floor(dcent / LEAP_CYCLE_DAYS)
    dquad = dcent % LEAP_CYCLE_DAYS

    yindex = floor(dquad / 365)
    year = (
        quadricent * INTERCALATION_CYCLE_YEARS +
        cent * LEAP_SUPPRESSION_YEARS +
        quad * LEAP_CYCLE_YEARS + yindex
    )

    if not (cent == 4 or yindex == 4):
        year += 1

    yearday = wjd - to_jd(year, 1, 1)

    isleap = leap(year)

    if yearday < 58 + isleap:
        leap_adj = 0
    elif isleap:
        leap_adj = 1
    else:
        leap_adj = 2

    month = floor((((yearday + leap_adj) * 12) + 373) / 367)
    day = int(wjd - to_jd(year, month, 1)) + 1

    return (year, month, day)


def month_length(year, month):
    return monthrange(year, month)[1]


def monthcalendar(year, month):
    start_weekday = jwday(to_jd(year, month, 1))
    monthlen = month_length(year, month)

    return monthcalendarhelper(start_weekday, monthlen)
