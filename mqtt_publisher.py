import paho.mqtt.client as paho, os, urlparse

# Define event callbacks
def on_connect(mosq, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

mqttc = paho.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
#url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
url_str = 'mqtt://ombvfphu:qIYIG5AwS85t@m11.cloudmqtt.com:19992'
url = urlparse.urlparse(url_str)

# Connect
mqttc.username_pw_set(url.username, url.password)
mqttc.connect(url.hostname, url.port)

# Publish a message
#mqttc.publish("hello/world", "my message 2", retain=True)

import RPi.GPIO as GPIO
from time import gmtime, strftime, sleep, mktime
import datetime

GPIO.setmode(GPIO.BOARD)

last_status = 0
last_updated_time = gmtime()

def get_time_diff_str():
  time_str = str(datetime.timedelta(seconds=mktime(gmtime()) - mktime(last_updated_time)))
  return time_str

def make_message(status):
  global last_status
  global last_updated_time
  time = get_time_diff_str() #strftime("%Y-%m-%d %H:%M:%S", gmtime())
  if status != last_status:
    last_status = status
    last_updated_time = gmtime()
  return 'Status: ' + str(status) + ' | Time since last changed: ' + time

def on_motion():
  mqttc.publish("pipong/status", make_message("IN USE"), retain=True)

def on_no_motion():
  mqttc.publish("pipong/status", make_message("NOT IN USE"), retain=True)

GPIO.setup(16, GPIO.IN)

mqttc.loop_start()
while True:
  i=GPIO.input(16)
  if i==0:
    on_no_motion()
  if i==1:
    on_motion()
  sleep(1)
