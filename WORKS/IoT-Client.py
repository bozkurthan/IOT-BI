# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time, sys, argparse, math
from numpy import long
import os

global sub_message

# pragma CONFIG
client_ID = "CC0"
_client_will_sub = True
_client_has_model = True

test_packet_length = 10

sub_broker_address = "127.0.0.1"
sub_broker_port = 1883
client_sub_topic = "test-cloud"

pub_broker_address = "127.0.0.1"
pub_broker_port = 1883
client_pub_topic = "test-server"
publish_delay_time = 0.2
publish_size = 100
client_number = "C1"
location_number = "L1"

dir_name = "data_log"
log_dir = os.getcwd()
log_dir = log_dir + "/" + dir_name + "/"
os.mkdir(log_dir)



##INCOMING MESSAGE TRANSMISSION TIME LOG DEFINITIONS
total_packet_tx_time_L1_C1 = 0
total_packet_tx_time_L1_C2 = 0
total_packet_tx_time_L1_C3 = 0
total_packet_tx_time_L2_C1 = 0
total_packet_tx_time_L2_C2 = 0
total_packet_tx_time_L2_C3 = 0

total_packet_size_L1_C1 = 0
total_packet_size_L1_C2 = 0
total_packet_size_L1_C3 = 0
total_packet_size_L2_C1 = 0
total_packet_size_L2_C2 = 0
total_packet_size_L2_C3 = 0

packet_counter_L1_C1 = 1
packet_counter_L1_C2 = 1
packet_counter_L1_C3 = 1
packet_counter_L2_C1 = 1
packet_counter_L2_C2 = 1
packet_counter_L2_C3 = 1

##MODEL TIME LOG DEFINITIONS
total_model_proc_time_L1_C1 = 0
total_model_proc_time_L1_C2 = 0
total_model_proc_time_L1_C3 = 0
total_model_proc_time_L2_C1 = 0
total_model_proc_time_L2_C2 = 0
total_model_proc_time_L2_C3 = 0

_mpacket_counter_L1_C1 = 1
_mpacket_counter_L1_C2 = 1
_mpacket_counter_L1_C3 = 1
_mpacket_counter_L2_C1 = 1
_mpacket_counter_L2_C2 = 1
_mpacket_counter_L2_C3 = 1





def incoming_data_log_cfg_tx_time(packet_header, end_time, packet_size):
    global packet_counter_L1_C1
    global packet_counter_L1_C2
    global packet_counter_L1_C3
    global packet_counter_L2_C1
    global packet_counter_L2_C2
    global packet_counter_L2_C3

    global total_packet_tx_time_L1_C1
    global total_packet_tx_time_L1_C2
    global total_packet_tx_time_L1_C3
    global total_packet_tx_time_L2_C1
    global total_packet_tx_time_L2_C2
    global total_packet_tx_time_L2_C3

    global total_packet_size_L1_C1
    global total_packet_size_L1_C2
    global total_packet_size_L1_C3
    global total_packet_size_L2_C1
    global total_packet_size_L2_C2
    global total_packet_size_L2_C3


    if "L1-C1" in packet_header:
        if (packet_counter_L1_C1 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L1C1.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L1_C1) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L1C1.txt", "a")
            model_size_log_file.write(str(total_packet_size_L1_C1) + "\n")
            model_size_log_file.close()
            packet_counter_L1_C1 = 1
            total_packet_tx_time_L1_C1 = 0
            total_packet_size_L1_C1 = 0
        else:
            total_packet_tx_time_L1_C1 = total_packet_tx_time_L1_C1 + (long(time.time() * 1000) - long(end_time))
            total_packet_size_L1_C1 = total_packet_size_L1_C1 + packet_size
            packet_counter_L1_C1 = packet_counter_L1_C1 + 1
    elif "L1-C2" in packet_header:
        if (packet_counter_L1_C2 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L1C2.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L1_C2) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L1C2.txt", "a")
            model_size_log_file.write(str(total_packet_size_L1_C2) + "\n")
            model_size_log_file.close()
            packet_counter_L1_C2 = 1
            total_packet_tx_time_L1_C2 = 0
            total_packet_size_L1_C2 = 0
        else:
            total_packet_tx_time_L1_C2 = total_packet_tx_time_L1_C2 + (long(time.time() * 1000) - long(end_time))
            packet_counter_L1_C2 = packet_counter_L1_C2 + 1
    elif "L1-C3" in packet_header:
        if (packet_counter_L1_C3 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L1C3.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L1_C3) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L1C3.txt", "a")
            model_size_log_file.write(str(total_packet_size_L1_C3) + "\n")
            model_size_log_file.close()
            packet_counter_L1_C3 = 1
            total_packet_tx_time_L1_C3 = 0
            total_packet_size_L1_C3 = 0
        else:
            total_packet_tx_time_L1_C3 = total_packet_tx_time_L1_C3 + (long(time.time() * 1000) - long(end_time))
            packet_counter_L1_C3 = packet_counter_L1_C3 + 1
    elif "L2-C1" in packet_header:
        if (packet_counter_L2_C1 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L2C1.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L2_C1) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L2C1.txt", "a")
            model_size_log_file.write(str(total_packet_size_L2_C1) + "\n")
            model_size_log_file.close()
            packet_counter_L2_C1 = 1
            total_packet_tx_time_L2_C1 = 0
            total_packet_size_L2_C1 = 0
        else:
            total_packet_tx_time_L2_C1 = total_packet_tx_time_L2_C1 + (long(time.time() * 1000) - long(end_time))
            packet_counter_L2_C1 = packet_counter_L2_C1 + 1
    elif "L2-C2" in packet_header:
        if (packet_counter_L2_C2 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L2C2.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L2_C2) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L2C2.txt", "a")
            model_size_log_file.write(str(total_packet_size_L2_C2) + "\n")
            model_size_log_file.close()
            packet_counter_L2_C2 = 1
            total_packet_tx_time_L2_C2 = 0
            total_packet_size_L2_C2 = 0
        else:
            total_packet_tx_time_L2_C2 = total_packet_tx_time_L2_C2 + (long(time.time() * 1000) - long(end_time))
            packet_counter_L2_C2 = packet_counter_L2_C2 + 1
    elif "L2-C3" in packet_header:
        if (packet_counter_L2_C3 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L2C3.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L2_C3) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L2C3.txt", "a")
            model_size_log_file.write(str(total_packet_size_L2_C3) + "\n")
            model_size_log_file.close()
            packet_counter_L2_C3 = 1
            total_packet_tx_time_L2_C3 = 0
            total_packet_size_L2_C3 = 0
        else:
            total_packet_tx_time_L2_C3 = total_packet_tx_time_L2_C3 + (long(time.time() * 1000) - long(end_time))
            packet_counter_L2_C3 = packet_counter_L2_C3 + 1
    else:
        print("Problem in data_log_cfg_tx_time")

