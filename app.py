import os
from app.handlers.handlers import GetGameDataHandler, SetGameResultHandler
from app.handlers.home import HomeHandler

from app.handlers.test import TestHandler


__author__ = 'ashwin'

import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
from tornado.options import define, options
from tornado.web import url

define("port", default=8888, type=int)


class Application(tornado.web.Application):
    def __init__(self, *overrides):
        handlers = [
            url(r'/', HomeHandler),
            url(r'/a', TestHandler),
            url(r'/get_game_data', GetGameDataHandler),
            url(r'/set_game_result', SetGameResultHandler)
        ]

        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            'xsrf_cookies': False,
            'debug': True,
            'log_file_prefix': "tornado.log",
        }

        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
