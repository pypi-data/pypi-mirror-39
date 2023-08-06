# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://github.com/mbarkhau/pycalver
#
# Copyright (c) 2018 Manuel Barkhau (@mbarkhau) - MIT License
# SPDX-License-Identifier: MIT
#
# pycalver/vcs.py (this file) is based on code from the
# bumpversion project: https://github.com/peritus/bumpversion
# Copyright (c) 2013-2014 Filip Noetzel - MIT License
"""Minimal Git and Mercirial API.

If terminology for similar concepts differs between git and
mercurial, then the git terms are used. For example "fetch"
(git) instead of "pull" (hg) .
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import logging
import tempfile
import typing as typ
import subprocess as sp
log = logging.getLogger('pycalver.vcs')
VCS_SUBCOMMANDS_BY_NAME = {'git': {'is_usable': 'git rev-parse --git-dir',
    'fetch': 'git fetch', 'ls_tags': 'git tag --list v*', 'status':
    'git status --porcelain', 'add_path': 'git add --update {path}',
    'commit': 'git commit --file {path}', 'tag':
    'git tag --annotate {tag} --message {tag}', 'push_tag':
    'git push origin {tag}'}, 'hg': {'is_usable': 'hg root', 'fetch':
    'hg pull', 'ls_tags': 'hg tags', 'status': 'hg status -mard',
    'add_path': 'hg add {path}', 'commit': 'hg commit --logfile', 'tag':
    'hg tag {tag} --message {tag}', 'push_tag': 'hg push {tag}'}}


class VCS(object):
    """VCS absraction for git and mercurial."""

    def __init__(self, name, subcommands=None):
        self.name = name
        if subcommands is None:
            self.subcommands = VCS_SUBCOMMANDS_BY_NAME[name]
        else:
            self.subcommands = subcommands

    def __call__(self, cmd_name, env=None, **kwargs):
        """Invoke subcommand and return output."""
        cmd_str = self.subcommands[cmd_name]
        cmd_parts = cmd_str.format(**kwargs).split()
        output_data = sp.check_output(cmd_parts, env=env)
        _encoding = 'utf-8'
        return output_data.decode(_encoding)

    @property
    def is_usable(self):
        """Detect availability of subcommand."""
        cmd = self.subcommands['is_usable'].split()
        try:
            retcode = sp.call(cmd, stderr=sp.PIPE, stdout=sp.PIPE)
            return retcode == 0
        except OSError as e:
            if e.errno == 2:
                return False
            raise

    def fetch(self):
        """Fetch updates from remote origin."""
        self('fetch')

    def status(self):
        """Get status lines."""
        status_output = self('status')
        return [line[2:].strip() for line in status_output.splitlines() if 
            not line.strip().startswith('??')]

    def ls_tags(self):
        """List vcs tags on all branches."""
        ls_tag_lines = self('ls_tags').splitlines()
        log.debug('ls_tags output {0}'.format(ls_tag_lines))
        return [line.strip() for line in ls_tag_lines if line.strip().
            startswith('v')]

    def add(self, path):
        """Add updates to be included in next commit."""
        log.info('{0} add {1}'.format(self.name, path))
        self('add_path', path=path)

    def commit(self, message):
        """Commit added files."""
        log.info("{0} commit -m '{1}'".format(self.name, message))
        message_data = message.encode('utf-8')
        tmp_file = tempfile.NamedTemporaryFile('wb', delete=False)
        assert ' ' not in tmp_file.name
        with tmp_file as fh:
            fh.write(message_data)
        env = os.environ.copy()
        env['HGENCODING'] = 'utf-8'
        self('commit', env=env, path=tmp_file.name)
        os.unlink(tmp_file.name)

    def tag(self, tag_name):
        """Create an annotated tag."""
        self('tag', tag=tag_name)

    def push(self, tag_name):
        """Push changes to origin."""
        self('push_tag', tag=tag_name)

    def __repr__(self):
        """Generate string representation."""
        return "VCS(name='{0}')".format(self.name)


def get_vcs():
    """Detect the appropriate VCS for a repository.

    raises OSError if the directory doesn't use a supported VCS.
    """
    for vcs_name in VCS_SUBCOMMANDS_BY_NAME.keys():
        vcs = VCS(name=vcs_name)
        if vcs.is_usable:
            return vcs
    raise OSError('No such directory .git/ or .hg/ ')
