====================
dalchymia for python
====================

This is libraries for using dalchymia M2M platform service.

Please sign in to http://dalchymia.net/ and get parameters to upload sensed data to dalchymia.

Features
========

- datastore(REST client)
- datastore(MQTT client)

Dependencies
============

This library has dependency with some existed python packages. Please install them before using dalchymia.

| $ pip install requests
| $ pip install mosquitto


Installation
============

dalchymia has already registered on PyPi.
To install dalchymia, simply:

| $ pip install dalchymia

Or

| $ easy_install dalchymia


Documentation
=============

Documentation is available at http://docs.dalchymia.net/.

How to use?
===========

There are 2 ways you can choose to store data.

1. MQTT(MQ Telemetry Transport)
  MQTT is desined for constrained embedded devices. It is a publish/subscribe, extermely simple and lightweight messaging protodocl. 

2. HTTP(RESTful)
  HTTP is the most well-known protocol. It is easy to deployment to applications with exists libraries and frameworks.

Please use RESTful API in HTTP as long as your application doesn't need to store data in realtime.


And also, both clients use same JSON format as follows:

[
  "t" : "1390199481.371757",
  "d" : [
    { "id" : "7f0000000000002a96467812819b11e3", "v" : "23.9" },
    { "id" : "7f0000000000002a96474fda819b11e3", "v" : "80.0" }
  ]
]
  

usage:

1. Define parameters.

root_device_id = "7f0000000000002a96467812819b11e3"
device_id = ["7f0000000000002a96467812819b11e3", "7f0000000000002a96474fda819b11e3"]
product_hash_key = "0e33b56487d0956d7f65412fecd3a43e91f0012b08c26070104fc6875d5075bc"

2. Compose payload

Tere are 2 devices for data store.

# define instance
data = storeformat()

# get timestamp, values
timestamp = str(time.mktime(datetime.datetime.now().timetuple()))
v_data1 = str(random.randint(1,100))
v_data2 = str(random.randint(1000,2000))

# append values to 
data.appendvalue(device_id[0], v_data1)
data.appendvalue(device_id[1], v_data2)
data.appendrow(timestamp, data.data)

# get json format
body = data.getjson()

3.Store data

-MQTT

conn = mqttclient()
conn.connect()
conn.publish(root_device_id, body)
conn.disconnect()

-HTTP(RESTful)
conn = httpclient(product_hash_key, root_device_id)
res =  conn.store(body)



