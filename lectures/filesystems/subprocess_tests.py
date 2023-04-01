from subprocess import Popen, PIPE


def piped_process():

    process = Popen(["date", "/T"], stdin=PIPE, stdout=PIPE, text=True, shell=True)

    assert "Sat 04/01/2023" == process.stdout.readline().strip()


if __name__ == "__main__":

    piped_process()