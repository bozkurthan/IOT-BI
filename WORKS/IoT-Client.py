import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time, sys, argparse, math
global mesaj

#pragma
_client_will_sub   = False
_client_has_model  = False

client_number   = "C1"
location_number = "L1"


sub_broker_address = "127.0.0.1"
sub_broker_port    = 1883
client_sub_topic   = "test"


pub_broker_address = "127.0.0.1"
pub_broker_port    = 1883
client_pub_topic   = "test3"
publish_size = 15



def on_message1(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    mesaj = str(message.payload.decode("utf-8"))
    print(mesaj)
    publish.single(client_pub_topic, mesaj, 1, False, pub_broker_address, pub_broker_port)

def client_sub_pub ():
    print("This client will be run for publishing and subscribing. \n ")

    client = mqtt.Client("P1")  # create new instance
    print("connecting to broker")


    client.connect(sub_broker_address)  # connect to broker
    client.subscribe(client_sub_topic)
    while (1):
        client.loop_start()  # start the loop
        # attach function to callback
        client.on_message = on_message1
        client.loop_stop()  # stop the loop



def client_pub ():
    print("This client will be run for only publishing. \n ")
    client = mqtt.Client("P1")  # create new instance
    if(_client_has_model):
        print("Model message process")
        i = 0
        while (i < publish_size):
            data_message1= "37.511"   #Bu mesaj csv dosyasından alınacak yoksa NaN yazılacak IBRAHIM HOCA
            data_message2= "52.87946" #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA
            data_message3= "NaN"      #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA

            publish_message = "(" + location_number + "-" + client_number + "-" + str(i) + ".Paket),(" + str(time.time() * 1000) + "),(" + data_message1 + "," +data_message2 + ","+ data_message3 + ")"

            publish.single(client_pub_topic, publish_message, 1, False, pub_broker_address, pub_broker_port)

            time.sleep(1)
            i = i + 1
    else:
        print("Without model message process")
        i=0
        while (i<publish_size):
            data_message1= "37.511"   #Bu mesaj csv dosyasından alınacak yoksa NaN yazılacak IBRAHIM HOCA
            data_message2= "52.87946" #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA
            data_message3= "NaN"      #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA

            publish_message = "( (" + location_number + "-" + client_number + "-" + str(i) + ".Paket), (" + str(time.time() * 1000) + "), ( ( Data: (Light: " + data_message1 + ", Humidity: " + data_message2 + ", Temperature:" + data_message3 + ") ) )"

            publish.single(client_pub_topic, publish_message, 1, False, pub_broker_address, pub_broker_port)

            time.sleep(1)
            i = i + 1









if(_client_will_sub):
    client_sub_pub()
else:
    client_pub()

print("allover")

