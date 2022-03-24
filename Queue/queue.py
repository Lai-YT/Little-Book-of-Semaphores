import logging
import random
import threading

logging.basicConfig(format="%(message)s", level=logging.INFO)


leader_queue = threading.Semaphore(0)
follower_queue = threading.Semaphore(0)


class Leader:
    def arrive(self) -> None:
        follower_queue.release()
        leader_queue.acquire()
        self.dance()

    def dance(self) -> None:
        logging.info('Follower says let\'s dance!')


class Follower:
    def arrive(self) -> None:
        leader_queue.release()
        follower_queue.acquire()
        self.dance()

    def dance(self) -> None:
        logging.info('Leader says let\'s dance!')


def main() -> None:
    dancers = [Leader() for _ in range(10)] + [Follower() for _ in range(10)]
    random.shuffle(dancers)

    dancer_threads = []
    for dancer in dancers:
        thread = threading.Thread(target=dancer.arrive)
        dancer_threads.append(thread)
        thread.start()

    for thread in dancer_threads:
        thread.join()


if __name__ == '__main__':
    main()
