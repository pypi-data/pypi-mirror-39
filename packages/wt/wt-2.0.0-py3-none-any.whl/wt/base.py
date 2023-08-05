# -*- coding: utf-8 -*-

import os
import re
import datetime
import logging

from string import Template

import yaml

from .decorators import reloadable


logger = logging.getLogger('wt.base')
fm_re = re.compile(r'^---$', re.MULTILINE)


@reloadable('(re)loading nested configuration...')
def load_yaml(filename):
    with open(filename, encoding='utf-8') as f:
        data = list(yaml.load_all(f))
    return data[0] if len(data) == 1 else data


@reloadable('(re)loading content...')
def load_content(filename):
    fm, text = {}, ''
    if os.path.isfile(filename):
        with open(filename, 'rt', encoding='utf-8') as f:
            text = f.read()
        if len(fm_re.findall(text)) >= 2:
            _, fm, text = fm_re.split(text, maxsplit=2)
            fm = yaml.safe_load(fm)
    return (fm, text)


def transform(value):
    conv = {
        list: process_list,
        dict: dict_to_object,
        str: lambda x: process_str_file(process_str_env(x)),
    }
    return conv.get(type(value), lambda x: x)(value)


def dict_to_object(obj):
    return Object(**obj)


def process_list(obj):
    return [isinstance(x, dict) and Object(**x) or x for x in obj]


def process_str_env(value):
    return Template(value).safe_substitute(**os.environ)


def process_str_file(value):
    if value[:6] == '{file}':
        workdir = os.environ.get('WT_WORKDIR', '')
        v = load_yaml(os.path.join(workdir, value[6:]))
        return transform(v)
    return value


class Object(object):

    __slots__ = ('_kwargs', )

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __getattr__(self, name):
        return transform(self._kwargs.get(name))


class Config(Object):

    def __getattr__(self, name):
        if name in ('paginate', 'jinja'):
            return self._kwargs.get(name, {})
        return super().__getattr__(name)


class Content(Object):

    __slots__ = ('next', 'prev')

    @property
    def text(self):
        txt = ''
        src = self._kwargs.get('src')
        if src is not None:
            _, txt = load_content(src)
        if not txt:
            logger.warning('  ! missing content file "%s"', src)
        return txt.strip()

    def __getattr__(self, name):
        if 'src' in self._kwargs:
            src = self._kwargs['src']
            fm, _ = load_content(src)
            if name in fm:
                return fm[name]
            if name == 'modified':
                return self.mtime
        return super().__getattr__(name)

    @property
    def mtime(self):
        if 'src' in self._kwargs:
            src = self._kwargs['src']
            if os.path.exists(src):
                mtime = os.stat(src).st_mtime
                return datetime.datetime.fromtimestamp(mtime)
