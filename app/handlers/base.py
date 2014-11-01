import tornado
from tornado.web import RequestHandler

from app.exception.customexceptions import InternalError, ApiAccessDenied, SessionExpired
from app.model.user import UserModel
from app.view.templates.json.base import JsonView


__author__ = 'ashwin'


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.add_header('Content-Type', 'application/json')

    # Uncaught exceptions will be handled here
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

    # Validate session and API keys for every request
    def prepare(self):
        api_access_key = self.request.headers.get('X-Pb-Api-Access-Key')
        if (api_access_key is None) or (api_access_key != 'api-access-key'):
            raise ApiAccessDenied

        # If the session header is set, validate it. Otherwise ignore this step, this might be an unauthenticated
        # request.
        user_session = self.request.headers.get('X-Pbsession')
        if (user_session is not None) and (self.current_user is None):
            raise SessionExpired

    def get_current_user(self):
        user_session = self.request.headers.get('X-Pbsession')
        user_model = UserModel()
        user_id = user_model.get_user_id_from_session(user_session)
        return user_id