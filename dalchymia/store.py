#!/usr/bin/python
# _*_ coding: utf-8 _*_

"""

store.py
~~~~~~~~

Copyright (c) 2014 Ubiquitous Corporation
Released under the MIT license

"""

import requests
import paho.mqtt.client as paho
import json
import time,datetime
import sys
import random
import Crypto.Cipher.AES
import Crypto.Hash.SHA256
import Crypto.Hash.HMAC
import binascii

api_base = 'https://api.dalchymia.net/api/v2'

class mqttclient:
    
    def __init__(self, root_device_id):
        self.server = "mq.dalchymia.net"
        self.port = 1883
        self.keepalive = 60
        self.basetopic = 'api/v2/store'
        self.root_device_id = root_device_id
        self.topic = self.basetopic + "/" + self.root_device_id
        self.client = paho.Client(self.root_device_id)

        def on_connect(mosq, obj, rc):
            print("rc: " + str(rc))

        def on_message(mosq, obj, msg):
            print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

        def on_publish(mosq, obj, mid):
            print("mid: " + str(mid))

        def on_disconnect(mosq, obj, rc):
            print("disconnected successfully.")

        self.client.on_connect = on_connect
        self.client.on_publish = on_publish
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect

    def connect(self):
        self.client.connect(self.server, self.port, self.keepalive)

    def publish(self, payload):
        #print "Publish %s : %s" % (topic, payload)
        self.client.publish(self.topic, payload, retain=False, qos=0)
            
    def disconnect(self):
        self.client.disconnect()

class httpclient:

    def __init__(self, hash_key, root_device_id):
        self.api_store = api_base + '/fw/store'
        self.hash_key = hash_key
        self.root_device_id = root_device_id
        print self.api_store

    def store(self, body):
        digest = Crypto.Hash.HMAC.new(binascii.a2b_hex(self.hash_key), body, Crypto.Hash.SHA256)
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'x-sha256-digest': digest.hexdigest(),
                   'x-root-device-id': self.root_device_id
                   }
        return requests.post(self.api_store, headers=headers, data=body)
    
class storeformat:
    def __init__(self):
        self.data = []
        self.row = {}
        self.base = []

    def appendvalue(self, device_id, value):
        self.data.append({"id":device_id, "v":value})
        return self.data

    def resetvalue(self):
        self.data = []

    def appendrow(self, timestamp, data):
        self.row['t'] = timestamp
        self.row['d'] = data
        self.base.append(self.row)

    def resetrow(self):
        self.row = {}

    def getjson(self):
        return json.dumps(self.base)

