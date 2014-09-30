import hashlib
import time
from tornado.web import HTTPError
from app.exception.customexceptions import InvalidInput
from app.handlers.base import BaseHandler
from app.view.templates.json.base import JsonView

__author__ = 'ashwin'


class GetGameDataHandler(BaseHandler):
    def get(self, *args, **kwargs):
        raise HTTPError(405)

    def post(self, *args, **kwargs):
        post = self.get_argument('unique_user_id', None)
        if not post:
            e = InvalidInput()
            e.set_display_data('unique_user_id is not set')
            raise e
        data = dict()
        data['unique_key'] = hashlib.md5(post).hexdigest()
        data['games'] = []
        for x in xrange(1, 5):
            game_data = {'id': x,
                         'dimensions': [x, 10 - x],
                         'data': {'debug_data': 'This can be an array or json object or whatever we decide on.'}
            }
            data['games'].append(game_data)

        view = JsonView().set_data(data).render()
        self.finish(view)


class SetGameResultHandler(BaseHandler):
    def post(self, *args, **kwargs):
        uuid = self.get_argument('uuid', None)
        result = self.get_argument('result', None)
        if not uuid:
            e = InvalidInput()
            e.set_display_data('uuid is not set')
            raise e

        if not result:
            e = InvalidInput()
            e.set_display_data('result is not set')
            raise e

        view = JsonView().render()
        self.finish(view)
