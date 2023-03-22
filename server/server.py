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
from vacations_db import VacationsDB


class MyRequestHandler(BaseHTTPRequestHandler):
    def handleNotFound(self):
        # response status code:
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found", "utf-8"))

    def handleGetVacationsCollection(self):
        db = VacationsDB()
        allVacations = db.getAllVacations()
        # response status code:
        self.send_response(200)
        # repsonse header:
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        # response body
        self.wfile.write(bytes(json.dumps(allVacations), "utf-8"))

    def handleGetVacationsMember(self, vacation_id):
        db = VacationsDB()
        oneVacation = db.getOneVacation(vacation_id)

        if oneVacation != None:
            # response status code:
            self.send_response(200)
            # repsonse header:
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            # response body
            self.wfile.write(bytes(json.dumps(oneVacation), "utf-8"))
        else:
            self.handleNotFound()

    def handleDeleteVacationMember(self, vacation_id):
        db = VacationsDB()
        oneVacation = db.deleteOneVacation(vacation_id)

        if oneVacation == True:
            # response status code:
            self.send_response(200)
            # repsonse header:
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            # response body
            self.wfile.write(bytes("Deleted", "utf-8"))
        else:
            self.handleNotFound()

    def handleCreateVacation(self):
        print("request headers:", self.headers)
        # read the data in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body", parsed_body)

        # save vacation to the "database"
        vacation_location = parsed_body["location"][
            0
        ]  # indexed in the value is a list
        vacation_activity = parsed_body["activity"][0]
        vacation_climate = parsed_body["climate"][0]
        vacation_cost = parsed_body["cost"][0]
        vacation_length = parsed_body["length"][0]
        db = VacationsDB()
        db.createVacation(
            vacation_location,
            vacation_activity,
            vacation_climate,
            vacation_cost,
            vacation_length,
        )

        # send a response
        self.send_response(201)  # successfully created\
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def handleUpdateVacationMember(self, vacation_id):
        print("request headers:", self.headers)
        # read the data in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body", parsed_body)

        # save movie name to the "database"
        vacation_location = parsed_body["location"][
            0
        ]  # indexed in the value is a list
        vacation_activity = parsed_body["activity"][0]
        vacation_climate = parsed_body["climate"][0]
        vacation_cost = parsed_body["cost"][0]
        vacation_length = parsed_body["length"][0]

        db = VacationsDB()
        exists = db.updateVacation(
            vacation_location,
            vacation_activity,
            vacation_climate,
            vacation_cost,
            vacation_length,
            vacation_id,
        )

        if exists:

            # send a response
            self.send_response(200)  # successfully created\
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
        else:
            self.handleNotFound()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET,POST, PUT, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_DELETE(self):
        path_parts = self.path.split("/")
        if len(path_parts) == 3:
            collection_name = path_parts[1]
            member_id = path_parts[2]
        else:
            collection_name = path_parts[1]
            member_id = None

        if collection_name == "vacations":
            if member_id:
                self.handleDeleteVacationMember(member_id)
            else:
                self.handleNotFound()  # since this is delete/update we do 404 error
        else:
            self.handleNotFound()

    def do_GET(self):
        path_parts = self.path.split("/")
        if len(path_parts) == 3:
            collection_name = path_parts[1]
            member_id = path_parts[2]
        else:
            collection_name = path_parts[1]
            member_id = None

        if collection_name == "vacations":
            if member_id:
                self.handleGetVacationsMember(member_id)
            else:
                self.handleGetVacationsCollection()  # if this was delete/update we would do 404 error
        else:
            self.handleNotFound()

    def do_POST(self):
        if self.path == "/vacations":
            self.handleCreateVacation()
        else:
            self.handleNotFound()

    def do_PUT(self):
        path_parts = self.path.split("/")
        if len(path_parts) == 3:
            collection_name = path_parts[1]
            member_id = path_parts[2]
        else:
            collection_name = path_parts[1]
            member_id = None

        if collection_name == "vacations":
            if member_id:
                self.handleUpdateVacationMember(member_id)
            else:
                self.handleNotFound()  # since this is delete/update we  do 404 error
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
