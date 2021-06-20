#!/usr/bin/python
import json
import time
from pathlib import Path
from threading import RLock
from threading import Lock
import threading

class Keyring():

    _instance = None
    _slock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._slock:
            if not cls._instance:
                cls._instance = super(Keyring, cls).__new__(cls)
            return cls._instance

    def __init__(self):
        self.keyring = self.read()
        self.in_use = list()
        self.timer = dict()
        self._lock = RLock()
        self._rlock = RLock()

    def read(self):
        keyring = list()
        path = Path(__file__).parent
        with open((path / "keys/keys.json").resolve()) as keys_file:
            read_keys = json.load(keys_file)
            for item in read_keys:
                keys = list()
                user_keys = read_keys[item]
                for key in user_keys:
                    keyring.append(str(user_keys[key]))
            return keyring

    def request(self):
        self._lock.acquire() # Enter critical section
        print(str(threading.get_ident()) + " Key was requested.")
        self.wait() # If there's no key available, wait
        key = self.keyring.pop() # Assign requested key
        self.in_use.append(key) # Key is now in use
        now = time.time()
        if not key in self.timer:
            self.timer[key] = (now + 60 * 15) # Assign time when key is requested
        else:
            if now > self.timer[key]:
                self.timer[key] = now + 60 * 15
        print(str(threading.get_ident()) + " Key was obtained! " + str(key))
        self._lock.release() # Leave critical section
        return key

    def wait(self):
        while len(self.keyring) == 0:
            time.sleep(0.1)
            pass
            
    def release(self, key):
        self._rlock.acquire() # Enter critical section
        self.keyring.append(key)
        index = self.in_use.index(key)
        self.in_use.pop(index)
        print(str(threading.get_ident()) + " Iteration over. Returned key ")
        self._rlock.release() # Leave critical section

    def timer_key(self, key):
        return self.timer[key]