# -*- coding: utf-8 -*-

import os
import sys
import glob
import itertools
import logging
import multiprocessing as mp
import time
import subprocess
import string
import traceback
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler

from .exceptions import UrlNotFoundError
from . import utils

logger = logging.getLogger(__name__)

SERVER_ERROR = string.Template(
    """
    <html>
    <head>
    <title>Server Error (500)</title>
    </head>
    <body>
    <h3>${title}</h3>
    <pre>${error}</pre>
    </body>
    </html>
    """
)


class Server(HTTPServer):  # pragma: no cover

    def __init__(self, config, *args, **kwargs):
        self.engine = utils.engine(config)
        os.chdir(self.engine.static_root)
        super().__init__(*args, **kwargs)


class Handler(SimpleHTTPRequestHandler):  # pragma: no cover

    def do_GET(self):
        engine = self.server.engine
        try:
            try:
                content = engine.render(self.path, self.headers)
            except UrlNotFoundError:
                super().do_GET()
            else:
                self.send_content(HTTPStatus.OK, content)
        except Exception as exc:
            logger.error('Error rendering page', exc_info=True)
            content = traceback.format_exc()
            content = SERVER_ERROR.substitute(error=content, title=str(exc))
            self.send_content(HTTPStatus.INTERNAL_SERVER_ERROR, content)

    def send_error(self, code, message=None, explain=None):
        if code == HTTPStatus.NOT_FOUND:
            engine = self.server.engine
            content = engine.render_html('404.html')
            self.send_content(code, content)
        else:
            super().send_error(code, message=message, explain=explain)

    def send_content(self, code, content):
        content = content.encode('utf-8')
        size = len(content)

        path = self.path.split('?')[0]
        path = path.split('#')[0]
        base, ext = os.path.splitext(path)
        ct = {
            '.xml': 'text/xml',
            '.txt': 'text/plain'
        }
        ct = ct.get(ext.lower(), 'text/html')
        ct += ';charset=utf-8'

        self.log_request(code=code, size=size)
        self.send_response_only(code)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())
        self.send_header('Content-Type', ct)
        self.send_header('Content-Length', size)
        self.send_header('Last-Modified', self.date_time_string())
        self.end_headers()
        self.wfile.write(content)


def code_changed(workdir):  # pragma: no cover
    mtime = time.time()
    wtdir = os.path.abspath(os.path.dirname(__file__))

    while True:
        wtfiles = glob.iglob(os.path.join(wtdir, '**', '*.py'), recursive=True)
        files = glob.iglob(os.path.join(workdir, '**', '*.py'), recursive=True)
        changed = False
        for fn in itertools.chain(wtfiles, files):
            if not os.path.exists(fn):
                continue
            _mtime = os.stat(fn).st_mtime
            if _mtime > mtime:
                mtime = _mtime
                changed = True
                break
        yield changed


def redirect_stdout(stdout):  # pragma: no cover
    while True:
        try:
            data = os.read(stdout.fileno(), 2**15)
        except KeyboardInterrupt:
            break
        if len(data) > 0:
            sys.stdout.write(data.decode('utf-8'))


def server(config, host, port):  # pragma: no cover
    logger = logging.getLogger('wt.server')

    if os.environ.get('IS_WT_CHILD') == 'yes':
        address = (host, port)
        httpd = Server(config, address, Handler)
        logger.debug('Server started at %s:%s...', host, port)
        httpd.serve_forever()

    checker = code_changed(os.path.dirname(config))

    def run():
        env = os.environ.copy()
        env['IS_WT_CHILD'] = 'yes'
        env['PYTHONUNBUFFERED'] = 'yes'
        p = subprocess.Popen(sys.argv[:],
                             env=env,
                             universal_newlines=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        t = mp.Process(target=redirect_stdout, args=(p.stdout,))
        t.start()
        return p, t

    p, t = run()

    try:
        while True:
            if next(checker):
                logger.debug('some python code changed, restarting server...')
                t.terminate()
                time.sleep(0.1)
                p.terminate()
                time.sleep(0.3)
                p, t = run()
            time.sleep(0.3)
    except KeyboardInterrupt:
        p.terminate()
    return 0
