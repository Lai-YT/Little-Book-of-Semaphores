import logging
import threading


logging.basicConfig(format='%(message)s', level=logging.INFO)


# a1 < b2 && b1 < a2
a1_done = threading.Semaphore(0)
b1_done = threading.Semaphore(0)


def worker_a() -> None:
    logging.info('a1')
    a1_done.release()
    b1_done.acquire()
    logging.info('a2')


def worker_b() -> None:
    logging.info('b1')
    b1_done.release()
    a1_done.acquire()
    logging.info('b2')


def main() -> None:
    thread_a = threading.Thread(target=worker_a)
    thread_b = threading.Thread(target=worker_b)

    thread_a.start()
    thread_b.start()

    thread_a.join()
    thread_b.join()


if __name__ == '__main__':
    main()
