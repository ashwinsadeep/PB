import hashlib
import json
from random import randint
from time import sleep
import re
from tornado.web import HTTPError
from app.exception.customexceptions import InvalidInput, SessionExpired, InternalError
from app.handlers.base import BaseHandler, BaseAuthenticatedHandler
from app.handlers.sendpushnotification import PushNotificationHandler
from app.model.gamedata import GameDataModel
from app.model.user import UserModel
from app.view.templates.json.base import JsonView

__author__ = 'ashwin'


class GetGameDataHandler(BaseAuthenticatedHandler):
    def get(self, *args, **kwargs):
        raise HTTPError(405)

    def post(self, *args, **kwargs):
        data = dict()
        game_data_model = GameDataModel()
        tournament = game_data_model.get_games_from_active_tournament()
        if 'id' in tournament:
            data['tournament_data'] = tournament
            view = JsonView().set_data(data).render()
        else:
            view = JsonView().render()

        self.finish(view)


class SetGameResultHandler(BaseAuthenticatedHandler):
    def post(self, *args, **kwargs):
        if not self.current_user:
            raise SessionExpired

        result = self.get_argument('game_moves', None)
        # TODO: Write a validator for input validation
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
        view = JsonView({'api_access_key': 'Hkaiooiwe7#jiop8'}).render()
        self.finish(view)


class CreateSessionHandler(BaseHandler):
    def post(self, *args, **kwargs):
        email = self.get_argument('user_email', None)
        if not email:
            raise InvalidInput('user_email cannot be empty')

        user_model = UserModel()
        user_id = user_model.get_user_id_from_email(email)
        if not user_id:
            user_id = user_model.create_user_in_db(email)

        session = user_model.create_session(user_id)
        view = JsonView({'session': session}).render()
        self.finish(view)


class RegisterNotificationTokenHandler(BaseAuthenticatedHandler):
    def post(self, *args, **kwargs):
        notif_token = self.get_argument('notification_token', None)
        if not notif_token:
            raise InvalidInput('notification_token cannot be empty')

        user_model = UserModel()
        user_model.update_notification_token_for_user(notif_token, self.get_current_session())
        view = JsonView().render()
        self.finish(view)


class HttpNotFoundHandler(BaseHandler):
    def prepare(self):
        raise HTTPError(404)


class GetGameResultHandler(BaseAuthenticatedHandler):
    def post(self, *args, **kwargs):
        tournament_id = self.get_argument('tournament_id', None)
        if not tournament_id:
            raise InvalidInput('tournamen_id cannot be empty')

        result = {'rank': 12, 'total_players': 1658}
        view = JsonView(result).render()
        self.finish(view)


class PushNotificationTester(BaseAuthenticatedHandler):
    def post(self, *args, **kwargs):
        notif_token = self.get_argument('notification_token', None)
        color = self.get_argument('color', 'blue')
        alert = self.get_argument('alert', 'Some random string')
        badge_count = self.get_argument('badge_count', 1)
        has_content = self.get_argument('has_content', 0)
        if not notif_token:
            e = InvalidInput('notification_token')
            raise e

        notif_handler = PushNotificationHandler(notif_token)
        status = notif_handler.send_notification(alert, badge_count, color, has_content)
        if not status:
            e = InternalError(display_data=status)
            raise e

        view = JsonView().render()
        self.finish(view)


class DelayedResponseHandler(BaseHandler):
    def post(self, *args, **kwargs):
        delay = self.get_argument('delay', None)
        if not delay:
            raise InvalidInput('delay cannot be empty')

        sleep(float(delay))
        view = JsonView().render()
        self.finish(view)


class SubscibeInviteHandler(BaseHandler):
    def post(self, *args, **kwargs):
        email = self.get_argument('email', None)
        if not email:
            raise InvalidInput('email cannot be empty')

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise  InvalidInput('email is not valid')

        user_model = UserModel();
        user_model.insert_subscription_invite(email)
        view = JsonView()
        self.finish(view.render())