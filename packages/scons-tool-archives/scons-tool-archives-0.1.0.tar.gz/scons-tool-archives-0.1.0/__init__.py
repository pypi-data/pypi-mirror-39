# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 by Pawel Tomulik <ptomulik@meil.pw.edu.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

from __future__ import absolute_import

__docformat__ = "restructuredText"

from .about import __version__

import os
import re
import tarfile
import zipfile
import SCons.Builder


_tarfile_modes =  [
    ('.tar', 'w'),
    ('.tar.gz', 'w:gz'),
    ('.tgz', 'w:gz'),
    ('.tar.bz2', 'w:bz2'),
    ('.tbz2', 'w:bz2'),
    ('.tar.xz', 'w:xz'),
    ('.txz', 'w:xz')
]


_sep = ''.join(set([os.path.sep, '/']))
_sep_re = re.compile('(?:[%s]+)' % re.escape(_sep))


def _split_path(path, strip=True):
    if strip:
        path = path.rstrip(_sep)
    return _sep_re.split(path)


def _apply_path_mapping(path, map_from, map_to):
    path = _split_path(path, False)
    map_from = _split_path(map_from)
    if(len(path) < len(map_from) or map_from != path[:len(map_from)]):
        return None
    if map_to:
        map_to = _split_path(map_to)
    else:
        map_to = []
    return '/'.join(map_to + path[len(map_from):])


def _apply_path_mappings(path, mapitems):
    for map_from, map_to in mapitems:
        mapped = _apply_path_mapping(path, map_from, map_to)
        if mapped:
            return mapped
    return '/'.join(_split_path(path, False))


def _map_path(path, mappings):
    if isinstance(mappings, str):
        mapitems = ((p, None) for p in mappings.split(os.path.pathsep))
    elif isinstance(mappings, (list, tuple)):
        mapitems = ((p, None) if isinstance(p, str) else p for p in mappings)
    elif isinstance(mappings, dict):
        mapitems = mappings.items()
    elif mappings:
        mapitems = mappings
    else:
        mapitems = []
    return _apply_path_mappings(path, mapitems)


def _bool(arg, default):
    try:
        return bool(int(arg))
    except ValueError:
        if str(arg).lower() in ('true', 'yes', 'y', 'on'):
            return True
        elif str(arg).lower() in ('false', 'no', 'n', 'off'):
            return False
        else:
            return default


def _bool_f(arg):
    return _bool(arg, False)


def _bool_t(arg):
    return _bool(arg, True)


def _arcname(name, env, builder_name):
    transform = env.get('%sTRANSFORM' % builder_name.upper())
    if transform and callable(transform):
        return transform(name, env)
    return _map_path(name, env.get('%sMAPPINGS' % builder_name.upper()))


def _mode(target, env, builder_name, suffix_modes=(), default='w'):
    mode = env.subst('$%sMODE' % builder_name.upper())
    if mode:
        return mode
    for suffix, mode in suffix_modes:
        if target.lower().endswith(suffix):
            return mode
    return default


def _tar_format(arg):
    if isinstance(arg, str):
        if arg.upper().endswith('_FORMAT'):
            return getattr(tarfile, arg.upper())
        else:
            return getattr(tarfile, "%s_FORMAT" % arg.upper())
    else:
        return arg


def _zip_compression(arg):
    if isinstance(arg, str):
        if arg.upper().startswith('ZIP_'):
            return getattr(zipfile, arg.upper())
        else:
            return getattr(zipfile, 'ZIP_%s' % arg.upper())
    else:
        return arg


def _tar_kwargs(env):
    kwargs = [('bufsize', 'TARFILEBUFSIZE', int),
              ('compresslevel', 'TARFILECOMPRESSLEVEL', int),
              ('format', 'TARFILEFORMAT',_tar_format),
              ('dereference', 'TARFILEDEREFERENCE',_bool_f),
              ('debug', 'TARFILEDEBUG', int),
              ('encoding', 'TARFILEENCODING', str),
              ('errors', 'TARFILEERRORS', str)]
    return {k: f(env.subst("$%s" % e)) for k, e, f in kwargs if e in env}


def _zip_kwargs(env):
    kwargs = [('compression', 'ZIPFILECOMPRESSION', _zip_compression),
              ('allowZip64', 'ZIPFILEALLOW64', _bool_t),
              ('compresslevel', 'ZIPFILECOMPRESSLEVEL', int)]
    return {k: f(env.subst("$%s" % e)) for k, e, f in kwargs if e in env}


def TarFile(target, source, env):
    tgt = str(target[0])
    mode = _mode(tgt, env, 'TarFile', _tarfile_modes)
    with tarfile.open(tgt, mode, **_tar_kwargs(env)) as f:
        for src in map(str, source):
            f.add(src, _arcname(src, env, 'TarFile'))


def ZipFile(target, source, env):
    tgt = str(target[0])
    mode = _mode(tgt, env, 'ZipFile')
    with zipfile.ZipFile(tgt, mode, **_zip_kwargs(env)) as f:
        for src in map(str, source):
            f.write(src, _arcname(src, env, 'ZipFile'))


def createTarFileBuilder(env):
    try:
        builder = env['BUILDERS']['TarFile']
    except KeyError:
        builder = SCons.Builder.Builder(action=TarFile,
                                        suffix='$TARFILESUFFIX',
                                        multi=1)
        env['BUILDERS']['TarFile'] = builder
    return builder


def createZipFileBuilder(env):
    try:
        builder = env['BUILDERS']['ZipFile']
    except KeyError:
        builder = SCons.Builder.Builder(action=ZipFile,
                                        suffix='$ZIPFILESUFFIX',
                                        multi=1)
        env['BUILDERS']['ZipFile'] = builder
    return builder


def generate(env):
    createTarFileBuilder(env)
    createZipFileBuilder(env)
    env.SetDefault(TARFILESUFFIX='.tar')
    env.SetDefault(ZIPFILESUFFIX='.zip')

def exists(env):
    return 1

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
