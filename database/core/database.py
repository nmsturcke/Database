#encoding utf-8

# (c) Nickyux 2021 - current 
# (GitHub) @nmsturcke
# (Repository) https://github.com/nmsturcke/Database 

import sqlite3, json, os
from typing import Union

class DataBase():
    def __init__(self, path: str, keys:list = []) -> 'DataBase':
        """
        Class DataBase
        
        Sqlite rapper for a database object, the best way to connect to your database without having to remember all those tedious SQLite commands!
        
        :param path: The path to your database
        :type path: str
        :param keys: The keys you want your database to have
        :type keys: list = []
        :returns: DataBase
        """

        self.path = path
        self.keys = keys

        abspath = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        self._conn = self._conn = sqlite3.connect(abspath, check_same_thread=False)
        self._c = self._conn.cursor()
        self.na_create_table()

    # Backend functions

    def _format(self, item: Union[dict, list, int, str]) -> str:
        """
        Correctly formats an item to input into a SQLite command
        
        :param item: The item you want to format
        :type item: Union[dict, list, str, int]
        :returns: str
        """

        rem: str= lambda i: i.replace("'", "‘")

        return f"'{rem(json.dumps(item))}'"
        
    def _formatres(self, res: tuple) -> dict:
        """
        Formats the response from *args to **kwargs (tuple -> dictionary)
        
        :param res: The response you want to format
        :type res: tuple
        :returns dict:
        """
        
        kn = 0

        # Check if it's find_all
        fa = True
        for item in res:
            if not isinstance(item, tuple):
                fa = False

        if fa:
            out = []

            for item in res:
                out.append(self._formatres(item))

        else:
            out = {}
            for item in res:
                if not isinstance(item, int) and not isinstance(item, float) and not item is None and not item == "":
                    try:
                        out[self.keys[kn]] = json.loads(item)
                        kn += 1
                        continue
                    except:
                        pass
                
                out[self.keys[kn]] = item
                kn += 1
        
        return out
    
    def _formatadd(self, data: dict) -> str:
        """
        Formats the data to to add it to the string
        
        :param data: The data you want to format
        :type data: dict
        :returns: str
        """
        out = ""

        total = len(data)
        n = 1

        for qkey, qvalue in data.items():
            out += f"{qkey}={self._format(qvalue)}"

            if n < total:
                out += " AND "
            
            n += 1
        
        return out

    # Asynchronus functions

    async def create_table(self) -> None:
        """
        Create a table (if it doesn't exist)
        
        Equivalent: CREATE TABLE IF NOT EXISTS main(keys)
        """

        self._c.execute(f"CREATE TABLE IF NOT EXISTS main({', '.join(k for k in self.keys)})")
        self._conn.commit()

    async def find_one(self, query: dict) -> Union[dict, None]:
        """
        Find an object in your database that matches a query
        
        Equivalent: 'SELECT * FROM main WHERE key=value'
        
        :param query: Query values of your database
        :type query: dict
        :return: Union[dict, None]
        """

        t = f"SELECT * FROM main WHERE {self._formatadd(query)}"

        self._c.execute(t)
        fetch = self._c.fetchone()
        
        if not fetch:
            return None
        
        return self._formatres(fetch)
    
    async def find_all(self) -> Union[list, None]:
        """
        Find all objects in your database, 
        
        Equivalent: 'SELECT * FROM main'
        
        :return: Union[list, None]
        """

        t = "SELECT * FROM main"

        self._c.execute(t)
        fetch = self._c.fetchall()

        if not fetch:
            return None
        
        return self._formatres(fetch)
    
    async def update_one(self, query: dict, data: dict) -> None:
        """
        Updates an item in your database that fits the query to the new data you specify.
        
        Equivalent: 'UPATE main SET data WHERE query'
        
        :param query: The match your item has to have
        :type query: dict
        :param data: The new data your item should have
        :type data: dict
        :returns None
        """

        t = "UPDATE main SET " + ", ".join(f"{dkey}={self._format(dvalue)}" for dkey, dvalue in data.items()) + f" WHERE {self._formatadd(query)}"
        self._c.execute(t)
        self._conn.commit()

    async def insert(self, data: dict) -> None:
        """
        Insert an item into your database.
        
        Equivalent: 'INSERT OR IGNORE INTO main(keys) VALUES (data)
        
        :param data: The data you want to insert
        :type data: dict
        :returns: None
        """

        args = tuple()

        for key in self.keys:
            if key in data:
                args += (self._format(data[key]), )
            else:
                args += (json.dumps(None), )

        self._c.execute(f"INSERT OR IGNORE INTO main({', '.join(k for k in self.keys)}) VALUES ({', '.join(arg for arg in args)})")#, args)
        self._conn.commit()
    
    async def delete(self, query: dict) -> None:
        """
        Delete an item from your database, it must match the query specified
        
        Equivalent: DELETE * FROM main WHERE query
        
        :param query: The query the item must match in order to be deleted
        :type query: dict
        :returns: None
        """

        t = f"DELETE FROM main WHERE {self._formatadd(query)}"

        self._c.execute(t)
        self._conn.commit()
    
    # Non Asynchronous functions (na)

    def na_create_table(self) -> None:
        """
        Create a table (if it doesn't exist)
        
        Equivalent: CREATE TABLE IF NOT EXISTS main(keys)
        """

        self._c.execute(f"CREATE TABLE IF NOT EXISTS main({', '.join(k for k in self.keys)})")
        self._conn.commit()

    def na_find_one(self, query: dict) -> Union[dict, None]:
        """
        Find an object in your database that matches a query
        
        Equivalent: 'SELECT * FROM main WHERE key=value'
        
        :param query: Query values of your database
        :type query: dict
        :return: Union[dict, None]
        """

        t = f"SELECT * FROM main WHERE {self._formatadd(query)}"

        self._c.execute(t)
        fetch = self._c.fetchone()
        
        if not fetch:
            return None
        
        return self._formatres(fetch)
    
    def na_find_all(self) -> Union[list, None]:
        """
        Find all objects in your database, 
        
        Equivalent: 'SELECT * FROM main'
        
        :return: Union[list, None]
        """

        t = "SELECT * FROM main"

        self._c.execute(t)
        fetch = self._c.fetchall()

        if not fetch:
            return None
        
        return self._formatres(fetch)
    
    def na_update_one(self, query: dict, data: dict) -> None:
        """
        Updates an item in your database that fits the query to the new data you specify.
        
        Equivalent: 'UPATE main SET data WHERE query'
        
        :param query: The match your item has to have
        :type query: dict
        :param data: The new data your item should have
        :type data: dict
        :returns None
        """

        t = "UPDATE main SET "

        for dkey, dvalue in data.items():
            t += f"{dkey}={self._format(dvalue)}"

        t += f"WHERE {self._formatadd(query)}"
        
        self._c.execute(t)
        self._conn.commit()

    def na_insert(self, data: dict) -> None:
        """
        Insert an item into your database.
        
        Equivalent: 'INSERT OR IGNORE INTO main(keys) VALUES (data)
        
        :param data: The data you want to insert
        :type data: dict
        :returns: None
        """

        args = tuple()

        for key in self.keys:
            if key in data:
                args += (self._format(data[key]), )
            else:
                args += (json.dumps(None), )

        self._c.execute(f"INSERT OR IGNORE INTO main({', '.join(k for k in self.keys)}) VALUES ({', '.join(arg for arg in args)})")#, args)
        self._conn.commit()
    
    def na_delete(self, query: dict) -> None:
        """
        Delete an item from your database, it must match the query specified
        
        Equivalent: DELETE * FROM main WHERE query
        
        :param query: The query the item must match in order to be deleted
        :type query: dict
        :returns: None
        """

        t = f"DELETE FROM main WHERE {self._formatadd(query)}"

        self._c.execute(t)
        self._conn.commit()
