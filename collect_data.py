#!/<path-to>/python
"""python code to connect to the things network PI to collect data and send it to the database for storage
Author: Bontle Mere
"""
# import the required libraries
import json
import base64
import datetime as dt
import mysql.connector
import paho.mqtt.client as mqtt

#the following are required to connect to the APi and are found on the things network console
APPEUI = "70B3D57ED0022F9E"
APPID  = "thusang"
PSW    = 'ttn-account-v2.DMO9iviCnnPDk_12Zig_NnLhfowCV1_hltn3rF_7lG0'

# create mysql connector object to access the database
mydb = mysql.connector.connect(user = "nodepi", database="Bontle_database", passwd = "pi", host="196.42.78.200", port="3306")
mycursor = mydb.cursor()
# gives connection message
def on_connect(mqttc, mosq, obj,rc):
    print("Connected with result code:"+str(rc))
    # subscribe for all devices of user
    mqttc.subscribe('+/devices/+/up')

# gives message from device
def on_message(mqttc,obj,msg):
    try:
        #print(msg.payload)
        message = json.loads(msg.payload.decode('utf-8'))
        print(message)
        device_id = message["dev_id"]
        date_time = message['metadata']['time'].split("T")
        payload_raw = message["payload_raw"]
        device_reading = base64.b64decode(payload_raw).decode('utf-8')
        time_stamp = create_date(date_time)
        #print(message)
        gateways = message["metadata"]["gateways"]
        for gw in gateways:
           snr = gw["snr"]
           rssi = gw["rssi"]

        #print(device_id, device_reading, snr, rssi)
        #check the device id and store the data to the relevant table on the database
        if device_id == "soilmoisture":
           addMoisture(time_stamp, float(device_reading), float(snr), float(rssi))

        if device_id == "temperature":
           addTemperature(time_stamp, float(device_reading), float(snr), float(rssi))

    except Exception as e:
        print(e)
        pass

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc,obj,level,buf):
    print("message:" + str(buf))
    print("userdata:" + str(obj))

def create_date(date_time):
    """create a datetime object and return it"""
    year = date_time[0][0:4]
    month = date_time[0][5:7]
    day = date_time[0][8:]
    hour = date_time[1][0:2]
    minutes = date_time[1][3:5]
    seconds = date_time[1][6:len(date_time[1])-1]
    secs = int(float(seconds))
    microseconds = int((float(seconds) - secs) * 100000)
    time_stamp = dt.datetime(int(year), int(month), int(day), int(hour), int(minutes), secs, microseconds)
    return time_stamp

def addMoisture(time_stamp, device_reading, snr, rssi):
    """add the soil moisture reading to the table on the database"""

    sql = "INSERT INTO soil_moisture (time_stamp, moisture, snr, rssi) VALUES (%s, %s, %s, %s)"
    val = (time_stamp, device_reading, snr, rssi)
    mycursor.execute(sql, val)
    mydb.commit()
    #print("Here!")
def addTemperature(time_stamp, device_reading, snr, rssi):
    """add the temperature reading to the table on the database"""

    sql = "INSERT INTO temperature (time_stamp, temperature, snr, rssi) VALUES (%s, %s, %s, %s)"
    val = (time_stamp, device_reading, snr, rssi)
    mycursor.execute(sql, val)
    mydb.commit()
    #print("Here!")
#@def push_to_server():
mqttc= mqtt.Client()
# Assign event callbacks
mqttc.on_connect=on_connect
mqttc.on_message=on_message
mqttc.username_pw_set(APPID, PSW)
mqttc.connect("eu.thethings.network",1883,60)

# and listen to server
run = True
while run:
   mqttc.loop()
