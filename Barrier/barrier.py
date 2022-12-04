import logging
import threading


logging.basicConfig(format='%(message)s', level=logging.INFO)


NUM_OF_THREADS = 10
in_wait = 0
# mutex for safe increment
mutex = threading.Semaphore(1)
barrier = threading.Semaphore(0)


def worker(work_no: int) -> None:
    global in_wait

    # do some rendezvous...
    logging.info(f'Worker {work_no} finishes rendezvous.')

    mutex.acquire()
    in_wait += 1
    logging.info(f'Worker {work_no} is waiting...')
    mutex.release()

    # The last thread in wait meets the condition and passes the barrier.
    if in_wait == NUM_OF_THREADS:
        barrier.release()

    # This immediately release pattern is called turnstile,
    # threads pass the barrier one by one.
    barrier.acquire()
    barrier.release()

    # get into critical point...
    logging.info(f'Worker {work_no} is now in critical point!')
    # do some critical work...


def main() -> None:
    threads = []
    for work_no in range(NUM_OF_THREADS):
        thread = threading.Thread(target=worker, args=(work_no,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
