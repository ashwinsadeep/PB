import hashlib
import json
from random import randint
from tornado.web import HTTPError
from app.exception.customexceptions import InvalidInput, SessionExpired, InternalError
from app.handlers.base import BaseHandler
from app.model.gamedata import GameDataModel
from app.model.user import UserModel
from app.view.templates.json.base import JsonView

__author__ = 'ashwin'


class GetGameDataHandler(BaseHandler):
    def get(self, *args, **kwargs):
        raise HTTPError(405)

    def post(self, *args, **kwargs):
        user_email = self.get_argument('user_email', None)
        if (not user_email) and (not self.current_user):
            e = InvalidInput()
            e.set_display_data('user_email is not set')
            raise e

        data = dict()
        # User id was not set at this point, means this is a new user or a returning user without session
        if not self.current_user:
            user_model = UserModel()
            user_id = user_model.get_user_id_from_email(user_email)
            print(user_id)
            # For returning user, create session
            if user_id is not None:
                data['session'] = user_model.create_session(user_id)
                self.current_user = user_id
            # Create a new user if not a returning user
            else:
                self.current_user = user_model.create_user_in_db(user_email)
                data['session'] = user_model.create_session(self.current_user)

        game_data_model = GameDataModel()
        tournament = game_data_model.get_games_from_active_tournament()
        if 'id' in tournament:
            data['tournament_data'] = tournament
            view = JsonView().set_data(data).render()
        else:
            view = JsonView().render()

        print(view)
        self.finish(view)


class SetGameResultHandler(BaseHandler):
    def post(self, *args, **kwargs):
        if not self.current_user:
            raise SessionExpired

        result = self.get_argument('game_moves', None)
        if not result:
            e = InvalidInput()
            e.set_display_data('game_moves was not set')
            raise e

        result = json.loads(result)
        game_data_model = GameDataModel()
        for game_result in result:
            try:
                game_id = game_result['game_id']
                game_moves = game_result['moves']
                game_score = game_result['score']
            except KeyError:
                raise InvalidInput('game_moves didn\'t have the necessary keys')

            game_data_model.set_game_moves(self.current_user, game_id, game_moves, game_score)

        view = JsonView().render()
        self.finish(view)


class GetApiAccessKeyHandler(BaseHandler):
    def get(self, *args, **kwargs):
        view = JsonView({'api_access_key':'Hkaiooiwe7#jiop8'}).render()
        self.finish(view)

