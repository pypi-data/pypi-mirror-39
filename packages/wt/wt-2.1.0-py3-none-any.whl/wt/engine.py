# -*- coding: utf-8 -*-

import os
import datetime
import itertools
import logging
from collections import OrderedDict
from pathlib import Path
from shutil import copytree, rmtree

import yaml
from cached_property import cached_property

from .base import Config, Content
from .jinja import get_env
from .exceptions import UrlNotFoundError, InvalidLocalLinkError
from .paginator import Paginator
from .html import HTMLParser, parse_link, is_local_link


class WT(object):

    def __init__(self, filename, is_prod=False):
        self.config_filename = filename
        self.workdir = os.path.dirname(filename)
        self.logger = logging.getLogger('wt.blog')
        self.is_prod = is_prod

        os.environ.setdefault('WT_WORKDIR', self.workdir)

        conf = None
        if os.path.isfile(filename):
            with open(filename, encoding='utf-8') as f:
                try:
                    conf = yaml.load(f)
                except yaml.YAMLError:
                    conf = {}
                    self.logger.error('Error parsing yaml', exc_info=True)
                else:
                    if not isinstance(conf, dict):
                        self.logger.error(
                            'Loaded config expected to be a dict,'
                            ' got "%s" instead', type(conf).__name__)
                        conf = {}
        else:
            self.logger.warning('Missing config file "%s"', filename)

        self.conf = Config(**(conf or {}))

    def conf_value(self, name, dflt=None):
        path = name.split('.')
        v = self.conf
        try:
            for part in path:
                v = getattr(v, part)
        except AttributeError:
            v = None
        return v in (self.conf, None) and dflt or v

    @cached_property
    def static_root(self):
        static_root = self.conf_value('directories.static', 'static')
        return os.path.join(self.workdir, static_root)

    @cached_property
    def pages_root(self):
        pages_root = self.conf_value('directories.pages',
                                     os.path.join('content', 'pages'))
        return os.path.join(self.workdir, pages_root)

    @cached_property
    def posts_root(self):
        posts_root = self.conf_value('directories.posts',
                                     os.path.join('content', 'posts'))
        return os.path.join(self.workdir, posts_root)

    @cached_property
    def with_feed(self):
        return self.conf_value('build.feed', True)

    @cached_property
    def verify_links(self):
        return self.conf_value('verify.links', False)

    @cached_property
    def baseurl(self):
        return getattr(self.conf, 'baseurl', '') if self.is_prod else ''

    def unbaseurl(self, url):
        if not self.is_prod or not self.baseurl:
            return url
        return url[len(self.baseurl):]

    @property
    def pages(self):
        pages_root, pages = self.pages_root, []
        if os.path.isdir(pages_root):
            pages = (Content(src=os.path.join(pages_root, x))
                     for x in os.listdir(pages_root))
        return {x.url: x for x in pages if x.url}

    @property
    def posts(self):
        posts_root, posts = self.posts_root, []
        if os.path.isdir(posts_root):
            posts = (Content(src=os.path.join(posts_root, x))
                     for x in os.listdir(posts_root))
        if self.is_prod:
            posts = (x for x in posts if not x.draft)
        posts = sorted(posts, key=lambda x: x.modified, reverse=True)
        dst = OrderedDict()
        _prev = None
        for idx, post in enumerate(posts):
            if idx > 0:
                post.next = _prev
                _prev.prev = post
            dst[post.url] = _prev = post
        return dst

    def paginator(self, posts, path='/'):
        return Paginator(posts, path, **self.conf.paginate)

    @cached_property
    def env(self):
        return get_env(self.workdir, self.baseurl, **self.conf.jinja)

    @cached_property
    def parser(self):
        return HTMLParser()

    @property
    def local_links(self):
        pages, posts = self.pages, self.posts
        links = list(
            itertools.chain(
                ['/'] if '/' not in pages else [],
                ['/atom.xml'] if self.with_feed else [],
                (x for x in self.paginator(list(posts.values())).pages.keys()
                 if x != '/'),
                pages.keys(),
                posts.keys(),
            ))
        return links

    def render_html(self, template, **context):
        tmpl = self.env.get_template(template)
        html = tmpl.render(**context)
        if self.verify_links:
            html = self.do_verify_links(html)
        return html

    def render(self, path, headers=None):
        headers = headers or {}
        host = headers.get('Host')
        now = datetime.datetime.utcnow()
        posts = self.posts
        pages = self.pages
        context = dict(config=self.conf,
                       host=host,
                       now=now,
                       is_prod=self.is_prod,
                       posts=posts.values(),
                       pages=pages.values())
        if path.endswith('atom.xml') and self.with_feed:
            tmpl = self.conf_value('templates.feed', 'atom.xml')
            return self.render_html(tmpl, **context)

        elif path in pages:
            page = pages[path]
            tmpl = (page.template or
                    self.conf_value('templates.page', 'page.html'))
            context['content'] = page
            return self.render_html(tmpl, **context)

        elif path in posts:
            post = posts[path]
            tmpl = (post.template or
                    self.conf_value('templates.post', 'post.html'))
            context['content'] = post
            return self.render_html(tmpl, **context)

        tmpl = self.conf_value('templates.mainpage', 'mainpage.html')
        paginator = self.paginator(list(posts.values()), path)
        if path == '/' or path in paginator.pages:
            context['paginator'] = paginator
            return self.render_html(tmpl, **context)

        raise UrlNotFoundError

    @cached_property
    def output_path(self):
        output = self.conf_value('build.output', 'output')
        output = Path(output)
        if not output.is_absolute():
            output = Path(self.workdir).joinpath(output)
        return output.expanduser()

    def build(self):
        build_static = self.conf_value('build.static', False)
        output = self.output_path
        self.logger.info('Building pages to %s directory', str(output))
        if output.exists():
            self.logger.info('  * output directory exists, cleaning')
            rmtree(str(output))
        if build_static:
            self.logger.info('  + copying static files')
            copytree(self.static_root, str(output))
        else:
            output.mkdir(parents=True)
        for path in self.local_links:
            self.logger.info('  + building path "%s"', path)
            html = self.render(path)
            if path.endswith('/'):
                path += 'index.html'
            target = output.joinpath(path.lstrip('/'))
            parent = target.parent
            parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html, encoding='utf-8')
        self.logger.info('done')

    def do_verify_links(self, html):

        links = self.parser.get_links(html)

        for link in links:
            parsed = parse_link(link)
            if is_local_link(parsed):
                path = self.unbaseurl(parsed.path)
                if not self.is_valid_local_link(path) and \
                        not self.is_valid_static_link(path):
                    # FIXME show line numbers?
                    # this is generated html - line numbers might not be useful
                    self.logger.warning('[!] Bad local link "%s" found', link)
                    if self.is_prod:
                        raise InvalidLocalLinkError
        return html

    def is_valid_local_link(self, link):
        return link in self.local_links

    def is_valid_static_link(self, link):
        return os.path.exists(os.path.join(self.static_root, link.lstrip('/')))
