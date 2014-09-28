from app.handlers.base import BaseHandler

__author__ = 'ashwin'


class HomeHandler(BaseHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write('ASF')
