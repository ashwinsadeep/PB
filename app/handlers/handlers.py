import hashlib
from random import randint
from tornado.web import HTTPError
from app.exception.customexceptions import InvalidInput
from app.handlers.base import BaseHandler
from app.model.gamedata import GameDataModel
from app.view.templates.json.base import JsonView

__author__ = 'ashwin'


class GetGameDataHandler(BaseHandler):
    def get(self, *args, **kwargs):
        raise HTTPError(405)

    def post(self, *args, **kwargs):
        unique_user_id = self.get_argument('unique_user_id', None)
        if not unique_user_id:
            e = InvalidInput()
            e.set_display_data('unique_user_id is not set')
            raise e
        data = dict()
        data['unique_key'] = hashlib.md5(unique_user_id).hexdigest()
        data['games'] = []
        for count in xrange(1, 5):
            x = count
            y = 10-count
            game_data = {'id': count,
                         'dimensions': [x, y],
                         'data': self._get_randomly_generated_array(x*y)
            }
            data['games'].append(game_data)

        game_data_model = GameDataModel()
        game_data_model.save_unique_user_id(unique_user_id, data['unique_key'], [1, 2])
        view = JsonView().set_data(data).render()
        self.finish(view)
        
    def _get_randomly_generated_array(self,size):
        possible_values = [0, 1, 2]
        random_array = []
        for count in xrange(0, size):
            random_number = randint(0, 2)
            random_array.append(possible_values[random_number])

        return random_array


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
