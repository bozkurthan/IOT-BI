import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time

##MAIN CODE
broker_address = "127.0.0.1"
mesaj = "hello"
# broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1")  # create new instance
print("connecting to broker")

i = 0
while i < 10:
  publish.single("test","pub-C1-" + str(i),1,False,"localhost",1883)
  i += 1
  time.sleep(1)
