import concurrent.futures
import threading

counter = 0
lock = threading.Lock()


def increment():
    global counter
    for _ in range(10):
        with lock:
            print('increment: ', threading.current_thread())
            counter += 1


def decrement():
    global counter
    for _ in range(10):
        with lock:
            print('decrement: ', threading.current_thread())
            counter -= 1


if __name__ == "__main__":

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as exe:
        exe.submit(increment)
        exe.submit(decrement)

    print(counter)