import multiprocessing


def worker_process(n, accuracy):
    guess = n / 2
    for _ in range(accuracy):
        guess = 0.5 * (guess + n / guess)


if __name__ == "__main__":
    for num in [5, 10, 20, 30, 60, 100]:
        proc = multiprocessing.Process(target=worker_process, args=(num, 1000000))
        proc.start()
