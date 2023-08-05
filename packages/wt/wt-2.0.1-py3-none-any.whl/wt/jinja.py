# -*- coding: utf-8 -*-

import os

import jinja2


class Registry(object):

    def __init__(self):
        self._functions = []

    def add(self, fn):
        self._functions.append(fn)
        return fn

    def __iter__(self):
        for fn in self._functions:
            yield fn


filters = Registry()
functions = Registry()


class Baseurl(object):
    __slots__ = ('baseurl', )

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def __call__(self, url):
        if not self.baseurl:
            return url
        return '{}{}'.format(self.baseurl, url)


def get_env(workdir, baseurl='', **config):
    loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader(
            os.path.join(workdir, 'templates')),
        jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates'))
    ])

    env = jinja2.Environment(loader=loader, **config)
    env.add_extension('jinja2.ext.autoescape')

    try:
        import jinja_helpers  # noqa
    except ImportError:
        pass

    for fn in filters:
        if not hasattr(fn, 'filter_name') and not hasattr(fn, '__name__'):
            raise ValueError(
                'Registered jinja filter must be a function '
                'or must have "filter_name" attribute')
        env.filters[getattr(fn, 'filter_name',
                            getattr(fn, '__name__', 'fltr'))] = fn

    for fn in functions:
        if not hasattr(fn, 'function_name') and not hasattr(fn, '__name__'):
            raise ValueError(
                'Registered jinja function must be a real function '
                'or must have "function_name" attribute')
        env.globals[getattr(fn, 'function_name',
                            getattr(fn, '__name__', 'func'))] = fn

    if 'baseurl' not in env.globals:
        env.globals['baseurl'] = Baseurl(baseurl)

    if 'markdown' not in env.globals:
        from .md import make_jinja_function

        md = make_jinja_function(baseurl)
        env.globals['markdown'] = md

    return env
