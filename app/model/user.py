import base64
import M2Crypto
import torndb

__author__ = 'ashwins'
class UserModel:

    def __init__(self):
        self.db = torndb.Connection('pb-production.cyxvzxlxcukg.us-east-1.rds.amazonaws.com', 'pixelbot', user='root', password='EnzeN9AdugodI', connect_timeout=5)
        # self.db = torndb.Connection('127.0.0.1', 'pixelbot', user='root', password='EnzeN9AdugodI', connect_timeout=5)

    def get_user_id_from_session(self, session):
        user_id = self.db.get('SELECT _user_id from pb_user_session WHERE _session_hash = MD5(%s)', session)
        if not user_id:
            return None

        return user_id['_user_id']

    def get_user_id_from_email(self, email):
        user_id = self.db.get('SELECT _id from pb_user WHERE _unique_id = %s', email)
        if not user_id:
            return None

        return user_id['_id']

    def create_user_in_db(self, user_email):
        user_id = self.db.execute_lastrowid('INSERT INTO pb_user (_unique_id, _ts_created) VALUES (%s, NOW())',
                                            user_email)
        return user_id

    def create_session(self, user_id):
        user_id = int(user_id)
        session = self.generate_session_id()
        self.db.execute_lastrowid('INSERT INTO pb_user_session(_user_id, _session_hash, _ts_created) '
                                  'VALUES (%s, MD5(%s), NOW())', user_id, session)
        return session

    def generate_session_id(self):
        return base64.b64encode(M2Crypto.m2.rand_bytes(16))

    def update_notification_token_for_user(self, notification_token, session):
        self.db.execute('INSERT INTO pb_device_notification(_session_hash, _notification_token) '
                        'VALUES (MD5(%s), %s) ON DUPLICATE KEY UPDATE _notification_token = %s',
                        session, notification_token, notification_token)

    def insert_subscription_invite(self, email):
        self.db.execute('INSERT INTO pb_subscribe_invite(_email) VALUES (%s)', email)