from logging import Logger
from tornado import options, log
from tornado.options import define
import torndb

__author__ = 'ashwins'


class GameDataModel:

    def save_unique_user_id(self, identifier, unique_key, game_ids):
        db = torndb.Connection('127.0.0.1', 'pixelbot', user='root', password='EnzeN9AdugodI')
        for game_id in game_ids:
            game_id = int(game_id)
            print(game_id)
            db.insert('INSERT INTO pb_user_game_data (_identifier, _unique_key, _game_id) VALUES (%s, %s, %s)', identifier, unique_key, game_id)

