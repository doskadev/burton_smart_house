#!/usr/bin/env python
from flask import *
import requests
import simplejson as json
import random
import time


class Device:
    """modal class for devices"""
    id = 0
    name = ""
    room = ""
    state = 0

    def __init__(self, id, name, room, state):
        self.id = id
        self.name = name
        self.room = room
        self.state = state

    def __repr__(self):
        return json.dumps({"id": self.id, "name": self.name, "room": self.room, "state": self.state})

    def getState(self):
        return self.state

    def getId(self):
        return self.id

    def updateState(self, newState):
        self.state = newState

    def verifyState(self, targetState):
        for i in range(80):
            p = {'DeviceNum': self.id, 'rand': random.random()}
            response = requests.get("http://192.168.1.88/port_3480/data_request?id=status&output_format=json", params=p)
            states = json.loads(response.__dict__['_content'])['Device_Num_' + str(self.id)]['states']

            for state in states:
                if state["variable"] == "Status":
                    self.state = state["value"]
            if self.state == str(targetState):
                return True
            else:
                time.sleep(0.3)
        return False

    def setState(self, targetState, serviceName):
        # set state
        p = {'serviceId': serviceName, 'DeviceNum': self.id, 'newTargetValue': targetState, 'rand': random.random()}
        response = requests.get(
            "http://192.168.1.88/port_3480/data_request?id=lu_action&output_format=json&action=SetTarget", params=p)

        # return response
        if "ERROR" not in response.__dict__['_content']:
            if self.verifyState(targetState):
                return True
            else:
                return jsonify(result="Error",
                               message="Switching state of " + str(self.name) + "(" + str(self.id) + ") has timed out")
        else:
            return jsonify(result="Error", message=response.__dict__['_content'])

