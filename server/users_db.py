#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 21:21:38 2023

@author: brooklynprice
"""

import sqlite3
from passlib.hash import bcrypt

# first use sqlite3 in terminal to create a database:
# CREATE TABLE vacation () ....
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {
        key: value for key, value in zip(fields, row)
    }  # makes it so records returns as a diction with keys


class UsersDB:
    def __init__(self):
        self.connection = sqlite3.connect("vacations_db.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def createUser(self, fname, lname, email, pw):

        # INSERT record
        data = [email]  # always has to be an array/list

        self.cursor.execute("SELECT * FROM users WHERE email== ?", data)
        record = self.cursor.fetchone()
        if record:
            return False
        else:
            pw = bcrypt.hash(pw)
            data = [fname, lname, email, pw]
            self.cursor.execute(
                "INSERT INTO users (fname, lname, email, pass) VALUES (?,?,?,?)",
                data,
            )
            self.connection.commit()  # saves DON'T do on select commands
            return True

    def getAllUsers(self):

        # read all records
        self.cursor.execute("SELECT * FROM users")

        records = (
            self.cursor.fetchall()
        )  # show the data follow a select with a fetch
        return records

    def getOneUser(self, user_id):
        data = [user_id]
        # read one record
        self.cursor.execute("SELECT * FROM users WHERE id=?", data)
        record = self.cursor.fetchone()
        return record

    def deleteOneUser(self, user_id):
        data = [user_id]
        # single record
        self.cursor.execute(
            "SELECT * FROM users WHERE id=?", data
        )  # one or none doesn't return an array
        record = self.cursor.fetchone()
        if record:
            self.cursor.execute("DELETE FROM users WHERE id=?", data)
            self.connection.commit()
            return True
        else:
            return record

    def updateUser(self, fname, lname, email, pw, user_id):
        data = [user_id]

        self.cursor.execute(
            "SELECT * FROM users WHERE id=?", data
        )  # one or none doesn't return an array
        record = self.cursor.fetchone()
        if record:
            # INSERT record
            data = [
                fname,
                lname,
                email,
                pw,
                user_id,
            ]  # always has to be an array/list
            self.cursor.execute(
                "UPDATE users SET fname=?, lname=?, email=?,pass=? WHERE id=?",
                data,
            )
            self.connection.commit()  # saves DON'T do on select commands
            return True
        else:
            return None

    def verifyUser(self, email, pw):
        data = [email]
        self.cursor.execute("SELECT * FROM users WHERE email=?", data)
        record = self.cursor.fetchone()
        if record:
            print(record)
            res = bcrypt.verify(pw, record["pass"])
            if res:
                return record
            else:
                return False

        else:
            return False
