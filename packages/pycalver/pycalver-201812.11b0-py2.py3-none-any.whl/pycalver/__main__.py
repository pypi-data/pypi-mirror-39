#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://gitlab.com/mbarkhau/pycalver
#
# Copyright (c) 2018 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""
CLI module for PyCalVer.

Provided subcommands: show, incr, init, bump
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
import click
import logging
import typing as typ
from . import vcs
from . import parse
from . import config
from . import version
from . import rewrite
_VERBOSE = 0
try:
    import backtrace
    backtrace.hook(align=True, strip_path=True, enable_on_envvar_only=True)
except ImportError:
    pass
click.disable_unicode_literals_warning = True
log = logging.getLogger('pycalver.cli')


def _init_logging(verbose=0):
    if verbose >= 2:
        log_format = (
            '%(asctime)s.%(msecs)03d %(levelname)-7s %(name)-15s - %(message)s'
            )
        log_level = logging.DEBUG
    elif verbose == 1:
        log_format = '%(levelname)-7s - %(message)s'
        log_level = logging.INFO
    else:
        log_format = '%(message)s'
        log_level = logging.WARNING
    logging.basicConfig(level=log_level, format=log_format, datefmt=
        '%Y-%m-%dT%H:%M:%S')
    log.debug('Logging initialized.')


@click.group()
@click.version_option()
@click.help_option()
@click.option('-v', '--verbose', count=True, help=
    'Control log level. -vv for debug level.')
def cli(verbose=0):
    """Automatically update PyCalVer version strings on python projects."""
    global _VERBOSE
    _VERBOSE = verbose


@cli.command()
@click.argument('old_version')
@click.option('-v', '--verbose', count=True, help=
    'Control log level. -vv for debug level.')
@click.option('--release', default=None, metavar='<name>', help=
    'Override release name of current_version')
def incr(old_version, verbose=0, release=None):
    """Increment a version number for demo purposes."""
    _init_logging(verbose=max(_VERBOSE, verbose))
    if release and release not in parse.VALID_RELEASE_VALUES:
        log.error('Invalid argument --release={0}'.format(release))
        log.error('Valid arguments are: {0}'.format(', '.join(parse.
            VALID_RELEASE_VALUES)))
        sys.exit(1)
    new_version = version.incr(old_version, release=release)
    pep440_version = version.pycalver_to_pep440(new_version)
    print('PyCalVer Version:', new_version)
    print('PEP440 Version:', pep440_version)


def _update_cfg_from_vcs(cfg, fetch):
    try:
        _vcs = vcs.get_vcs()
        log.debug('vcs found: {0}'.format(_vcs.name))
        if fetch:
            log.info('fetching tags from remote'.format())
            _vcs.fetch()
        version_tags = [tag for tag in _vcs.ls_tags() if version.
            PYCALVER_RE.match(tag)]
        if version_tags:
            version_tags.sort(reverse=True)
            log.debug('found {0} tags: {1}'.format(len(version_tags),
                version_tags[:2]))
            latest_version_tag = version_tags[0]
            if latest_version_tag > cfg.current_version:
                log.info('Working dir version        : {0}'.format(cfg.
                    current_version))
                log.info('Latest version from {0:>3} tag: {1}'.format(_vcs.
                    name, latest_version_tag))
                cfg = cfg._replace(current_version=latest_version_tag)
        else:
            log.debug('no vcs tags found')
    except OSError:
        log.debug('No vcs found')
    return cfg


@cli.command()
@click.option('-v', '--verbose', count=True, help=
    'Control log level. -vv for debug level.')
@click.option('-f', '--fetch/--no-fetch', is_flag=True, default=True, help=
    'Sync tags from remote origin.')
def show(verbose=0, fetch=True):
    """Show current version."""
    _init_logging(verbose=max(_VERBOSE, verbose))
    ctx = config.init_project_ctx(project_path='.')
    cfg = config.parse(ctx)
    if cfg is None:
        log.error('Could not parse configuration from setup.cfg')
        sys.exit(1)
    cfg = _update_cfg_from_vcs(cfg, fetch=fetch)
    print('Current Version: {0}'.format(cfg.current_version))
    print('PEP440 Version : {0}'.format(cfg.pep440_version))


