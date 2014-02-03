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

#: Generate value at random, and compose body message
data = storeformat()
now = time.mktime(datetime.datetime.now().timetuple())
timestamp = str(now)
v_data1 = str(random.randint(1,100))

#: Compose payload
data.appendvalue(device_id[0], v_data1)
data.appendrow(timestamp, data.data)
payload = data.getjson()

#: Publish message (datastore)
conn = mqttclient(root_device_id)
conn.connect()
conn.publish(payload)
conn.disconnect()

