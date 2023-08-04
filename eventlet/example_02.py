#!/usr/bin/python3

import eventlet
import pdb

Timeout = eventlet.timeout.Timeout

class Event(object):
    def __init__(self):
        self._ev = eventlet.event.Event()
        self._cond = False

    def _wait(self, timeout=None):
        while not self._cond:
            self._ev.wait()

    def _broadcast(self):
        self._ev.send()
        # Since eventlet Event doesn't allow multiple send() operations
        # on an event, re-create the underlying event.
        # Note: _ev.reset() is obsolete.
        self._ev = eventlet.event.Event()

    def is_set(self):
        return self._cond

    def set(self):
        self._cond = True
        self._broadcast()

    def clear(self):
        self._cond = False

    def wait(self, timeout=None):
        if timeout is None:
            self._wait()
        else:
            try:
                with Timeout(timeout):
                    self._wait()
                    print(" --> [O][Event Class] Timeout Exception does NOT happen!")
            except Timeout:
                print(" --> [X][Event Class] Timeout Exception happen!")
                pass

        return self._cond


print("1. create Event instance")
ev = Event()

def timeout(t):
    timer = eventlet.timeout.Timeout(t)

def event_set():
    ev.set()

def th1_foo(event, timer=0):
    print(f"[Thread #1] 2. create Timeout instance(timeout: {timer}s)")
    try:
        with eventlet.Timeout(timer):
            ret_wait = event.wait()
        print("   -> [O][Main][Th1_foo] Exception not happen!")
    except eventlet.timeout.Timeout as to:
        print("   -> [X][Main][Th1_foo] Timeout Exception happen!")
    print("[Thread #1] 4. end... wait()")

def th2_foo(event, sleep_t=0):
    eventlet.sleep(sleep_t)
    print("[Thread #2] 3. send() to wakeup for sleep threads...")
    event_set()


def main():
    print("create thread#1 to run th1_foo")
    t1 = eventlet.spawn(th1_foo, ev, timer=10)

    print("create thread#2 to run th1_foo")
    t2 = eventlet.spawn(th1_foo, ev, timer=10)

    print("create thread#3 to run th1_foo")
    t3 = eventlet.spawn(th1_foo, ev, timer=10)

    print("create thread#2 to run th2_foo")
    t4 = eventlet.spawn(th2_foo, ev, sleep_t=1)

    t1.wait()
    t2.wait()
    t3.wait()
    t4.wait()

if __name__ == "__main__":
    main()
