from pickledb import PickleDB
from utils._logging import Logger
from threading import Thread
import os
import json


class Database(PickleDB):
    def __init__(self, location, auto_dump, sig=True) -> None:
        self.logger = Logger("database.log")
        self.log = self.logger.log.info
        super().__init__(location, auto_dump, sig)

    def load(self, location, auto_dump):
        """Loads, reloads or changes the path to the db file"""
        self.log("Loading %s | Auto dump was set to %s", location, auto_dump)
        location = os.path.expanduser(location)
        self.loco = location
        self.auto_dump = auto_dump
        self.location = location
        if os.path.exists(location):
            self._loaddb()
        else:
            self.db = {}
        self.log("Loaded %s", location)
        return True

    def dump(self):
        """Force dump memory db to file"""
        self.log("Dumping %s", self.location)
        json.dump(self.db, open(self.loco, "wt"), indent=4)
        self.dthread = Thread(
            target=json.dump,
            kwargs={"indent": 4},
            args=(self.db, open(self.loco, "wt")),
        )
        self.dthread.start()
        self.dthread.join()
        self.log("Dumped %s", self.location)
        return True

    def get(self, *keys):
        # current = None
        # for key in keys:
        #     if current is None:
        #         current = self.db.get(key)
        #     else:
        #         if current and (value := current.get(key)):
        #             current = value
        # return current
        current = self.db.copy()
        for key in keys[:-1]:
            current = current.setdefault(key, {})
        return current.get(keys[-1])

    def set(self, *keys, value):
        current = self.db
        for key in keys[:-1]:
            current = current.setdefault(key, {})
        current[keys[-1]] = value
        self._autodumpdb()

    def deldb(self):
        """Delete everything from the database"""
        self.log("Deleting everything from the db.")
        self.db = {}
        self._autodumpdb()
        return True
