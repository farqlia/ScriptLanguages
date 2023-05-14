import datetime
import re


class SSHUser:

    USERNAME_PATTERN = re.compile(r'^[a-z_][a-z0-9_-]{0,31}$')

    def __init__(self, username, last_login_date=datetime.datetime.now()):
        self.last_login_date = last_login_date
        self.username = username

    def validate(self):
        return re.search(SSHUser.USERNAME_PATTERN, self.username) is not None

    def __repr__(self):
        return self.username