import re
import datetime
import labs.lab5.src.ssh_log_entry as ssh_log_entry


class SSHUser:

    USERNAME_PATTERN = re.compile(r'^[a-z_][a-z0-9_-]{0,31}$')

    def __init__(self, username, last_login_date=datetime.datetime.now()):
        self.last_login_date = last_login_date
        self.username = username

    @classmethod
    def validate(cls, value):
        return re.search(SSHUser.USERNAME_PATTERN, value)


if __name__ == "__main__":

    users = [SSHUser("zuri2"), SSHUser("root"), SSHUser("****")]
    logs = [ssh_log_entry.AcceptedPassword("Dec 12 14:20:38 LabSZ sshd[29040]: Accepted password for curi from 137.189.88.215 port 33299 ssh2"),
            ssh_log_entry.FailedPassword("Dec 14 04:31:27 LabSZ sshd[8027]: Failed password for root from 180.101.249.16 port 54864 ssh2"),
            ssh_log_entry.Error("Dec 17 05:17:45 LabSZ sshd[25192]: error: Received disconnect from 103.99.0.122: 14: No more user authentication methods available. [preauth]"),
            ssh_log_entry.Other("Jan  3 18:16:11 LabSZ sshd[5514]: PAM service(sshd) ignoring max retries; 6 > 3")]

    logs[0].port = 0
    logs[1].user = "julia"
    logs[2].cause = "input_userauth_request: invalid user wangj [preauth]"
    logs[3].date = datetime.datetime.now()

    for entry in logs:
        print(entry.validate())
