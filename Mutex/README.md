# Mutex

## Puzzle

Add semaphores to the following example to enforce mutual exclusion \
to the shared variable `count`.

*Thread A*
```
1 count = count + 1
```

*Thread B*
```
1 count = count + 1
```
