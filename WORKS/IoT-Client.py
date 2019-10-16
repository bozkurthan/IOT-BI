import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time, sys, argparse, math
from decimal import Decimal

from numpy import long

global sub_message

#pragma
client_ID = "CC0"
_client_will_sub = True
_client_has_model = False
test_packet_length = 100
total_packet_tx_time = 0
total_packet_size = 0



sub_broker_address = "127.0.0.1"
sub_broker_port    = 1883
client_sub_topic   = "test"


pub_broker_address = "127.0.0.1"
pub_broker_port    = 1883
client_pub_topic   = "test3"
publish_size = 15
client_number = "C1"
location_number = "L1"


def incoming_data_log_cfg_tx_time(packet_header, end_time, packet_size):
    if (packet_header == "L1-C1"):
        model_log_file = open("transmission_time_hoop-L1C1.txt", "a")
        model_log_file.write(str(long(time.time()) * 1000 - long(end_time)) + "\n")
        model_log_file.close()
    elif (packet_header == "L1-C2"):
        model_log_file = open("transmission_time_hoop-L1C2.txt", "a")
        model_log_file.write(str(long(time.time()) * 1000 - long(end_time)) + "\n")
        model_log_file.close()
    elif (packet_header == "L1-C3"):
        model_log_file = open("transmission_time_hoop-L1C3.txt", "a")
        model_log_file.write(str(long(time.time()) * 1000 - long(end_time)) + "\n")
        model_log_file.close()
    elif (packet_header == "L2-C1"):
        model_log_file = open("transmission_time_hoop-L2C1.txt", "a")
        model_log_file.write(str(long(time.time()) * 1000 - long(end_time)) + "\n")
        model_log_file.close()
    elif (packet_header == "L2-C2"):
        model_log_file = open("transmission_time_hoop-L2C2.txt", "a")
        model_log_file.write(str(long(time.time()) * 1000 - long(end_time)) + "\n")
        model_log_file.close()
    elif (packet_header == "L2-C3"):
        model_log_file = open("transmission_time_hoop-L2C3.txt", "a")
        model_log_file.write(str(long(time.time()) * 1000 - long(end_time)) + "\n")
        model_log_file.close()
    else:
        print("Problem in data_log_cfg_tx_time")


def data_log_model_time(packet_header, end_time):
    if (packet_header == "L1-C1"):
        log_file = open("model_proc_time-L1C1.txt", "a")
        log_file.write(str(end_time) + "\n")
        log_file.close()
    elif (packet_header == "L1-C2"):
        log_file = open("model_proc_time-L1C2.txt", "a")
        log_file.write(str(end_time) + "\n")
        log_file.close()
    elif (packet_header == "L1-C3"):
        log_file = open("model_proc_time-L1C3.txt", "a")
        log_file.write(str(end_time) + "\n")
        log_file.close()
    elif (packet_header == "L2-C1"):
        log_file = open("model_proc_time-L2C1.txt", "a")
        log_file.write(str(end_time) + "\n")
        log_file.close()
    elif (packet_header == "L2-C2"):
        log_file = open("model_proc_time-L2C2.txt", "a")
        log_file.write(str(end_time) + "\n")
        log_file.close()
    elif (packet_header == "L2-C3"):
        log_file = open("model_proc_time-L2C3.txt", "a")
        log_file.write(str(end_time) + "\n")
        log_file.close()
    else:
        print("Problem in data_log_model_time")


def data_process_to_pub(sub_message):
    if "NaN" in sub_message:
        if (_client_has_model):
            raw_data_info, raw_data_sensors = sub_message.split("Data: (")
            before_time, message_time = raw_data_info.split("[")
            message_time, unused = message_time.split("]")
            packet_header = before_time.replace("( ", "").replace(" ", "")
            incoming_data_log_cfg_tx_time(packet_header, message_time, sub_message.__sizeof__())
            light_data, humidity_data, temperature_data = raw_data_sensors.split(",")
            light_data = light_data.replace("Light:", "")
            humidity_data = humidity_data.replace("Humidty:", "").replace(" ", "")
            temperature_data = temperature_data.replace("Temperature:", "").replace(" ", "").replace(")))", "")
            if (light_data == "NaN"):
                start_time = long(time.time() * 1000)
                # Burada model işleyecek
                data_message1 = "11.11"  # Bu mesaj model sonunda elde edilen değerdir
                data_message2 = humidity_data  # Bu mesaj model sonunda elde edilen değerdir
                data_message3 = temperature_data  # Bu mesaj model sonunda elde edilen değerdir
                end_time = long(time.time() * 1000) - start_time
                data_log_model_time(packet_header, end_time)
            elif (humidity_data == "NaN"):
                start_time = long(time.time() * 1000)
                # Burada model işleyecek
                data_message1 = light_data  # Bu mesaj model sonunda elde edilen değerdir
                data_message2 = "22.22"  # Bu mesaj model sonunda elde edilen değerdir
                data_message3 = temperature_data  # Bu mesaj model sonunda elde edilen değerdir
                end_time = long(time.time() * 1000) - start_time
                data_log_model_time(packet_header, end_time)
            elif (temperature_data == "NaN"):
                # Burada model işleyecek
                start_time = long(time.time() * 1000)
                data_message1 = light_data  # Bu mesaj model sonunda elde edilen değerdir
                data_message2 = humidity_data  # Bu mesaj model sonunda elde edilen değerdir
                data_message3 = "33.33"  # Bu mesaj model sonunda elde edilen değerdir
                end_time = long(time.time() * 1000) - start_time
                data_log_model_time(packet_header, end_time)
            else:
                print("Problem occured")

            new_message = packet_header + "[" + str(long(time.time() * 1000)) \
                          + "],(" + data_message1 + "," + data_message2 + "," + data_message3 + ")"
            publish.single(client_pub_topic, new_message, 1, False, pub_broker_address, pub_broker_port)
        else:
            # These code snippet provides that it handles time by incoming messages and saves them to file.
            # After this operation, it prepares new message.
            print("NaN value found but pass that directly publish.")
            time_first, message_time = sub_message.split("[")
            message_time, unused = message_time.split("]")
            unused, time_last = sub_message.split("]")
            model_log_file = open("unproc_tx_time.txt", "a")
            model_log_file.write(str(long(time.time() * 1000) - Decimal(message_time)) + "\n")
            model_log_file.close()
            new_message = time_first + "[" + str(time.time() * 1000) + "]" + time_last
            publish.single(client_pub_topic, new_message, 1, False, pub_broker_address, pub_broker_port)
    else:
        # These code snippet provides that it handles time by incoming messages and saves them to file.
        # After this operation, it prepares new message.
        print("No NaN value, so directly publish.")
        time_first, message_time = sub_message.split("[")
        message_time, unused = message_time.split("]")
        unused, time_last = sub_message.split("]")
        incoming_data_log_cfg_tx_time(time_first, message_time, sub_message.__sizeof__())
        new_message = time_first + "[" + str(time.time() * 1000) + "]" + time_last
        publish.single(client_pub_topic, new_message, 1, False, pub_broker_address, pub_broker_port)


def callback_on_message(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    data_process_to_pub(sub_message)



def client_sub_pub ():
    print("This client will be run for publishing and subscribing. \n ")

    client = mqtt.Client("P1")  # create new instance
    print("connecting to broker")

    client.connect(sub_broker_address)  # connect to broker
    client.subscribe(client_sub_topic)
    while (1):
        client.loop_start()  # start the loop
        # attach function to callback
        client.on_message = callback_on_message
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