import tornado
from tornado.web import RequestHandler

from app.exception.customexceptions import InternalError
from app.view.templates.json.base import JsonView


__author__ = 'ashwin'


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.add_header('Content-Type', 'application/json')

    def write_error(self, status_code, **kwargs):
        display_data = {'msg': 'Something went wrong'}
        error_code = 1001
        if 'exc_info' in kwargs:
            exception = kwargs['exc_info'][1]
            if isinstance(exception, InternalError):
                display_data = exception.display_data
                error_code = exception.error_code

        json_data = JsonView(display_data, error_code).render()
        self.finish(json_data)
