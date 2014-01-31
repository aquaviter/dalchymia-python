#!/usr/bin/python
# _*_ coding: utf-8 _*_

import sys
sys.path.append('../dalchymia')

from store import mqttclient, storeformat
import time
import datetime
import random


#: Device id for dalmon
root_device_id = "7f000000000000251c7e9e24609411e3"
device_id = ["7f000000000000251c7f7f10609411e3"]

#: MQTT Parameters
mqtt_broker = "mq.dalchymia.net"
mqtt_port = 1883
base_topic = "api/v2/store"
topic = base_topic + "/" + root_device_id

#: delay time while checking datastore
delay = 5

#: Response record limit
limit = 10
    
#: Generate value at random, and compose body message
data = storeformat()
now = time.mktime(datetime.datetime.now().timetuple())
timestamp = str(now)
v_data1 = str(random.randint(1,100))
    
data.appendvalue(device_id[0], v_data1)
data.appendrow(timestamp, data.data)
body = data.getjson()

print "===================================="
print "server:\t\t%s" % (mqtt_broker)
print "topic:\t\t%s" % (topic)
print "body:\n%s" % (body)
print "===================================="

#: Publish message (datastore)
conn = mqttclient()
conn.connect()
conn.publish(topic, body)
conn.disconnect()

