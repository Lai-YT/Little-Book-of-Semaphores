"""This is an exclusive queue, leaders and followers dance in pairs."""

import logging
import random
import threading


logging.basicConfig(format='%(message)s', level=logging.INFO)


leader_queue = threading.Semaphore(0)
follower_queue = threading.Semaphore(0)
# check that both threads are done dancing
rendezvous = threading.Semaphore(0)
# keep track of the number of dancers of each kinds that are waiting
mutex = threading.Semaphore(1)


class Leader:
    leader_in_wait = 0

    def arrive(self) -> None:
        mutex.acquire()
        if Follower.follower_in_wait > 0:
            # if there's any follower, take "one" into dance
            Follower.follower_in_wait -= 1
            follower_queue.release()
        else:
            # leader waits and release mutex
            Leader.leader_in_wait += 1
            logging.info(f'\tleader in wait: {Leader.leader_in_wait}')
            mutex.release()
            # wait for the follower to arrive
            leader_queue.acquire()
        # now can dance, either by a existing follower of an arrival
        self.dance()
        # wait for the follower to dance, too
        rendezvous.acquire()
        # this pair of dancer ends their process
        mutex.release()

    def dance(self) -> None:
        logging.info('Leader says let\'s dance!')


class Follower:
    follower_in_wait = 0

    def arrive(self) -> None:
        mutex.acquire()
        if Leader.leader_in_wait > 0:
            # if there's any leader, take "one" into dance
            Leader.leader_in_wait -= 1
            leader_queue.release()
        else:
            # follower waits and release mutex
            Follower.follower_in_wait += 1
            logging.info(f'\tfollower in wait: {Follower.follower_in_wait}')
            mutex.release()
            # wait for the leader to arrive
            follower_queue.acquire()
        # now can dance, either by a existing leader of an arrival
        self.dance()
        # tell the leader that the follower is now also dancing
        rendezvous.release()
        # leader handles the release of this pair of dancer,
        # so follower doesn't release

    def dance(self) -> None:
        logging.info('Follower says let\'s dance!')


def main() -> None:
    dancers = [Leader() for _ in range(10)] + [Follower() for _ in range(10)]
    # since Timer is used to fire the threads randomly,
    # one may not need to shuffle
    random.shuffle(dancers)

    dancer_threads = []
    for dancer in dancers:
        # simulate the uncertain time of arrival
        thread = threading.Timer(random.randint(0, 5), dancer.arrive)
        dancer_threads.append(thread)
        thread.start()

    for thread in dancer_threads:
        thread.join()


if __name__ == '__main__':
    main()
