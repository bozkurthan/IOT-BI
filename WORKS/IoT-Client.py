import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time, sys, argparse, math

global sub_message

#pragma
client_ID = "CC0"
_client_will_sub = True
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
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    if "L1-C1" in sub_message:
        print("L1A")
        if "NaN" in sub_message:
            if (_client_has_model):
                print("Model algorithm.")
            else:
                print("NaN value found but pass that directly publish.")
        else:
            print("No NaN value, so directly publish.")

    elif "L1-C2" in sub_message:
        print("L1B")
        # dataTn(deger1, deger2, zamanbilgi)

    elif "L1-C3" in sub_message:
        print("L1C")
        # dataLn(deger1, deger2, zamanbilgi)

    elif "L2-C1" in sub_message:
        print("L2A")
        # dataH2(deger1, deger2, zamanbilgi)

    elif "L2-C2" in sub_message:
        print("L2B")
        # dataT2(deger1, deger2, zamanbilgi)

    elif "L2-C3" in sub_message:
        print("L2C")
        # dataL2(deger1, deger2, zamanbilgi)
    else:
        print("Problem occured.")

    publish.single(client_pub_topic, sub_message, 1, False, pub_broker_address, pub_broker_port)

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
        model_log_file = open("model_log_file.txt", "w")
        model_log_file.write("Model isletim sureleri (milisaniye)***\n")

        i = 0
        while (i < publish_size):
            model_start_time = time.time() * 1000

            # BURADA MODEL İŞLETİLECEK VE SONUCU data_message değişkenelerine işlenecek.

            data_message1 = "37.511"  # Bu mesaj model sonunda elde edilen değerdir
            data_message2 = "52.87946"  # Bu mesaj model sonunda elde edilen değerdir
            data_message3 = "33333"  # Bu mesaj model sonunda elde edilen değerdir

            time.sleep(2)
            model_end_time = time.time() * 1000
            final_time = model_end_time - model_start_time

            model_log_file.write(str(final_time) +"\n")

            publish_message = "(" + location_number + "-" + client_number + "-" + str(i) + ".Paket),(" + str(time.time() * 1000) + "),(" + data_message1 + "," +data_message2 + ","+ data_message3 + ")"

            publish.single(client_pub_topic, publish_message, 1, False, pub_broker_address, pub_broker_port)

            #Delay time
            time.sleep(1)
            i = i + 1
        model_log_file.close()



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

