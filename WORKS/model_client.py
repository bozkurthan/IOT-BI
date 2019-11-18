# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time, sys, argparse, math
from numpy import long
import os
# import warnings
import pandas as pd
import numpy as np
import tensorflow as tf
# import my_funcs as myf
from sklearn.preprocessing import MinMaxScaler
from time import sleep
from keras.models import load_model
import shutil

# model girdilerini almak için 2D bir dizi oluşturulsu- dolu değerleri bu diziliere alınıp modele verielcek


global sub_message

# pragma CONFIG
client_ID = "CC0"
_client_will_sub = False
_client_has_model = False

test_packet_length = 2

sub_broker_address = "192.168.1.103" # bu clientta etki etmıyor
sub_broker_port = 1883
client_sub_topic = "test1"

pub_broker_address = "192.168.1.41"
pub_broker_port = 1883
client_pub_topic = "test1"
publish_delay_time = 1.0
publish_size = 50
client_number = "C1"
location_number = "L1"
packet_name=location_number+ "-"+ client_number

dir_name = "data_log1"
log_dir = os.getcwd()
log_dir = log_dir + "/" + dir_name

if os.path.isdir(log_dir):
    print("File exist")
    shutil.rmtree(log_dir, ignore_errors=True)
    log_dir = log_dir + "/"
    os.mkdir(log_dir)
else:
    log_dir = log_dir + "/"
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

packet_counter_L1_C1 = 0
packet_counter_L1_C2 = 0
packet_counter_L1_C3 = 0
packet_counter_L2_C1 = 0
packet_counter_L2_C2 = 0
packet_counter_L2_C3 = 0

##MODEL TIME LOG DEFINITIONS
total_model_proc_time_L1_C1 = 0
total_model_proc_time_L1_C2 = 0
total_model_proc_time_L1_C3 = 0
total_model_proc_time_L2_C1 = 0
total_model_proc_time_L2_C2 = 0
total_model_proc_time_L2_C3 = 0

_mpacket_counter_L1_C1 = 0
_mpacket_counter_L1_C2 = 0
_mpacket_counter_L1_C3 = 0
_mpacket_counter_L2_C1 = 0
_mpacket_counter_L2_C2 = 0
_mpacket_counter_L2_C3 = 0

##PUBLISH MESSAGE PROCCESS LOG DEFINITIONS
total_message_proc_time_L1_C1 = 0
total_message_proc_time_L1_C2 = 0
total_message_proc_time_L1_C3 = 0
total_message_proc_time_L2_C1 = 0
total_message_proc_time_L2_C2 = 0
total_message_proc_time_L2_C3 = 0

_outgoing_total_packet_size_L1_C1 = 0
_outgoing_total_packet_size_L1_C2 = 0
_outgoing_total_packet_size_L1_C3 = 0
_outgoing_total_packet_size_L2_C1 = 0
_outgoing_total_packet_size_L2_C2 = 0
_outgoing_total_packet_size_L2_C3 = 0

publog_mpacket_counter_L1_C1 = 0
publog_mpacket_counter_L1_C2 = 0
publog_mpacket_counter_L1_C3 = 0
publog_mpacket_counter_L2_C1 = 0
publog_mpacket_counter_L2_C2 = 0
publog_mpacket_counter_L2_C3 = 0


## MODEL YÜKLEME BÖLÜMÜ
if (_client_has_model):
    print("- Loading Models and Graphs-")
    global Lmodel, Hmodel, Tmodel
    Hmodel = load_model('H_3_Wmodel.h5')
    Tmodel = load_model('T_3_Wmodel.h5')
    Lmodel = load_model('L_3_Wmodel.h5')

    global graph, graphT, graphL
    graphH = tf.get_default_graph()
    graphT = tf.get_default_graph()
    graphL = tf.get_default_graph()
    print("- Models and Graphs Loaded")

