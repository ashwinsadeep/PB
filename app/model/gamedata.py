from logging import Logger
import datetime
from tornado import options, log
from tornado.options import define
import torndb

__author__ = 'ashwins'


class GameDataModel:

    def __init__(self):
        self.db = torndb.Connection('pb-production.cyxvzxlxcukg.us-east-1.rds.amazonaws.com', 'pixelbot', user='root', password='EnzeN9AdugodI')
        # self.db = torndb.Connection('127.0.0.1', 'pixelbot', user='root', password='EnzeN9AdugodI')

    def get_games_from_active_tournament(self):
        # This whole function is horribly convoluted, so that we get all the required data in one query.
        # Once we can afford a bigger RDS instance, fetch the latest active tournament and find the games for it.
        # That'll be much more readable
        active_games = self.db.query('SELECT _tournament_id as tournament_id,'
                                     'pb_game._id as game_id,'
                                     'pb_game._data as game_data,'
                                     'pb_game._rows as rows,'
                                     'pb_game._columns as columns,'
                                     'unix_timestamp(pb_tournament._ts_end) as ts_expiry '
                                     'FROM pb_tournament INNER JOIN pb_game '
                                     'ON pb_tournament._id = pb_game._tournament_id '
                                     'WHERE pb_tournament._is_active = 1 '
                                     'ORDER BY pb_tournament._id DESC')

        tournament_data = dict()
        games = list()
        for game in active_games:
            # Got a game from a different tournament. Only one is supposed to be active at any given time
            try:
                if tournament_id != game['tournament_id']:
                    break
            # If exception, it means tournament_id was not yet initialized, no issues, go ahead and assign it
            # for the first time
            except NameError:
                tournament_id = game['tournament_id']

            ts_expiry = game['ts_expiry']
            temp_game = dict()
            temp_game['id'] = game['game_id']
            temp_game['rows'] = game['rows']
            temp_game['columns'] = game['columns']
            temp_game['data'] = game['game_data']
            games.append(temp_game)

        try:
            tournament_data['id'] = tournament_id
            tournament_data['ts_expiry'] = ts_expiry
        except NameError:
            return tournament_data

        tournament_data['games'] = games
        return tournament_data

    def set_game_moves(self, user_id, game_id, game_moves, score):
        user_id = int(user_id)
        self.db.execute_lastrowid('INSERT INTO pb_game_move (_game_id, _user_id, _game_moves, _ts_created, _score) '
                                  'VALUES (%s, %s, %s, NOW(), %s) ON DUPLICATE KEY UPDATE '
                                  '_game_moves = %s, '
                                  '_score = %s, '
                                  '_ts_created = NOW()', game_id, user_id, game_moves, score, game_moves, score)