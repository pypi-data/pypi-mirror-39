# -*- coding: utf-8 -*-

import logging
from pathlib import Path
from shutil import copyfile

from .decorators import reloadable
from .engine import WT


@reloadable('(re)loading configuration...')
def engine(fn):  # pragma: no cover
    return WT(fn)


def build(fn):  # pragma: no cover
    b = WT(fn, is_prod=True)
    try:
        b.build()
    except Exception as exc:
        logger = logging.getLogger('wt.build')
        logger.error('Error while building', exc_info=exc)
        return 1
    else:
        return 0


def init(path):
    src = Path(__file__).parent
    dst = Path(path)

    logger = logging.getLogger('wt.init')

    to_copy = (
        (['fixtures', 'wt.yaml'], ['wt.yaml']),
        (['fixtures', 'foo.md'], ['content', 'pages', 'foo.md']),
        (['fixtures', 'bar.md'], ['content', 'posts', 'bar.md']),
        (['fixtures', 'baz.md'], ['content', 'posts', 'baz.md']),
        (['fixtures', 'style.css'], ['static', 'css', 'style.css']),
        (['fixtures', 'logo96.png'], ['static', 'img', 'logo96.png']),
        (['templates', 'atom.xml'], ['templates', 'atom.xml']),
        (['templates', 'content.html'], ['templates', 'content.html']),
        (['templates', 'mainpage.html'], ['templates', 'mainpage.html']),
    )

    for from_, to_ in to_copy:
        left = src.joinpath(*from_)
        right = dst.joinpath(*to_)
        if not left.exists():  # pragma: no cover
            logger.warning('[!] missing file "%s", skipping', str(left))
            continue
        if right.exists():  # pragma: no cover
            logger.warning('[!] target file "%s" exists, skipping', str(right))
            continue
        if not right.parent.exists():
            right.parent.mkdir(parents=True)
        copyfile(str(left), str(right))
        logger.info('[+] "%s" created', str(right))

    logger.info('[+] done')

    return 0
