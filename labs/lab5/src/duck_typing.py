import ipaddress
from datetime import datetime

import labs.lab5.src.ssh_log_entry as ssh_log_entry
import labs.lab5.src.ssh_log_journal as ssh_log_journal
from labs.lab5.src.ssh_user import SSHUser


if __name__ == "__main__":

    users = [SSHUser("zuri2"), SSHUser("root"), SSHUser("****")]

    raw_entries = [
        "Jan  3 18:16:11 LabSZ sshd[5514]: PAM service(sshd) ignoring max retries; 6 > 3",
        "Dec 14 04:31:27 LabSZ sshd[8027]: Failed password for root from 180.101.249.16 port 54864 ssh2",
        "Dec 17 05:17:45 LabSZ sshd[25192]: error: Received disconnect from 103.99.0.122: 14: No more user authentication methods available. [preauth]",
        "Dec 12 14:20:38 LabSZ sshd[29040]: Accepted password for curi from 137.189.88.215 port 33299 ssh2",
        "Dec 10 09:32:20 LabSZ sshd[24680]: Accepted password for fztu from 119.137.62.142 port 49116 ssh2",
        "Dec 13 11:00:22 LabSZ sshd[5459]: Accepted password for zachary from 218.17.80.182 port 50313 ssh2",
        "Jan  2 16:14:25 LabSZ sshd[8223]: Accepted password for curi from 61.187.54.9 port 17206 ssh2"

    ]

    accepted_ssh_log_journal = ssh_log_journal.AcceptedPasswordJournal()

    for log in raw_entries:
        print(accepted_ssh_log_journal.append(log))

    for log in accepted_ssh_log_journal:
        print(log)

    more_than_200_addresses = accepted_ssh_log_journal[ipaddress.IPv4Address("200.0.0.0"):]
    less_than_100_address = accepted_ssh_log_journal[:ipaddress.IPv4Address("100.0.0.0")]

    print("more_than_200_addresses = ", more_than_200_addresses)
    print("less_than_100_address = ", less_than_100_address)

    accepted_ssh_log_journal[1].user = "julia"
    accepted_ssh_log_journal[3].date = datetime.now()

    container = [item for l in [more_than_200_addresses, less_than_100_address, users] for item in l]

    print("\nValidate entries")

    for entry in container:
        print(entry, entry.validate())
