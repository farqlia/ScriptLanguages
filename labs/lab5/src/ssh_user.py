import re
import datetime


class SSHUser:

    USERNAME_PATTERN = re.compile(r'^[a-z_][a-z0-9_-]{0,31}$')

    def __init__(self, username, last_login_date=datetime.datetime.now()):
        self.last_login_date = last_login_date
        self.username = username

    @classmethod
    def validate(cls, value):
        return re.search(SSHUser.USERNAME_PATTERN, value)
