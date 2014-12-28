import os
from app.handlers.base import BaseHandler
from app.handlers.handlers import GetGameDataHandler, SetGameResultHandler, GetApiAccessKeyHandler, CreateSessionHandler, \
    RegisterNotificationTokenHandler, HttpNotFoundHandler, GetGameResultHandler, PushNotificationTester, \
    DelayedResponseHandler


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
            url(r'/get_game_data', GetGameDataHandler),
            url(r'/set_game_result', SetGameResultHandler),
            url(r'/get_api_access_key', GetApiAccessKeyHandler),
            url(r'/session_create', CreateSessionHandler),
            url(r'/register_notification_token', RegisterNotificationTokenHandler),
            url(r'/get_tournament_result', GetGameResultHandler),
            url(r'/send_notification', PushNotificationTester),
            url(r'/delayed_response', DelayedResponseHandler),
            url(r'/(.*)', HttpNotFoundHandler)
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
