#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 21:37:47 2023

@author: brooklynprice
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:58:40 2023

@author: brooklynprice
"""

import os
import psycopg2
import psycopg2.extras
import urllib.parse

# first use sqlite3 in terminal to create a database:
# CREATE TABLE vacation () ....
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {
        key: value for key, value in zip(fields, row)
    }  # makes it so records returns as a diction with keys


class VacationsDB:
    def __init__(self):

        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
        )

        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def createVacationsTable(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS vacations (id SERIAL PRIMARY KEY, location TEXT, activity TEXT, climate TEXT, cost TEXT, length TEXT)"
        )

        self.connection.commit()

    def createUsersTable(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, fname TEXT, lname TEXT, email TEXT, pass TEXT);"
        )
        self.connection.commit()

    def createVacation(self, location, activity, climate, cost, length):

        # INSERT record
        data = [
            location,
            activity,
            climate,
            cost,
            length,
        ]  # always has to be an array/list
        self.cursor.execute(
            "INSERT INTO vacations (location, activity, climate, cost, length) VALUES (%s,%s,%s,%s,%s)",
            data,
        )
        self.connection.commit()  # saves DON'T do on select commands

    def getAllVacations(self):

        # read all records
        self.cursor.execute("SELECT * FROM vacations")

        records = (
            self.cursor.fetchall()
        )  # show the data follow a select with a fetch
        return records

    def updateVacation(
        self, location, activity, climate, cost, length, vacation_id
    ):
        data = [vacation_id]

        self.cursor.execute(
            "SELECT * FROM vacations WHERE id=%s", data
        )  # one or none doesn't return an array
        record = self.cursor.fetchone()
        if record:
            # INSERT record
            data = [
                location,
                activity,
                climate,
                cost,
                length,
                vacation_id,
            ]  # always has to be an array/list
            self.cursor.execute(
                "UPDATE vacations SET location=%s, activity=%s, climate=%s,cost=%s,length=%s WHERE id=%s",
                data,
            )
            self.connection.commit()  # saves DON'T do on select commands
            return True
        else:
            return None

    def getOneVacation(self, vacation_id):
        data = [vacation_id]
        # read one record
        self.cursor.execute("SELECT * FROM vacations WHERE id=%s", data)
        record = self.cursor.fetchone()
        return record

    def deleteOneVacation(self, vacation_id):
        data = [vacation_id]
        # single record
        self.cursor.execute(
            "SELECT * FROM vacations WHERE id=%s", data
        )  # one or none doesn't return an array
        record = self.cursor.fetchone()
        if record:
            self.cursor.execute("DELETE FROM vacations WHERE id=%s", data)
            self.connection.commit()
            return True
        else:
            return record
