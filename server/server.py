#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 12:47:02 2023

@author: brooklynprice
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import json
from urllib.parse import parse_qs
from dummydb import DummyDB

# MY_VACATIONS = [
#     "Backpack through Europe",
#     "Hike Machu Picchu",
#     "Pyramids in Egypt",
# ]


class MyRequestHandler(BaseHTTPRequestHandler):
    def handleNotFound(self):
        # response status code:
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found", "utf-8"))

    def handleGetVacationsCollection(self):
        # response status code:
        self.send_response(200)
        # repsonse header:
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        # response body
        db = DummyDB("vacations_db.db")
        allVacations = db.readAllRecords()
        self.wfile.write(bytes(json.dumps(allVacations), "utf-8"))

    def handleCreateVacation(self):
        print("request headers:", self.headers)
        # read the data in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body", parsed_body)

        # save vacation to the "database"
        vacation_name = parsed_body["name"][
            0
        ]  # indexed in the value is a list
        db = DummyDB("vacations_db.db")
        db.saveRecord(vacation_name)

        # send a response
        self.send_response(201)  # successfully created\
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        if self.path == "/vacations":
            self.handleGetVacationsCollection()
        else:
            self.handleNotFound()

    def do_POST(self):
        if self.path == "/vacations":
            self.handleCreateVacation()
        else:
            self.handleNotFound()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def run():
    listen = ("127.0.0.1", 8080)
    server = ThreadedHTTPServer(listen, MyRequestHandler)
    print("Server running")
    server.serve_forever()


if __name__ == "__main__":
    run()
