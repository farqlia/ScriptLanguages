import threading
from datetime import datetime


class MyOwnThread(threading.Thread):

    def run(self) -> None:
        print(f"{datetime.now(): %Y-%m-%d %H:%M}")


if __name__ == "__main__":
    print("Main thread starting")
    thread = MyOwnThread()
    thread.start()
    thread.join()
    print("Main continue")