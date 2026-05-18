from threading import Semaphore, Thread, Event
import time

sem: Semaphore = Semaphore()
stop_event = Event()


def fun1():
    while not stop_event.is_set():
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    while not stop_event.is_set():
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


t1: Thread = Thread(target=fun1)
t2: Thread = Thread(target=fun2)

t1.start()
t2.start()

try:
    while t1.is_alive() or t2.is_alive():
        time.sleep(0.1)

except KeyboardInterrupt:
    print('\nReceived keyboard interrupt, quitting threads.')
    stop_event.set()

    t1.join()
    t2.join()