def data_log_model_time(packet_header, end_time):
    global _mpacket_counter_L1_C1
    global _mpacket_counter_L1_C2
    global _mpacket_counter_L1_C3
    global _mpacket_counter_L2_C1
    global _mpacket_counter_L2_C2
    global _mpacket_counter_L2_C3

    global total_model_proc_time_L1_C1
    global total_model_proc_time_L1_C2
    global total_model_proc_time_L1_C3
    global total_model_proc_time_L2_C1
    global total_model_proc_time_L2_C2
    global total_model_proc_time_L2_C3

    if "L1-C1" in packet_header:
        if (_mpacket_counter_L1_C1 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L1C1.txt", "a")
            model_log_file.write(str(total_model_proc_time_L1_C1) + "\n")
            model_log_file.close()
            _mpacket_counter_L1_C1 = 1
            total_model_proc_time_L1_C1 = 0
        else:
            total_model_proc_time_L1_C1 = total_model_proc_time_L1_C1 + (long(time.time() * 1000) - long(end_time))
            _mpacket_counter_L1_C1 = _mpacket_counter_L1_C1 + 1
    elif "L1-C2" in packet_header:
        if (_mpacket_counter_L1_C2 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L1C2.txt", "a")
            model_log_file.write(str(total_model_proc_time_L1_C2) + "\n")
            model_log_file.close()
            _mpacket_counter_L1_C2 = 1
            total_model_proc_time_L1_C2 = 0
        else:
            total_model_proc_time_L1_C2 = total_model_proc_time_L1_C2 + (long(time.time() * 1000) - long(end_time))
            _mpacket_counter_L1_C2 = _mpacket_counter_L1_C2 + 1
    elif "L1-C3" in packet_header:
        if (_mpacket_counter_L1_C3 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L1C3.txt", "a")
            model_log_file.write(str(total_model_proc_time_L1_C3) + "\n")
            model_log_file.close()
            _mpacket_counter_L1_C3 = 1
            total_model_proc_time_L1_C3 = 0
        else:
            total_model_proc_time_L1_C3 = total_model_proc_time_L1_C3 + (long(time.time() * 1000) - long(end_time))
            _mpacket_counter_L1_C3 = _mpacket_counter_L1_C3 + 1
    elif "L2-C1" in packet_header:
        if (_mpacket_counter_L2_C1 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L2C1.txt", "a")
            model_log_file.write(str(total_model_proc_time_L2_C1) + "\n")
            model_log_file.close()
            _mpacket_counter_L2_C1 = 1
            total_model_proc_time_L2_C1 = 0
        else:
            total_model_proc_time_L2_C1 = total_model_proc_time_L2_C1 + (long(time.time() * 1000) - long(end_time))
            _mpacket_counter_L2_C1 = _mpacket_counter_L2_C1 + 1
    elif "L2-C2" in packet_header:
        if (_mpacket_counter_L2_C2 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L2C2.txt", "a")
            model_log_file.write(str(total_model_proc_time_L2_C2) + "\n")
            model_log_file.close()
            _mpacket_counter_L2_C2 = 1
            total_model_proc_time_L2_C2 = 0
        else:
            total_model_proc_time_L2_C2 = total_model_proc_time_L2_C2 + (long(time.time() * 1000) - long(end_time))
            _mpacket_counter_L2_C2 = _mpacket_counter_L2_C2 + 1
    elif "L2-C3" in packet_header:
        if (_mpacket_counter_L2_C3 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L2C3.txt", "a")
            model_log_file.write(str(total_model_proc_time_L2_C3) + "\n")
            model_log_file.close()
            _mpacket_counter_L2_C3 = 1
            total_model_proc_time_L2_C3 = 0
        else:
            total_model_proc_time_L2_C3 = total_model_proc_time_L2_C3 + (long(time.time() * 1000) - long(end_time))
            _mpacket_counter_L2_C3 = _mpacket_counter_L2_C3 + 1
    else:
        print("Problem in data_log_model_time")

def data_process_to_pub(sub_message):
    if "NaN" in sub_message:
        if (_client_has_model):
            print("NaN value found. Processing AI.")
            raw_data_info, raw_data_sensors = sub_message.split("Data: (")
            before_time, message_time = raw_data_info.split("[")
            message_time, unused = message_time.split("]")
            packet_header = before_time.replace("( ", "").replace(" ", "")
            incoming_data_log_cfg_tx_time(packet_header, message_time, sub_message.__sizeof__())
            print(packet_header)
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
                data_log_model_time(packet_header, start_time)
            elif (humidity_data == "NaN"):
                start_time = long(time.time() * 1000)
                # Burada model işleyecek
                data_message1 = light_data  # Bu mesaj model sonunda elde edilen değerdir
                data_message2 = "22.22"  # Bu mesaj model sonunda elde edilen değerdir
                data_message3 = temperature_data  # Bu mesaj model sonunda elde edilen değerdir
                data_log_model_time(packet_header, start_time)
            elif (temperature_data == "NaN"):
                # Burada model işleyecek
                start_time = long(time.time() * 1000)
                data_message1 = light_data  # Bu mesaj model sonunda elde edilen değerdir
                data_message2 = humidity_data  # Bu mesaj model sonunda elde edilen değerdir
                data_message3 = "33.33"  # Bu mesaj model sonunda elde edilen değerdir
                data_log_model_time(packet_header, start_time)
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
            incoming_data_log_cfg_tx_time(time_first, message_time, sub_message.__sizeof__())
            new_message = time_first + "[" + str(long(time.time() * 1000)) + "]" + time_last
            publish.single(client_pub_topic, new_message, 1, False, pub_broker_address, pub_broker_port)
    else:
        # These code snippet provides that it handles time by incoming messages and saves them to file.
        # After this operation, it prepares new message.
        print("No NaN value, so directly publish.")
        time_first, message_time = sub_message.split("[")
        message_time, unused = message_time.split("]")
        unused, time_last = sub_message.split("]")
        incoming_data_log_cfg_tx_time(time_first, message_time, sub_message.__sizeof__())
        new_message = time_first + "[" + str(long(time.time() * 1000)) + "]" + time_last
        publish.single(client_pub_topic, new_message, 1, False, pub_broker_address, pub_broker_port)


def callback_on_message(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    data_process_to_pub(sub_message)

def client_sub_pub ():
    print("This client will be run for publishing and subscribing. \n ")

    client = mqtt.Client(client_ID)  # create new instance
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
    client = mqtt.Client(client_ID)  # create new instance


    if(_client_has_model):
        print("Model message process")
        i = 0
        while (i < publish_size):
            model_start_time = long(time.time() * 1000)

            # BURADA MODEL İŞLETİLECEK VE SONUCU data_message değişkenelerine işlenecek.

            data_message1 = "37.511"  # Bu mesaj model sonunda elde edilen değerdir
            data_message2 = "52.87946"  # Bu mesaj model sonunda elde edilen değerdir
            data_message3 = "33333"  # Bu mesaj model sonunda elde edilen değerdir
            data_log_model_time(location_number + "-" + client_number, model_start_time)
            publish_message = "(" + location_number + "-" + client_number + "-" + str(i) + ".Paket),(" + str(
                long(time.time() * 1000)) + "),(" + data_message1 + "," + data_message2 + "," + data_message3 + ")"

            publish.single(client_pub_topic, publish_message, 1, False, pub_broker_address, pub_broker_port)

            #Delay time
            time.sleep(publish_delay_time)
            i = i + 1



    else:
        print("Without model message process")
        i=0
        while (i<publish_size):
            data_message1= "37.511"   #Bu mesaj csv dosyasından alınacak yoksa NaN yazılacak IBRAHIM HOCA
            data_message2= "52.87946" #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA
            data_message3= "NaN"      #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA
            publish_message = "( (" + location_number + "-" + client_number + "-" + str(i) + ".Paket), (" + str(long(
                time.time() * 1000)) + "), ( ( Data: (Light: " + data_message1 + ", Humidity: " + data_message2 + ", Temperature:" + data_message3 + ") ) )"
            publish.single(client_pub_topic, publish_message, 1, False, pub_broker_address, pub_broker_port)

            time.sleep(publish_delay_time)
            i = i + 1

if(_client_will_sub):
    client_sub_pub()
else:
    client_pub()