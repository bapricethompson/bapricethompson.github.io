#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 12:36:00 2023

@author: brooklynprice
"""

import json
import os.path


class DummyDB:

    ### USAGE EXAMPLE:
    #
    #  from dummydb import DummyDB
    #
    ### SAVE DICTIONARY RECORD:
    #
    #  dictRecord = { 'conditions': 'rain', 'temp': 55 }
    #  db = DummyDB('mydatabase.db')
    #  db.saveRecord(dictRecord)
    #
    ### SAVE STRING RECORD:
    #
    #  strRecord = 'cold rainy day'
    #  db = DummyDB('mydatabase.db')
    #  db.saveRecord(strRecord)
    #
    ### READ ALL RECORDS:
    #
    #  db = DummyDB('mydatabase.db')
    #  allRecords = db.readAllRecords()
    #  print(allRecords)
    #
    ###

    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def saveRecord(self, record):
        all = self.readAllRecords()
        all.append(record)
        with open(self.filename, "w") as f:
            json.dump(all, f)

    def readAllRecords(self):
        with open(self.filename, "r") as f:
            return json.load(f)
