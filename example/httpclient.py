#!/usr/bin/python
# _*_ coding: utf-8 _*_

import sys
sys.path.append('../dalchymia')

from store import httpclient, storeformat
import time
import datetime
import random

def str2epoch(str):
    return time.mktime(time.strptime(str, "%Y-%m-%dT%H:%M:%S"))


# define device parameters
root_device_id = "7f0000000000002a96467812819b11e3"
device_id = ["7f0000000000002a96467812819b11e3", "7f0000000000002a96474fda819b11e3"]
product_hash_key = "0e33b56487d0956d7f65412fecd3a43e91f0012b08c26070104fc6875d5075bc"

# generate current timestamp and random values
timestamp = str(time.mktime(datetime.datetime.now().timetuple()))
v_data1 = str(random.randint(1,100))
v_data2 = str(random.randint(1000,2000))

# compose sending data (JSON format)
data = storeformat()
data.appendvalue(device_id[0], v_data1)
data.appendvalue(device_id[1], v_data2)
data.appendrow(timestamp, data.data)
body = data.getjson()

# data store by using HTTP
conn = httpclient(product_hash_key, root_device_id)
res =  conn.store(body)
print res.text