@cli.command()
@click.option('-v', '--verbose', count=True, help=
    'Control log level. -vv for debug level.')
@click.option('--dry', default=False, is_flag=True, help=
    "Display diff of changes, don't rewrite files.")
def init(verbose=0, dry=False):
    """Initialize [pycalver] configuration."""
    _init_logging(verbose=max(_VERBOSE, verbose))
    ctx = config.init_project_ctx(project_path='.')
    cfg = config.parse(ctx)
    if cfg:
        log.error('Configuration already initialized in {ctx.config_filepath}')
        sys.exit(1)
    if dry:
        print("Exiting because of '--dry'. Would have written to setup.cfg:")
        cfg_lines = config.default_config(ctx)
        print('\n    ' + '\n    '.join(cfg_lines))
        return
    config.write_content(ctx)


def _assert_not_dirty(vcs, filepaths, allow_dirty):
    dirty_files = vcs.status()
    if dirty_files:
        log.warn('{0} working directory is not clean:'.format(vcs.name))
        for dirty_file in dirty_files:
            log.warn('    ' + dirty_file)
    if not allow_dirty and dirty_files:
        sys.exit(1)
    dirty_pattern_files = set(dirty_files) & filepaths
    if dirty_pattern_files:
        log.error('Not commiting when pattern files are dirty:')
        for dirty_file in dirty_pattern_files:
            log.warn('    ' + dirty_file)
        sys.exit(1)


def _bump(cfg, new_version, allow_dirty=False):
    _vcs = None
    try:
        _vcs = vcs.get_vcs()
    except OSError:
        log.warn('Version Control System not found, aborting commit.')
        _vcs = None
    filepaths = set(cfg.file_patterns.keys())
    if _vcs:
        _assert_not_dirty(_vcs, filepaths, allow_dirty)
    rewrite.rewrite(new_version, cfg.file_patterns)
    if _vcs is None or not cfg.commit:
        return
    for filepath in filepaths:
        _vcs.add(filepath)
    _vcs.commit('bump version to {0}'.format(new_version))
    if cfg.tag:
        _vcs.tag(new_version)
        _vcs.push(new_version)


@cli.command()
@click.option('-v', '--verbose', count=True, help=
    'Control log level. -vv for debug level.')
@click.option('-f', '--fetch/--no-fetch', is_flag=True, default=True)
@click.option('--dry', default=False, is_flag=True, help=
    "Display diff of changes, don't rewrite files.")
@click.option('--release', default=None, metavar='<name>', help=
    'Override release name of current_version')
@click.option('--allow-dirty', default=False, is_flag=True, help=
    'Commit even when working directory is has uncomitted changes. (WARNING: The commit will still be aborted if there are uncomitted to files with version strings.'
    )
def bump(release=None, verbose=0, dry=False, allow_dirty=False, fetch=True):
    """Increment the current version string and update project files."""
    verbose = max(_VERBOSE, verbose)
    _init_logging(verbose)
    if release and release not in parse.VALID_RELEASE_VALUES:
        log.error('Invalid argument --release={0}'.format(release))
        log.error('Valid arguments are: {0}'.format(', '.join(parse.
            VALID_RELEASE_VALUES)))
        sys.exit(1)
    ctx = config.init_project_ctx(project_path='.')
    cfg = config.parse(ctx)
    if cfg is None:
        log.error('Could not parse configuration from setup.cfg')
        sys.exit(1)
    cfg = _update_cfg_from_vcs(cfg, fetch=fetch)
    old_version = cfg.current_version
    new_version = version.incr(old_version, release=release)
    log.info('Old Version: {0}'.format(old_version))
    log.info('New Version: {0}'.format(new_version))
    if dry or verbose:
        print(rewrite.diff(new_version, cfg.file_patterns))
    if dry:
        return
    _bump(cfg, new_version, allow_dirty)
