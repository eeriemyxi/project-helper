from pickledb import PickleDB
from utils._logging import Logger
from threading import Thread
import os
import json
from contextlib import suppress
class Database(PickleDB):
    def __init__(self, location, auto_dump, sig=True) -> None:
        self.logger = Logger('database.log')
        self.log = self.logger.log.info
        super().__init__(location, auto_dump, sig)

    def load(self, location, auto_dump):
        '''Loads, reloads or changes the path to the db file'''
        self.log('Loading %s | Auto dump was set to %s', location, auto_dump)
        location = os.path.expanduser(location)
        self.loco = location
        self.auto_dump = auto_dump
        self.location = location
        if os.path.exists(location):
            self._loaddb()
        else:
            self.db = {}
        self.log('Loaded %s', location)
        return True

    def dump(self):
        '''Force dump memory db to file'''
        self.log('Dumping %s', self.location)
        json.dump(self.db, open(self.loco, 'wt'), indent=4)
        self.dthread = Thread(
            target=json.dump,
            kwargs={'indent':4},
            args=(self.db, open(self.loco, 'wt')))
        self.dthread.start()
        self.dthread.join()
        self.log("Dumped %s", self.location)
        return True

    def append(self, key, more):
        '''Add more to a key's value'''
        self.log("Appending `%s` to the key `%s`", more, key)
        tmp = self.db[key]
        self.db[key] = tmp + more
        self._autodumpdb()
        return True
    
    def set(self, key, value):
        '''Set the str value of a key'''
        if isinstance(key, str):
            self.log("Setting key `%s` to `%s`", key, value)
            self.db[key] = value
            self._autodumpdb()
            return True
        else:
            raise self.key_string_error

    def get(self, key):
        '''Get the value of a key'''
        try:
            value = self.db[key]
            self.log("Getting key `%s`. `%s`'s value was `%s`", key, key, value)
            return value
        except KeyError:
            return None
            
    def dadd(self, name, key, value):
        '''Add a key-value pair to a dict, "pair" is a tuple'''
        self.db[name][key] = value
        self._autodumpdb()
        return True
    
    def _dget(self, key: str):
        current = None
        keys = key.split('.') if '.' in key else [key]
        for _key in keys:
            if current is None:
                current = self.db.get(_key)
            else:
                if current and (value := current.get(_key)):
                    current = value
        return current

    def dset(self, key: str, value):
        if self._dget(key) is not None:
            key = key.split('.') if '.' in key else [key]
            index = "".join([repr([i]) for i in key])
            exec(f'self.db{index} = {repr(value)}')
            self._autodumpdb()
        else:
            raise KeyError('Key not found.')
    def deldb(self):
        '''Delete everything from the database'''
        self.log('Deleting everything from the db.')
        self.db = {}
        self._autodumpdb()
        return True