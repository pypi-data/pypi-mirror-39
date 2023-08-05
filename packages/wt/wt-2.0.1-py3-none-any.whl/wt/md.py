# -*- coding: utf-8 -*-

import markdown
from markdown.extensions import Extension
from markdown.extensions.extra import ExtraExtension
from markdown.extensions.toc import TocExtension
from markdown.treeprocessors import Treeprocessor

from .html import parse_link, is_local_link


class BaseurlTreeprocessor(Treeprocessor):

    def __init__(self, baseurl):
        self.baseurl = baseurl

    def run(self, root):
        if not self.baseurl:
            return
        attrs = ['href', 'src']
        for attr in attrs:
            for tag in root.findall('.//*[@%s]' % attr):
                link = tag.get(attr)
                parsed = parse_link(link)
                if is_local_link(parsed):
                    tag.set(attr, '{}{}'.format(self.baseurl, link))


class BaseurlExtension(Extension):

    def __init__(self, *args, **kwargs):
        self.config = {
            'baseurl': ['', 'baseurl wt configuration value']
        }
        super(BaseurlExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)
        proc = BaseurlTreeprocessor(self.getConfig('baseurl'))
        md.treeprocessors.register(proc, 'baseurl', 1)


class md(object):

    def __init__(self, **kwargs):
        self.md = markdown.Markdown(**kwargs)

    def __call__(self, text):
        return self.md.reset().convert(text)


def make_jinja_function(baseurl):

    extensions = [
        ExtraExtension(),
        TocExtension(permalink=True),
        BaseurlExtension(baseurl=baseurl),
    ]

    return md(extensions=extensions, output_format='html5')
