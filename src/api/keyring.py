#!/usr/bin/python
import json
import time
from pathlib import Path
from threading import RLock
from threading import Lock

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
        print("Key was requested.")
        self._lock.acquire() # Enter critical section
        self.wait() # If there's no key available, wait
        key = self.keyring.pop() # Assign requested key
        self.in_use.append(key) # Key is now in use
        self.timer.append(time.time()) # Assign time when key is requested
        self._lock.release() # Leave critical section
        print("Key was obtained! " + str(key))
        return key

    def wait(self):
        if len(self.keyring) == 0:
            maximum_elapsed = -1
            now = time.time()
            print("TEMPO AGORA " + str(now))
            key_index = None
            for index, key in enumerate(self.in_use):
                elapsed = now - self.timer[index]
                print("PASSOU " + str(elapsed))
                if elapsed > maximum_elapsed:
                    maximum_elapsed = elapsed
                    key_index = index
            print("Waiting next key available in " + str(60 * 15 - maximum_elapsed))
            time.sleep(60 * 15 - maximum_elapsed)
            self.keyring.append(self.in_use[key_index])
            self.in_use.pop(key_index)
            self.timer.pop(key_index)
            print("Key released " + str(self.in_use[key_index]))

    def release(self, key):
        self.keyring.append(key)
        index = self.in_use.index(key)
        self.in_use.pop(index)
        self.timer.pop(index)
        print("Key was released just now " + str(key))
            
