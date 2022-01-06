import threading


# a1 < b2 && b1 < a2
a1_done = threading.Semaphore(0)
b1_done = threading.Semaphore(0)


def worker_a() -> None:
    print('a1')
    a1_done.release()
    b1_done.acquire()
    print('a2')


def worker_b() -> None:
    print('b1')
    b1_done.release()
    a1_done.acquire()
    print('b2')


def main() -> None:
    thread_a = threading.Thread(target=worker_a)
    thread_b = threading.Thread(target=worker_b)

    thread_a.start()
    thread_b.start()

    thread_a.join()
    thread_b.join()


if __name__ == '__main__':
    main()
