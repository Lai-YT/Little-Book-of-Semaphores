import logging
import random
import threading
import time


logging.basicConfig(format='%(message)s', level=logging.INFO)


class Event:
    def process(self) -> None:
        time.sleep(random.random() * 3)


def wait_for_event() -> Event:
    time.sleep(random.random() * 3)
    return Event()


buffer = []

# mutex provides exclusive access to the buffer
mutex = threading.Semaphore(1)
# When items is positive, it indicates the number of items in the buffer.
# When it is negative, it indicates the number of consumer threads in queue.
items = threading.Semaphore(0)


def produce(producer_no: int) -> None:
    # The producer doesn't have to get exclusive access to the buffer until it
    # gets an event. Several threads can run wait_for_event concurrently.
    logging.info(f'Producer {producer_no} waiting for an event...')
    event = wait_for_event()

    mutex.acquire()
    buffer.append(event)
    mutex.release()

    # The items semaphore keeps track of the number of items in the buffer. Each
    # time the producer adds an item, it signals items, incrementing it by one.
    items.release()


def consume(consumer_no: int) -> None:
    # The buffer operation is protected by a mutex, but before the consumer
    # gets to it, it has to decrement items. If items is zero or negative,
    # the consumer blocks until a producer signals.
    items.acquire()

    mutex.acquire()
    event = buffer.pop(0)
    mutex.release()

    logging.info(f'> Consumer {consumer_no} consuming an event...')
    event.process()


def main() -> None:
    num_of_events = 10

    producers = []
    for producer_no in range(num_of_events):
        producer = (
            threading.Timer(random.randint(0, 5), function=produce, args=(producer_no,)))
        producers.append(producer)
    consumers = []
    for consumer_no in range(num_of_events):
        consumer = (  # The consumers get into the queue faster than producers to have them waiting.
            threading.Timer(random.randint(0, 2), function=consume, args=(consumer_no,)))
        consumers.append(consumer)

    for consumer, producer in zip(consumers, producers):
        consumer.start()
        producer.start()

    for consumer, producer in zip(consumers, producers):
        consumer.join()
        producer.join()


if __name__ == '__main__':
    main()
