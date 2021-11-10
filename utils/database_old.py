import sqlite3
from typing import Callable, List, Tuple

class Database:
    def __init__(self, database_name: str) -> None:
        self.db_name = database_name
        self.db = sqlite3.connect(self.db_name)
        self.cursor = self.db.cursor()
        self.execute = self.cursor.execute
        self.executemany = self.cursor.executemany
        self.executescript = self.cursor.executescript
    def add_table(self, table_name: str, columns: List[Tuple]) -> None:
        # columns = ",".join([" ".join((name, data_type)) if not const else " ".join((name, data_type, const)) for name, data_type, const in columns])
        self.executemany("CREATE TABLE ? (?,?,?)", (table_name, columns))
    
    def drop_table(self, table_name: str, if_exists: bool = False) -> None:
        self.execute("DROP TABLE ? ?", (if_exists or '', table_name))
    
    def insert_into(self, table_name: str, values: Tuple | List, columns: Tuple | List = '') -> None:
        self.execute("INSERT INTO ? ? VALUES ?", (table_name, columns, values))
    
    def select(self, text: str, fetch: str = None, formatting: Tuple = tuple()):
        '''
        Parameters
        ----------
        text
            - Actual thing to execute after typing SELECT

        fetch
            - It could be any of these:
                - "all"
                - "one"
        
        formatting
            - A tuple to pass to `self.cursor.execute` to format.
        '''
        print('SELECT %s' % text, formatting)
        self.execute('SELECT %s' % text, formatting)
        match fetch:
            case 'all':
                return self.cursor.fetchall()
            case 'one':
                return self.cursor.fetchone()
            case _:
                fetch = self.cursor.fetchall()
                # 1 is considered True and 0 is considered False. If you're confused what I did below.
                return fetch[0] if len(fetch) else fetch