# def load_data():
#    global df
#    df= pd.read_excel('scaler.xlsx', sheetname='Scaler')
#    df=df.values.astype('float32')
#
#    global x_scaler,y_scaler
#    x_scaler = MinMaxScaler(feature_range=(0, 1))
#    y_scaler = MinMaxScaler(feature_range=(0, 1))


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
            model_log_file.write(str(total_packet_tx_time_L1_C1/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L1C1.txt", "a")
            model_size_log_file.write(str(total_packet_size_L1_C1/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L1_C1 = 0
            total_packet_tx_time_L1_C1 = 0
            total_packet_size_L1_C1 = 0
        #else:
        total_packet_tx_time_L1_C1 = total_packet_tx_time_L1_C1 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L1_C1 = total_packet_size_L1_C1 + packet_size
        packet_counter_L1_C1 = packet_counter_L1_C1 + 1
    elif "L1-C2" in packet_header:
        if (packet_counter_L1_C2 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L1C2.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L1_C2/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L1C2.txt", "a")
            model_size_log_file.write(str(total_packet_size_L1_C2/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L1_C2 = 0
            total_packet_tx_time_L1_C2 = 0
            total_packet_size_L1_C2 = 0
        #else:
        total_packet_tx_time_L1_C2 = total_packet_tx_time_L1_C2 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L1_C2 = total_packet_size_L1_C2 + packet_size
        packet_counter_L1_C2 = packet_counter_L1_C2 + 1
    elif "L1-C3" in packet_header:
        if (packet_counter_L1_C3 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L1C3.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L1_C3/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L1C3.txt", "a")
            model_size_log_file.write(str(total_packet_size_L1_C3/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L1_C3 = 0
            total_packet_tx_time_L1_C3 = 0
            total_packet_size_L1_C3 = 0
       #else:
        total_packet_tx_time_L1_C3 = total_packet_tx_time_L1_C3 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L1_C3 = total_packet_size_L1_C3 + packet_size
        packet_counter_L1_C3 = packet_counter_L1_C3 + 1
    elif "L2-C1" in packet_header:
        if (packet_counter_L2_C1 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L2C1.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L2_C1/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L2C1.txt", "a")
            model_size_log_file.write(str(total_packet_size_L2_C1/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L2_C1 = 0
            total_packet_tx_time_L2_C1 = 0
            total_packet_size_L2_C1 = 0
       # else:
        total_packet_tx_time_L2_C1 = total_packet_tx_time_L2_C1 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L2_C1 = total_packet_size_L2_C1 + packet_size
        packet_counter_L2_C1 = packet_counter_L2_C1 + 1
    elif "L2-C2" in packet_header:
        if (packet_counter_L2_C2 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L2C2.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L2_C2/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L2C2.txt", "a")
            model_size_log_file.write(str(total_packet_size_L2_C2/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L2_C2 = 0
            total_packet_tx_time_L2_C2 = 0
            total_packet_size_L2_C2 = 0
        #else:
        total_packet_tx_time_L2_C2 = total_packet_tx_time_L2_C2 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L2_C2 = total_packet_size_L2_C2 + packet_size
        packet_counter_L2_C2 = packet_counter_L2_C2 + 1
    elif "L2-C3" in packet_header:
        if (packet_counter_L2_C3 == test_packet_length):
            model_log_file = open(log_dir + "transmission_time_hoop-L2C3.txt", "a")
            model_log_file.write(str(total_packet_tx_time_L2_C3/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "packet_size_hoop-L2C3.txt", "a")
            model_size_log_file.write(str(total_packet_size_L2_C3/test_packet_length) + "\n")
            model_size_log_file.close()
            packet_counter_L2_C3 = 0
            total_packet_tx_time_L2_C3 = 0
            total_packet_size_L2_C3 = 0
        #else:
        total_packet_tx_time_L2_C3 = total_packet_tx_time_L2_C3 + (long(time.time() * 1000) - long(end_time))
        total_packet_size_L2_C3 = total_packet_size_L2_C3 + packet_size
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
            model_log_file.write(str(total_model_proc_time_L1_C1/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L1_C1 = 0
            total_model_proc_time_L1_C1 = 0
        #else:
        total_model_proc_time_L1_C1 = total_model_proc_time_L1_C1 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L1_C1 = _mpacket_counter_L1_C1 + 1
    elif "L1-C2" in packet_header:
        if (_mpacket_counter_L1_C2 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L1C2.txt", "a")
            model_log_file.write(str(total_model_proc_time_L1_C2/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L1_C2 = 0
            total_model_proc_time_L1_C2 = 0
        #else:
        total_model_proc_time_L1_C2 = total_model_proc_time_L1_C2 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L1_C2 = _mpacket_counter_L1_C2 + 1
    elif "L1-C3" in packet_header:
        if (_mpacket_counter_L1_C3 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L1C3.txt", "a")
            model_log_file.write(str(total_model_proc_time_L1_C3/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L1_C3 = 0
            total_model_proc_time_L1_C3 = 0
        #else:
        total_model_proc_time_L1_C3 = total_model_proc_time_L1_C3 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L1_C3 = _mpacket_counter_L1_C3 + 1
    elif "L2-C1" in packet_header:
        if (_mpacket_counter_L2_C1 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L2C1.txt", "a")
            model_log_file.write(str(total_model_proc_time_L2_C1/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L2_C1 = 0
            total_model_proc_time_L2_C1 = 0
        #else:
        total_model_proc_time_L2_C1 = total_model_proc_time_L2_C1 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L2_C1 = _mpacket_counter_L2_C1 + 1
    elif "L2-C2" in packet_header:
        if (_mpacket_counter_L2_C2 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L2C2.txt", "a")
            model_log_file.write(str(total_model_proc_time_L2_C2/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L2_C2 = 0
            total_model_proc_time_L2_C2 = 0
        #else:
        total_model_proc_time_L2_C2 = total_model_proc_time_L2_C2 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L2_C2 = _mpacket_counter_L2_C2 + 1
    elif "L2-C3" in packet_header:
        if (_mpacket_counter_L2_C3 == test_packet_length):
            model_log_file = open(log_dir + "data_log_model_time-L2C3.txt", "a")
            model_log_file.write(str(total_model_proc_time_L2_C3/test_packet_length) + "\n")
            model_log_file.close()
            _mpacket_counter_L2_C3 = 0
            total_model_proc_time_L2_C3 = 0
        #else:
        total_model_proc_time_L2_C3 = total_model_proc_time_L2_C3 + (long(time.time() * 1000) - long(end_time))
        _mpacket_counter_L2_C3 = _mpacket_counter_L2_C3 + 1
    else:
        print("Problem in data_log_model_time")
        
        
def publish_message_log_time(packet_header, end_time,packet_size):
    global publog_mpacket_counter_L1_C1
    global publog_mpacket_counter_L1_C2
    global publog_mpacket_counter_L1_C3
    global publog_mpacket_counter_L2_C1
    global publog_mpacket_counter_L2_C2
    global publog_mpacket_counter_L2_C3

    global total_message_proc_time_L1_C1
    global total_message_proc_time_L1_C2
    global total_message_proc_time_L1_C3
    global total_message_proc_time_L2_C1
    global total_message_proc_time_L2_C2
    global total_message_proc_time_L2_C3

    global _outgoing_total_packet_size_L1_C1
    global _outgoing_total_packet_size_L1_C2
    global _outgoing_total_packet_size_L1_C3
    global _outgoing_total_packet_size_L2_C1
    global _outgoing_total_packet_size_L2_C2
    global _outgoing_total_packet_size_L2_C3

    print(packet_header)

    if "L1-C1" in packet_header:
        if (publog_mpacket_counter_L1_C1 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L1C1.txt", "a")
            model_log_file.write(str(total_message_proc_time_L1_C1/test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L1C1.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L1_C1 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L1_C1 = 0
            total_message_proc_time_L1_C1 = 0
            _outgoing_total_packet_size_L1_C1 = 0
        total_message_proc_time_L1_C1 = total_message_proc_time_L1_C1 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L1_C1 = publog_mpacket_counter_L1_C1 + 1
        _outgoing_total_packet_size_L1_C1 = _outgoing_total_packet_size_L1_C1 + packet_size


    elif "L1-C2" in packet_header:
        if (publog_mpacket_counter_L1_C2 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L1C2.txt", "a")
            model_log_file.write(str(total_message_proc_time_L1_C2 / test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L1C2.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L1_C2 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L1_C2 = 0
            total_message_proc_time_L1_C2 = 0
            _outgoing_total_packet_size_L1_C2 = 0
        total_message_proc_time_L1_C2 = total_message_proc_time_L1_C2 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L1_C2 = publog_mpacket_counter_L1_C2 + 1
        _outgoing_total_packet_size_L1_C2 = _outgoing_total_packet_size_L1_C2 + packet_size


    elif "L1-C3" in packet_header:
        if (publog_mpacket_counter_L1_C3 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L1C3.txt", "a")
            model_log_file.write(str(total_message_proc_time_L1_C3 / test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L1C3.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L1_C3 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L1_C3 = 0
            total_message_proc_time_L1_C3 = 0
            _outgoing_total_packet_size_L1_C3 = 0
        total_message_proc_time_L1_C3 = total_message_proc_time_L1_C3 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L1_C3 = publog_mpacket_counter_L1_C3 + 1
        _outgoing_total_packet_size_L1_C3 = _outgoing_total_packet_size_L1_C3 + packet_size
    elif "L2-C1" in packet_header:
        if (publog_mpacket_counter_L2_C1 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L2C1.txt", "a")
            model_log_file.write(str(total_message_proc_time_L2_C1 / test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L2C1.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L2_C1 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L2_C1 = 0
            total_message_proc_time_L2_C1 = 0
            _outgoing_total_packet_size_L2_C1 = 0
        total_message_proc_time_L2_C1 = total_message_proc_time_L2_C1 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L2_C1 = publog_mpacket_counter_L2_C1 + 1
        _outgoing_total_packet_size_L2_C1 = _outgoing_total_packet_size_L2_C1 + packet_size
    elif "L2-C2" in packet_header:
        if (publog_mpacket_counter_L2_C2 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L2C2.txt", "a")
            model_log_file.write(str(total_message_proc_time_L2_C2 / test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L2C2.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L2_C2 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L2_C2 = 0
            total_message_proc_time_L2_C2 = 0
            _outgoing_total_packet_size_L2_C2 = 0
        total_message_proc_time_L2_C2 = total_message_proc_time_L2_C2 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L2_C2 = publog_mpacket_counter_L2_C2 + 1
        _outgoing_total_packet_size_L2_C2 = _outgoing_total_packet_size_L2_C2 + packet_size
    elif "L2-C3" in packet_header:
        if (publog_mpacket_counter_L2_C3 == test_packet_length):
            model_log_file = open(log_dir + "publish_message_log_time-L2C3.txt", "a")
            model_log_file.write(str(total_message_proc_time_L2_C3 / test_packet_length) + "\n")
            model_log_file.close()
            model_size_log_file = open(log_dir + "outgoing_packet_size-L2C3.txt", "a")
            model_size_log_file.write(str(_outgoing_total_packet_size_L2_C3 / test_packet_length) + "\n")
            model_size_log_file.close()
            publog_mpacket_counter_L2_C3 = 0
            total_message_proc_time_L2_C3 = 0
            _outgoing_total_packet_size_L2_C3 = 0
        total_message_proc_time_L2_C3 = total_message_proc_time_L2_C3 + (long(time.time() * 1000) - long(end_time))
        publog_mpacket_counter_L2_C3 = publog_mpacket_counter_L2_C3 + 1
        _outgoing_total_packet_size_L2_C3 = _outgoing_total_packet_size_L2_C3 + packet_size
    else:
        print("Problem in publish_message_log_time")


def data_process_to_pub(sub_message):
    print("Subscribe:",sub_message)
    if "nan" in sub_message:
        if (_client_has_model):
            start_time = long(time.time() * 1000)
            start_time_for_message_log = long(time.time() * 1000)
            print("nan value found. Processing AI.")
            raw_data_info, raw_data_sensors = sub_message.split("Data: (")
            before_time, message_time = raw_data_info.split("[")
            message_time, unused = message_time.split("]")
            packet_header = before_time.replace("( ", "").replace(" ", "")
            incoming_data_log_cfg_tx_time(packet_header, message_time, sub_message.__sizeof__())
            light_data, humidity_data, temperature_data = raw_data_sensors.split(",")
            light_data = light_data.replace("Light:", "").replace(" ", "")
            humidity_data = humidity_data.replace("Humidity:", "").replace(" ", "")
            temperature_data = temperature_data.replace("Temperature:", "").replace(" ", "").replace(")))", "")
            # ekleme-ikok
            if (light_data == "nan"):
                print("Processing Light\n")
                Lmodel_in = np.array([[float(temperature_data), float(humidity_data)]])
                # ekleme ikok
                # Burada model işleyecek
                data_message3 = temperature_data
                data_message2 = humidity_data
                L3d = Lmodel_in.reshape((Lmodel_in.shape[0], 1, Lmodel_in.shape[1]))
                with graphL.as_default():
                    preL = Lmodel.predict(L3d, 1)
                data_message1 = preL[0][0]
                #                data_message1 = "11.11"  # Bu mesaj model sonunda elde edilen değerdir
                #                data_message2 = humidity_data  # Bu mesaj model sonunda elde edilen değerdir
                #                data_message3 = temperature_data  # Bu mesaj model sonunda elde edilen değerdir
                data_log_model_time(packet_header, start_time)
            elif (humidity_data == "nan"):
                print("Processing Humidity\n")
                Hmodel_in = np.array([[float(light_data), float(temperature_data)]])
                # Burada model işleyecek
                data_message1 = light_data
                data_message3 = temperature_data
                H3d = Hmodel_in.reshape((Hmodel_in.shape[0], 1, Hmodel_in.shape[1]))
                with graphH.as_default():
                    preH = Hmodel.predict(H3d, 1)
                data_message2 = preH[0][0]
                #                data_message1 = light_data  # Bu mesaj model sonunda elde edilen değerdir
                #                data_message2 = "22.22"  # Bu mesaj model sonunda elde edilen değerdir
                #                data_message3 = temperature_data  # Bu mesaj model sonunda elde edilen değerdir
                data_log_model_time(packet_header, start_time)
            elif (temperature_data == "nan"):
                print("Processing Temperature\n")
                Tmodel_in = np.array([[float(humidity_data), float(light_data)]])
                # Burada model işleyecek
                data_message2 = humidity_data
                data_message1 = light_data
                T3d = Tmodel_in.reshape((Tmodel_in.shape[0], 1, Tmodel_in.shape[1]))
                with graphT.as_default():
                    preT = Tmodel.predict(T3d, 1)
                data_message3 = preT[0][0]
                #                data_message1 = light_data  # Bu mesaj model sonunda elde edilen değerdir
                #                data_message2 = humidity_data  # Bu mesaj model sonunda elde edilen değerdir
                #                data_message3 = "33.33"  # Bu mesaj model sonunda elde edilen değerdir
                data_log_model_time(packet_header, start_time)
            else:
                print("Problem occured")

            new_message = packet_header + "[" + str(long(time.time() * 1000)) \
                          + "],(" + str(data_message1) + "," + str(data_message2) + "," + str(data_message3) + ")"
            publish_message_log_time(packet_header, start_time_for_message_log,new_message.__sizeof__())
            publish.single(client_pub_topic, new_message, 1, False, pub_broker_address, pub_broker_port)
            print("Publish:", new_message)
        else:
            # These code snippet provides that it handles time by incoming messages and saves them to file.
            # After this operation, it prepares new message.
            start_time_for_message_log = long(time.time() * 1000)
            print("nan value found but pass that directly publish.")
            time_first, message_time = sub_message.split("[")
            message_time, unused = message_time.split("]")
            unused, time_last = sub_message.split("]")
            incoming_data_log_cfg_tx_time(time_first, message_time, sub_message.__sizeof__())
            new_message = time_first + "[" + str(long(time.time() * 1000)) + "]" + time_last
            publish_message_log_time(time_first, start_time_for_message_log,new_message.__sizeof__())
            publish.single(client_pub_topic, new_message, 1, False, pub_broker_address, pub_broker_port)
            print("Publish:", new_message)
    else:
        # These code snippet provides that it handles time by incoming messages and saves them to file.
        # After this operation, it prepares new message.
        start_time_for_message_log = long(time.time() * 1000)
        print("No nan value, so directly publish.")
        time_first, message_time = sub_message.split("[")
        message_time, unused = message_time.split("]")
        unused, time_last = sub_message.split("]")
        incoming_data_log_cfg_tx_time(time_first, message_time, sub_message.__sizeof__())
        new_message = time_first + "[" + str(long(time.time() * 1000)) + "]" + time_last
        publish_message_log_time(time_first, start_time_for_message_log,new_message.__sizeof__())
        publish.single(client_pub_topic, new_message, 1, False, pub_broker_address, pub_broker_port)
        print("Publish:", new_message)


def callback_on_message(client, userdata, message):
    # print("message received ", str(message.payload.decode("utf-8")))
    sub_message = str(message.payload.decode("utf-8"))
    data_process_to_pub(sub_message)

def client_sub_pub():
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

def client_pub():
    print("This client will be run for only publishing. \n ")
    client = mqtt.Client(client_ID)  # create new instance

    # data load-ikok
    df = pd.read_excel('Scaler.xlsx', sheetname='Scaler')
    df = df.values.astype('float32')
    #    global x_scaler
    #    x_scaler = MinMaxScaler(feature_range=(0, 1))
    if (_client_has_model):

        i = 0
        while (i < publish_size):
            model_start_time = long(time.time() * 1000)
            # BURADA MODEL İŞLETİLECEK VE SONUCU data_message değişkenelerine işlenecek.
            #
            start_time_for_message_log = long(time.time() * 1000)
            Lmodel_in = np.array([[0.0, 0.0]])
            Hmodel_in = np.array([[0.0, 0.0]])
            Tmodel_in = np.array([[0.0, 0.0]])

            nan_col = np.where(np.isnan(df[i]))
            if nan_col[0] == [0]:
                print("run lux model")
                data_message3 = Lmodel_in[0][0] = df[i][1]  # T
                data_message2 = Lmodel_in[0][1] = df[i][2]  # H
                L3d = Lmodel_in.reshape((Lmodel_in.shape[0], 1, Lmodel_in.shape[1]))
                with graphL.as_default():
                    preL = Lmodel.predict(L3d, 1)
                data_message1 = preL[0][0]

            elif nan_col[0] == [1]:
                print("runing Temp model")
                data_message2 = Tmodel_in[0][0] = df[i][2]  # H
                data_message1 = Tmodel_in[0][1] = df[i][0]  # L
                T3d = Tmodel_in.reshape((Tmodel_in.shape[0], 1, Tmodel_in.shape[1]))
                with graphT.as_default():
                    preT = Tmodel.predict(T3d, 1)
                data_message3 = preT[0][0]

            elif nan_col[0] == [2]:
                print("runing humd model")
                data_message1 = Hmodel_in[0][0] = df[i][0]  # L
                data_message3 = Hmodel_in[0][1] = df[i][1]  # T
                H3d = Hmodel_in.reshape((Hmodel_in.shape[0], 1, Hmodel_in.shape[1]))
                with graphH.as_default():
                    preH = Hmodel.predict(H3d, 1)
                data_message2 = preH[0][0]

            else:
                print("there is no nan values")
            #            data_message1 = "37.511"  # L Bu mesaj model sonunda elde edilen değerdir.
            #            data_message2 = "52.87946"  # H Bu mesaj model sonunda elde edilen değerdir
            #            data_message3 = "33333"  # T Bu mesaj model sonunda elde edilen değerdir
            data_log_model_time(location_number + "-" + client_number, model_start_time)
            publish_message = "(" + location_number + "-" + client_number + "-" + str(i) + ".Paket),[" + str(
                long(time.time() * 1000)) + "],(" + str(data_message1) + "," + str(data_message2) + "," + str(
                data_message3) + ")"
            publish_message_log_time(packet_name, start_time_for_message_log,publish_message.__sizeof__())
            publish.single(client_pub_topic, publish_message, 1, False, pub_broker_address, pub_broker_port)
            print(publish_message)
            # Delay time
            time.sleep(publish_delay_time)
            i = i + 1
    else:
        print("Without model message process")
        i = 0
        while (i < publish_size):
            start_time_for_message_log = long(time.time() * 1000)
            data_message1 = df[i][
                0]  # light "37.511"   #Bu mesaj csv dosyasından alınacak yoksa NaN yazılacak IBRAHIM HOCA
            data_message2 = df[i][
                2]  # humd "52.87946" #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA
            data_message3 = df[i][
                1]  # temp "NaN"      #Bu mesaj csv dosyasından alınacak  yoksa NaN yazılacak IBRAHIM HOCA
            publish_message = "( (" + location_number + "-" + client_number + "-" + str(i) + ".Paket), [" + str(long(
                time.time() * 1000)) + "], ( ( Data: (Light: " + str(data_message1) + ", Humidity: " + str(
                data_message2) + ", Temperature:" + str(data_message3) + " ) ) )"
            publish_message_log_time(packet_name, start_time_for_message_log,publish_message.__sizeof__())
            publish.single(client_pub_topic, publish_message, 1, False, pub_broker_address, pub_broker_port)
            print(publish_message)
            time.sleep(publish_delay_time)
            i = i + 1


if (_client_will_sub):
    client_sub_pub()
else:
    client_pub()
