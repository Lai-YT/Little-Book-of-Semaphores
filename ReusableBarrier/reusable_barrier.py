import logging
import threading


logging.basicConfig(format='%(message)s', level=logging.INFO)


NUM_OF_THREADS = 9
in_wait = 0
# mutex for safe increment
mutex = threading.Semaphore(1)
# Two-phase barrier; at most one turnstile is unlocked at a time.
turnstile = threading.Semaphore(0)
turnstile2 = threading.Semaphore(1)


def worker(work_no: int) -> None:
    global in_wait

    for i in range(1, 10):
        # do some rendezvous...
        logging.info(f'Worker {work_no} finishes rendezvous in {i}.')

        mutex.acquire()
        in_wait += 1
        logging.info(f'Worker {work_no} is waiting at turnstile 1 in {i}...')
        # The last thread in wait meets the condition and passes the turnstile.
        if in_wait == NUM_OF_THREADS:
            # lock the second and unlock the first
            turnstile2.acquire()
            turnstile.release()
            logging.info(f'--- Turnstile 1 is unlocked in {i} ---')
        mutex.release()

        # first turnstile
        turnstile.acquire()
        turnstile.release()

        # do some critical work...
        logging.info(f'Worker {work_no} finishes critical point in {i}.')

        mutex.acquire()
        in_wait -= 1
        logging.info(f'Worker {work_no} is waiting at turnstile 2 in {i}...')
        if in_wait == 0:
            # lock the first and unlock the second
            turnstile.acquire()
            turnstile2.release()
            logging.info(f'--- Turnstile 2 is unlocked in {i} ---')
        mutex.release()

        # second turnstile
        turnstile2.acquire()
        turnstile2.release()


def main() -> None:
    threads = []
    for work_no in range(NUM_OF_THREADS):
        thread = threading.Thread(target=worker, args=(work_no+1,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
