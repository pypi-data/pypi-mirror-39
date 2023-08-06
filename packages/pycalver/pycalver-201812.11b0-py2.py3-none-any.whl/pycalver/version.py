# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://github.com/mbarkhau/pycalver
#
# Copyright (c) 2018 Manuel Barkhau (@mbarkhau) - MIT License
# SPDX-License-Identifier: MIT
"""Functions related to version string manipulation.

>>> version_info = PYCALVER_RE.match("v201712.0123-alpha").groupdict()
>>> assert version_info == {
...     "version" : "v201712.0123-alpha",
...     "calver"  : "v201712",
...     "year"    : "2017",
...     "month"   : "12",
...     "build"   : ".0123",
...     "release" : "-alpha",
... }
>>>
>>> version_info = PYCALVER_RE.match("v201712.0033").groupdict()
>>> assert version_info == {
...     "version" : "v201712.0033",
...     "calver"  : "v201712",
...     "year"    : "2017",
...     "month"   : "12",
...     "build"   : ".0033",
...     "release" : None,
... }
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import re
import logging
import pkg_resources
import typing as typ
import datetime as dt
from . import lex_id
str = getattr(__builtins__, 'unicode', str)
log = logging.getLogger('pycalver.version')
PYCALVER_PATTERN = """
\\b
(?P<version>
    (?P<calver>
       v                        # "v" version prefix
       (?P<year>\\d{4})
       (?P<month>\\d{2})
    )
    (?P<build>
        \\.                      # "." build nr prefix
        \\d{4,}
    )
    (?P<release>
        \\-                      # "-" release prefix
        (?:alpha|beta|dev|rc|post)
    )?
)(?:\\s|$)
"""
PYCALVER_RE = re.compile(PYCALVER_PATTERN, flags=re.VERBOSE)
VersionInfo = typ.NamedTuple('VersionInfo', [('version', str), (
    'pep440_version', str), ('calver', str), ('year', str), ('month', str),
    ('build', str), ('release', typ.Optional[str])])


def parse_version_info(version_str):
    """Parse a PyCalVer string.

    >>> vnfo = parse_version_info("v201712.0033-beta")
    >>> assert vnfo == VersionInfo(
    ...     version="v201712.0033-beta",
    ...     pep440_version="201712.33b0",
    ...     calver="v201712",
    ...     year="2017",
    ...     month="12",
    ...     build=".0033",
    ...     release="-beta",
    ... )
    """
    match = PYCALVER_RE.match(version_str)
    if match is None:
        raise ValueError('Invalid PyCalVer string: {0}'.format(version_str))
    kwargs = match.groupdict()
    kwargs['pep440_version'] = pycalver_to_pep440(kwargs['version'])
    return VersionInfo(**kwargs)


def current_calver():
    """Generate calver version string based on current date.

    example result: "v201812"
    """
    return dt.date.today().strftime('v%Y%m')


def incr(old_version, **kwargs):
    release = kwargs.get('release', None)
    """Increment a full PyCalVer version string.

    Old_version is assumed to be a valid calver string,
    already validated in pycalver.config.parse.
    """
    old_ver = parse_version_info(old_version)
    new_calver = current_calver()
    if old_ver.calver > new_calver:
        log.warning("'version.incr' called with '{0}', ".format(old_version
            ) + 'which is from the future, '.format() +
            'maybe your system clock is out of sync.'.format())
        new_calver = old_ver.calver
    new_build = lex_id.next_id(old_ver.build[1:])
    new_release = None
    if release is None:
        if old_ver.release:
            new_release = old_ver.release[1:]
        else:
            new_release = None
    elif release == 'final':
        new_release = None
    else:
        new_release = release
    new_version = new_calver + '.' + new_build
    if new_release:
        new_version += '-' + new_release
    return new_version


def pycalver_to_pep440(version):
    """Derive pep440 compliant version string from PyCalVer version string.

    >>> pycalver_to_pep440("v201811.0007-beta")
    '201811.7b0'
    """
    return str(pkg_resources.parse_version(version))
