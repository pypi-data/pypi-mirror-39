import http.client
import urllib
import argparse
import os.path
import json


def argParse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--user_key', metavar='<string>', help='pushover user token')
    parser.add_argument('-t', '--app_token', metavar='<string>', help='pushover app token')

    return parser.parse_args()


class PushoverError(Exception): pass


class Pushover:
    def __init__(self, user=None, token=None, sound=None,
                 target=None, url=None, url_title=None,
                 title=None, priority=0, timestamp=None,
                 retry=None, expire=None,):
        self.url = url
        self.user = user
        self.sound = sound
        self.title = title
        self.token = token
        self.target = target
        self.priority = priority
        self.timestamp = timestamp
        self.url_title = url_title
        self.retry = retry
        self.expire = expire

    def sendMessage(self, message):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                     urllib.parse.urlencode({
                        "url": self.url,
                        "user": self.user,
                        "sound": self.sound,
                        "title": self.title,
                        "token": self.token,
                        "device": self.target,
                        "message": message,
                        "priority": self.priority,
                        "timestamp": self.timestamp,
                        "url_title": self.url_title,
                        "retry": self.retry,
                        "expire": self.expire,
                        }),
                     {"Content-type": "application/x-www-form-urlencoded"})
        output = conn.getresponse().read().decode('utf-8')
        data = json.loads(output)

        if data['status'] != 1:
            raise PushoverError(output)
        else:
            return True

        self.data = data

        return self


def main():
    args = argParse()

    userKeySet = args.user_key or args.user_key == ""
    appTokenSet = args.app_token or args.app_token == ""

    print(userKeySet)
    print(appTokenSet)

    if not userKeySet or not appTokenSet:
        # Handle this better... If not set, ask user.
        print("Set user key and token with -u and -t respectively.")
        print("Exiting...")
        exit()
    else:
        user = args.user_key
        token = args.app_token

    p = Pushover()
    p.user = user
    p.token = token
    p.title = os.path.basename(__file__)
    p.sendMessage("Testing pushover.py...")


if __name__ == '__main__':
    main()
