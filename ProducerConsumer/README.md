# 4.1 Producer-consumer problem

*Producer*s create items of some kind and add them to a data structure; *consumer*s remove the items and process them. \
Whenever an event occurs, a producer thread creates an event object and adds it to the event buffer. Concurrently, consumer threads take events out
of the buffer and process them. \
In this case, the consumers are called "event
handlers". \
There are several synchronization constraints that we need to enforce to make this system work correctly:

- While an item is being added to or removed from the buffer, the buffer is in an inconsistent state. Therefore, threads must have exclusive access to the buffer.
- If a consumer thread arrives while the buffer is empty, it blocks until a producer adds a new item.

Assume that producers perform the following operations over and over:

```python
event = wait_for_event()
buffer.add(event)
```

Also, assume that consumers perform the following operations:

```python
event = buffer.get()
event.process()
```

As specified above, access to the buffer has to be exclusive, but `wait_for_event` and `event.process` can run concurrently.

## Puzzle

Add synchronization statements to the producer and consumer code to enforce the synchronization constraints.


