import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time, sys, argparse, math
global mesaj






def on_message1(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    mesaj = str(message.payload.decode("utf-8"))
    print(mesaj)


##MAIN CODE
broker_address = "127.0.0.1"
mesaj = "hello"
# broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1")  # create new instance
print("connecting to broker")

publish.single("test","hello2",1,False,"localhost",1883)

client.connect(broker_address)  # connect to broker
client.subscribe("test4563")

while (1):
    client.loop_start()  # start the loop
    # attach function to callback
    client.on_message = on_message1
    client.loop_stop()  # stop the loop