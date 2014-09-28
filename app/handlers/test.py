from app.handlers.base import BaseHandler
from app.exception.customexceptions import SessionExpired

__author__ = 'ashwin'


class TestHandler(BaseHandler):
    def get(self):
        raise SessionExpired
