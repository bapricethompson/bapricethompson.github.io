#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 12:47:02 2023

@author: brooklynprice
"""
from http import cookies
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import json
from urllib.parse import parse_qs
from vacations_db import VacationsDB
from passlib.hash import bcrypt
from users_db import UsersDB
from session_store import SessionStore
import os

# FIGURE OUT PASSWORD ENCRYPTION
# SHOW A MESSAGE TO USER CREATING WITH AN EMAIL IN DATABASE

SESSION_STORE = SessionStore()


class MyRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        print("got here")
        self.sendCookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        # super().end_headers()
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    # read cookie data from the Cookie Header
    def loadCookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    # send cookie data using the set-cookie header
    def sendCookie(self):
        for morsel in self.cookie.values():
            if "Postman" not in self.headers["User-Agent"]:
                morsel["samesite"] = "None"
                morsel["secure"] = True
            self.send_header("Set-Cookie", morsel.OutputString())

    def loadSession(self):
        # load cookie data
        self.loadCookie()
        # check for existence of the session ID cookie
        # if the session id cookie exists:
        if "sessionId" in self.cookie:
            sessionId = self.cookie["sessionId"].value
            # self.cookie[sessionId]["SameSite"] = "None"
            # self.cookie["sessionId"]["Secure"] = True
            # load session data for the session ID
            self.sessionData = SESSION_STORE.getSessionData(sessionId)
            # if the session id is not valid:
            print("session id here: ", sessionId)
            if self.sessionData == None:
                # create a new session / session ID
                sessionId = SESSION_STORE.createSession()
                # save the new session ID into a cookie
                self.cookie["sessionId"] = sessionId
                # load the session with the new session ID
                self.sessionData = SESSION_STORE.getSessionData(sessionId)
                # self.cookie["sessionId"]["SameSite"] = "None"
                # self.cookie["sessionId"]["Secure"] = True

        else:
            print("no sessionId")
            # create a new session / session ID
            sessionId = SESSION_STORE.createSession()
            print("session id here 2: ", sessionId)
            # save the new session ID into a cookie
            self.cookie["sessionId"] = sessionId

            # load the session with the new session ID
            self.sessionData = SESSION_STORE.getSessionData(sessionId)

            # self.cookie["sessionId"]["SameSite"] = "None"
            # self.cookie["sessionId"]["Secure"] = True

            print("achieve")

    def handleNotFound(self):
        # response status code:
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found", "utf-8"))

    def handleNotAuthorized(self):
        # response status code:
        self.send_response(401)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not authorized", "utf-8"))

    def handleGetVacationsCollection(self):
        if "userId" not in self.sessionData:
            self.handleNotAuthorized()
            return
        # if "test" not in self.sessionData:
        #     self.sessionData["test"] = 1
        # else:
        #     self.sessionData["test"] += 1

        print("current session data:", self.sessionData)

        db = VacationsDB()
        allVacations = db.getAllVacations()
        # response status code:
        self.send_response(200)
        # repsonse header:
        self.send_header("Content-Type", "application/json")
        # self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.end_headers()
        # response body
        self.wfile.write(bytes(json.dumps(allVacations), "utf-8"))

    def handleCreateSession(self):
        print("request headers:", self.headers)
        # read the data in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body", parsed_body)
        print("")

        user_email = parsed_body["email"][0]
        user_pass = parsed_body["pass"][0]

        db = UsersDB()
        # user =db.getUserbyEmail
        exists = db.verifyUser(user_email, user_pass)
        print(exists)
        if exists:
            # send a response
            # persist users's authenticated identiy into the session data
            self.sessionData["userId"] = exists["id"]  # user["id"]
            print("info", self.sessionData["userId"])

            self.send_response(201)  # successfully created\
            # self.send_header(
            #    "Access-Control-Allow-Origin", self.headers["Origin"]
            # )
            self.end_headers()
        else:
            self.send_response(401)  # successfully created\
            # self.send_header(
            #    "Access-Control-Allow-Origin", self.headers["Origin"]
            # )
            self.end_headers()

    # def handleGetUsersCollection(self):
    #     db = UsersDB()
    #     allUsers = db.getAllUsers()
    #     # response status code:
    #     self.send_response(200)
    #     # repsonse header:
    #     self.send_header("Content-Type", "application/json")
    #     # self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
    #     self.end_headers()
    #     # response body
    #     self.wfile.write(bytes(json.dumps(allUsers), "utf-8"))

    def handleGetVacationsMember(self, vacation_id):
        if "userId" not in self.sessionData:
            self.handleNotAuthorized()
            return
        db = VacationsDB()
        oneVacation = db.getOneVacation(vacation_id)

        if oneVacation != None:
            # response status code:
            self.send_response(200)
            # repsonse header:
            self.send_header("Content-Type", "application/json")
            # self.send_header(
            #    "Access-Control-Allow-Origin", self.headers["Origin"]
            # )
            # self.send_header("Set-Cookie", "flavor=biscoff")  # COOKIE
            self.end_headers()
            # response body
            self.wfile.write(bytes(json.dumps(oneVacation), "utf-8"))
        else:
            self.handleNotFound()

    # def handleGetUsersMember(self, user_id):
    #     db = UsersDB()
    #     oneUser = db.getOneUser(user_id)

    #     if oneUser != None:
    #         # response status code:
    #         self.send_response(200)
    #         # repsonse header:
    #         self.send_header("Content-Type", "application/json")
    #         # self.send_header(
    #         #   "Access-Control-Allow-Origin", self.headers["Origin"]
    #         # )
    #         self.end_headers()
    #         # response body
    #         self.wfile.write(bytes(json.dumps(oneUser), "utf-8"))
    #     else:
    #         self.handleNotFound()

    def handleDeleteVacationMember(self, vacation_id):
        if "userId" not in self.sessionData:
            self.handleNotAuthorized()
            return
        db = VacationsDB()
        oneVacation = db.deleteOneVacation(vacation_id)

        if oneVacation == True:
            # response status code:
            self.send_response(200)
            # repsonse header:
            self.send_header("Content-Type", "application/json")
            # self.send_header(
            #   "Access-Control-Allow-Origin", self.headers["Origin"]
            # )
            self.end_headers()
            # response body
            self.wfile.write(bytes("Deleted", "utf-8"))
        else:
            self.handleNotFound()

    # def handleDeleteUserMember(self, user_id):
    #     db = UsersDB()
    #     oneUser = db.deleteOneUser(user_id)

    #     if oneUser == True:
    #         # response status code:
    #         self.send_response(200)
    #         # repsonse header:
    #         self.send_header("Content-Type", "application/json")
    #         # self.send_header(
    #         #    "Access-Control-Allow-Origin", self.headers["Origin"]
    #         # )
    #         self.end_headers()
    #         # response body
    #         self.wfile.write(bytes("Deleted", "utf-8"))
    #     else:
    #         self.handleNotFound()

    def handleCreateVacation(self):
        if "userId" not in self.sessionData:
            self.handleNotAuthorized()
            return
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
        # self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.end_headers()

    # check user exists
    def handleCreateUser(self):
        print("request headers:", self.headers)
        # read the data in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body", parsed_body)
        print("")
        # save user to the "database"
        user_fname = parsed_body["fname"][0]  # indexed in the value is a list
        user_lname = parsed_body["lname"][0]
        user_email = parsed_body["email"][0]
        user_pass = parsed_body["pass"][0]

        db = UsersDB()
        exists = db.createUser(
            user_fname,
            user_lname,
            user_email,
            user_pass,
        )

        if exists:
            # send a response
            self.send_response(201)  # successfully created\
            # self.send_header(
            #    "Access-Control-Allow-Origin", self.headers["Origin"]
            # )
            self.end_headers()
        else:
            self.send_response(422)  # successfully created\
            # self.send_header(
            #   "Access-Control-Allow-Origin", self.headers["Origin"]
            # )
            self.end_headers()

    def handleUpdateVacationMember(self, vacation_id):
        if "userId" not in self.sessionData:
            self.handleNotAuthorized()
            return
        print("request headers:", self.headers)
        # read the data in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body", parsed_body)

        if parsed_body == {}:
            self.handleNotFound()
            return
        # save user name to the "database"
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
            # self.send_header(
            #    "Access-Control-Allow-Origin", self.headers["Origin"]
            # )
            self.end_headers()
        else:
            self.handleNotFound()

    def handleUpdateUserMember(self, user_id):
        print("request headers:", self.headers)
        # read the data in the request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("parsed request body", parsed_body)

        if parsed_body == {}:
            self.handleNotFound()
            return
        # save user name to the "database"
        user_fname = parsed_body["fname"][0]  # indexed in the value is a list
        user_lname = parsed_body["lname"][0]
        user_email = parsed_body["email"][0]
        user_pass = parsed_body["pass"][0]

        db = UsersDB()
        exists = db.updateUser(
            user_fname, user_lname, user_email, user_pass, user_id
        )

        if exists:

            # send a response
            self.send_response(200)  # successfully created\
            # self.send_header(
            #    "Access-Control-Allow-Origin", self.headers["Origin"]
            # )
            self.end_headers()
        else:
            self.handleNotFound()

    def do_OPTIONS(self):
        self.loadSession()
        self.send_response(200)
        # self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header(
            "Access-Control-Allow-Methods", "GET,POST, PUT, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_DELETE(self):
        self.loadSession()
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
        elif collection_name == "users":
            if member_id:
                self.handleDeleteUserMember(member_id)
            else:
                self.handleNotFound()  # since this is delete/update we do 404 error
        else:
            self.handleNotFound()

    def do_GET(self):
        self.loadSession()
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
        # elif collection_name == "users":
        #     if member_id:
        #         self.handleGetUsersMember(member_id)
        #     else:
        #         self.handleGetUsersCollection()
        else:
            self.handleNotFound()

    def do_POST(self):
        self.loadSession()
        if self.path == "/vacations":
            self.handleCreateVacation()
        elif self.path == "/users":
            self.handleCreateUser()
        elif self.path == "/sessions":
            self.handleCreateSession()

        else:
            self.handleNotFound()

    def do_PUT(self):
        self.loadSession()
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
        elif collection_name == "users":
            if member_id:
                self.handleUpdateUserMember(member_id)
            else:
                self.handleNotFound()  # since this is delete/update we  do 404 error
        else:
            self.handleNotFound()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def run():
    db = VacationsDB()
    db.createVacationsTable()
    db.createUsersTable()
    db.createUsersTable()
    db = None  # disconnect from database

    port = 8080
    if "PORT" in os.environ:
        port = int(os.environ["PORT"])

    listen = ("0.0.0.0", port)
    server = ThreadedHTTPServer(listen, MyRequestHandler)
    print("Server running")
    server.serve_forever()


if __name__ == "__main__":
    run()
