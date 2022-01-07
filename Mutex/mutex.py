import threading


count = 0
mutex = threading.Semaphore(1)

# provide large enough cycle number because of GIL
CYCLE = 1_000_000

def worker_a() -> None:
    global count

    for _ in range(CYCLE):
        mutex.acquire()
        count = count + 1
        mutex.release()

def worker_b() -> None:
    global count

    for _ in range(CYCLE):
        mutex.acquire()
        count = count + 1
        mutex.release()


def main() -> None:
    thread_a = threading.Thread(target=worker_a)
    thread_b = threading.Thread(target=worker_b)

    thread_a.start()
    thread_b.start()

    thread_a.join()
    thread_b.join()

    print(count)
    try:
        assert count == CYCLE * 2
    except AssertionError:
        print('Threads access shared variable `count` at the same time.')
    else:
        print('Is mutual exclusive.')


if __name__ == '__main__':
    main()
