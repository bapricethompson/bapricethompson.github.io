#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 12:27:36 2023

@author: brooklynprice
"""
import os, base64

# data organized as a dictionary of dictionaries


class SessionStore:
    def __init__(self):
        # a dictionary of dictionaries, one per session
        self.sessions = {}

    def createSession(self):
        # create a new session dictionary, add to self.sessions
        # assign new session to a new session ID
        sessionId = self.generateSessionId()
        self.sessions[sessionId] = {}
        return sessionId

    def generateSessionId(self):
        # return a new session ID that is
        # 1. random
        # 2. unique
        # 3. unguessable
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr

    def getSessionData(self, sessionId):
        # return the dictionary associated with the session ID
        # if it exists
        if sessionId in self.sessions:
            return self.sessions[sessionId]
        else:
            return None
