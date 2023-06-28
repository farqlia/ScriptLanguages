import multiprocessing, time

queue = multiprocessing.Queue()


def produce():
    n = 0
    while True:
        n += 1
        print("put: ", n + 1)
        queue.put(n + 1)
        time.sleep(2)


def consume():
    while True:
        num = queue.get()
        print(num)


if __name__ == "__main__":
    multiprocessing.Process(target=produce).start()
    multiprocessing.Process(target=consume).start()
    # multiprocessing.Process(target=consume).start()