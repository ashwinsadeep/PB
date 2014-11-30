import os
from apnsclient import *
import sys
import apnsclient

__author__ = 'ashwins'

class PushNotificationHandler:

    def __init__(self, notif_token):
        self.notif_toke = notif_token
        cert_file = os.path.join(os.path.dirname(__file__), '../../pushcert.pem')
        self.con = Session().new_connection('push_sandbox', cert_file=cert_file)

    def send_notification(self, alert, badge_count, color, has_content):
        message = Message(self.notif_toke, alert=alert, badge=badge_count, content_available=has_content, extra={'color':color})
        path = os.path.dirname(apnsclient.__file__)
        print path
        # Send the message.
        srv = APNs(self.con)
        try:
            res = srv.send(message)
        except:
            print(sys.exc_info())
            print "Can't connect to APNs, looks like network is down"
        else:
            # Check failures. Check codes in APNs reference docs.
            for token, reason in res.failed.items():
                code, errmsg = reason
                # according to APNs protocol the token reported here
                # is garbage (invalid or empty), stop using and remove it.
                print "Device failed: {0}, reason: {1}".format(token, errmsg)

            # Check failures not related to devices.
            for code, errmsg in res.errors:
                print "Error: {}".format(errmsg)

            # Check if there are tokens that can be retried
            if res.needs_retry():
                # repeat with retry_message or reschedule your task
                retry_message = res.retry()


notif_handler = PushNotificationHandler('cc85aa00960e2ec2e870826ae3ada3c3db250d65d4fe05924971e6e351402d5c')
notif_handler.send_notification('Random message',8,'blue',1)

