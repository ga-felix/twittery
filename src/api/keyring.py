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
        self.timer = list()
        self._lock = RLock()

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
        self.timer.append(time.time()) # Assign time when key is requested
        print(str(threading.get_ident()) + " Key was obtained! " + str(key))
        return key

    def wait(self):
        if len(self.keyring) == 0:
            maximum_elapsed = -1
            now = time.time()
            key_index = None
            for index, key in enumerate(self.in_use):
                elapsed = now - self.timer[index]
                if elapsed > maximum_elapsed:
                    maximum_elapsed = elapsed
                    key_index = index
            print(str(threading.get_ident()) + " Waiting next key available in " + str(3 * 1 - maximum_elapsed))
            time.sleep(3 * 1 - maximum_elapsed)
            self.keyring.append(self.in_use[key_index])
            self.in_use.pop(key_index)
            self.timer.pop(key_index)
            print(str(threading.get_ident()) + " Key released")

    def release(self):
        self._lock.release() # Leave critical section
        print(str(threading.get_ident()) + " Lock was released just now ")
            
    def return_key(self, key):
        self.keyring.append(key)
        index = self.in_use.index(key)
        self.in_use.pop(index)
        self.timer.pop(index)
        print(str(threading.get_ident()) + " Iteration over. Returned key ")
        self._lock.release() # Leave critical section
