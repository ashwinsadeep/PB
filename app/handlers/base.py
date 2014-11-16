import pprint
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
        # If the request is to fetch API access key, no need to check anything else
        if self.request.uri.find('get_api_access_key') != -1:
            return

        # In all other cases, validate api access key
        api_access_key = self.request.headers.get('X-Pb-Api-Access-Key')
        if (api_access_key is None) or (api_access_key != '164ad454785aa19e1b5e15888c9dc210'):
            raise ApiAccessDenied

    def get_current_user(self):
        user_session = self.request.headers.get('X-Pbsession')
        user_model = UserModel()
        user_id = user_model.get_user_id_from_session(user_session)
        return user_id


class BaseAuthenticatedHandler(BaseHandler):
    # Authenticated request. Has to have a valid session. If not, cry!
    def prepare(self):
        super(BaseAuthenticatedHandler, self).prepare()
        if not self.current_user:
            raise SessionExpired

    def get_current_session(self):
        return self.request.headers.get('X-Pbsession')