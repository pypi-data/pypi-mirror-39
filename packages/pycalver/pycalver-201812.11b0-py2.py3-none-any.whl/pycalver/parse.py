# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://github.com/mbarkhau/pycalver
#
# Copyright (c) 2018 Manuel Barkhau (@mbarkhau) - MIT License
# SPDX-License-Identifier: MIT
"""Parse PyCalVer strings from files."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import re
import logging
import typing as typ
str = getattr(__builtins__, 'unicode', str)
log = logging.getLogger('pycalver.parse')
VALID_RELEASE_VALUES = 'alpha', 'beta', 'dev', 'rc', 'post'
PATTERN_ESCAPES = [('\\', '\\\\'), ('-', '\\-'), ('.', '\\.'), ('+', '\\+'),
    ('*', '\\*'), ('[', '\\['), ('(', '\\(')]
RE_PATTERN_PARTS = {'pep440_version':
    '\\d{6}\\.[1-9]\\d*(a|b|dev|rc|post)?\\d*', 'version':
    'v\\d{6}\\.\\d{4,}(\\-(alpha|beta|dev|rc|post))?', 'calver': 'v\\d{6}',
    'build': '\\.\\d{4,}', 'release': '(\\-(alpha|beta|dev|rc|post))?'}
PatternMatch = typ.NamedTuple('PatternMatch', [('lineno', int), ('line',
    str), ('pattern', str), ('span', typ.Tuple[int, int]), ('match', str)])
PatternMatches = typ.Iterable[PatternMatch]


def _iter_for_pattern(lines, pattern):
    pattern_tmpl = pattern
    for char, escaped in PATTERN_ESCAPES:
        pattern_tmpl = pattern_tmpl.replace(char, escaped)
    pattern_str = pattern_tmpl.format(**RE_PATTERN_PARTS)
    pattern_re = re.compile(pattern_str)
    for lineno, line in enumerate(lines):
        match = pattern_re.search(line)
        if match:
            yield PatternMatch(lineno, line, pattern, match.span(), match.
                group(0))


def iter_matches(lines, patterns):
    """Iterate over all matches of any pattern on any line.

    >>> lines = ["__version__ = 'v201712.0002-alpha'"]
    >>> patterns = ["{version}", "{pep440_version}"]
    >>> matches = list(iter_matches(lines, patterns))
    >>> assert matches[0] == PatternMatch(
    ...     lineno = 0,
    ...     line   = "__version__ = 'v201712.0002-alpha'",
    ...     pattern= "{version}",
    ...     span   = (15, 33),
    ...     match  = "v201712.0002-alpha",
    ... )
    """
    for pattern in patterns:
        for match in _iter_for_pattern(lines, pattern):
            yield match
