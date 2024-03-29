import paho.mqtt.client as mqtt  # import the client1
import paho.mqtt.publish as publish
import time
from numpy import \
  long

client = mqtt.Client("P1")  # create new instance


# 0 = Unprocessed data
# 1 = Processed data
# 2 = Both data
pub_type = 1
time_of_unproccessed = 0.2
time_of_proccessed = 0.2
time_both_data = 1
pub_topic = "test"
host = "192.168.1.104"
qos_type = 1

total_packet_unproc = 100
total_packet_proc = 100

L1_C1_Packet_Send = True
L1_C2_Packet_Send = True
L1_C3_Packet_Send = True
L2_C1_Packet_Send = True
L2_C2_Packet_Send = True
L2_C3_Packet_Send = True

if (pub_type == 0):
  i = 0
  while i < total_packet_unproc:
    if (L1_C1_Packet_Send):
      publish_message = "( (L1-C1-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:33.141613,  Humidty:52.87946, Temperature:NaN ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L1_C2_Packet_Send):
      publish_message = "( (L1-C2-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:33.141613,  Humidty:NaN, Temperature:36.59778 ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L1_C3_Packet_Send):
      publish_message = "( (L1-C3-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:NaN,  Humidty:52.87946, Temperature:36.59778 ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C1_Packet_Send):
      publish_message = "( (L2-C1-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:33.141613,  Humidty:52.87946, Temperature:NaN ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C2_Packet_Send):
      publish_message = "( (L2-C2-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:33.141613,  Humidty:NaN, Temperature:36.59778 ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C3_Packet_Send):
      publish_message = "( (L2-C3-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:NaN,  Humidty:52.87946, Temperature:36.59778 ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    i += 1
    time.sleep(time_of_unproccessed)
elif (pub_type == 1):
  i = 0
  while i < total_packet_proc:
    if (L1_C1_Packet_Send):
      publish_message = "(L1-C1-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L1_C2_Packet_Send):
      publish_message = "(L1-C2-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L1_C3_Packet_Send):
      publish_message = "(L1-C3-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C1_Packet_Send):
      publish_message = "(L2-C1-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C2_Packet_Send):
      publish_message = "(L2-C2-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C3_Packet_Send):
      publish_message = "(L2-C3-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    i += 1
    time.sleep(time_of_proccessed)
elif (pub_type == 2):
  i = 0
  while i < total_packet_unproc:
    if (L1_C1_Packet_Send):
      publish_message = "( (L1-C1-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:33.141613,  Humidty:52.87946, Temperature:NaN ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L1_C2_Packet_Send):
      publish_message = "( (L1-C2-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:33.141613,  Humidty:NaN, Temperature:36.59778 ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L1_C3_Packet_Send):
      publish_message = "( (L1-C3-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:NaN,  Humidty:52.87946, Temperature:36.59778 ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C1_Packet_Send):
      publish_message = "( (L2-C1-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:33.141613,  Humidty:52.87946, Temperature:NaN ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C2_Packet_Send):
      publish_message = "( (L2-C2-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:33.141613,  Humidty:NaN, Temperature:36.59778 ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C3_Packet_Send):
      publish_message = "( (L2-C3-" + str(i) + ".paket), [" + str(
      long(time.time() * 1000)) + "], ( ( Data: (Light:NaN,  Humidty:52.87946, Temperature:36.59778 ) ) )"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    i += 1
    time.sleep(time_of_unproccessed)
  time.sleep(time_both_data)
  i = 0
  while i < total_packet_proc:
    if (L1_C1_Packet_Send):
      publish_message = "(L1-C1-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L1_C2_Packet_Send):
      publish_message = "(L1-C2-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L1_C3_Packet_Send):
      publish_message = "(L1-C3-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C1_Packet_Send):
      publish_message = "(L2-C1-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C2_Packet_Send):
      publish_message = "(L2-C2-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    if (L2_C3_Packet_Send):
      publish_message = "(L2-C3-" + str(i) + ".paket),[" + str(
      long(time.time() * 1000)) + "],(33.141613,52.87946,36.59778)"
      publish.single(pub_topic, publish_message, qos_type, False, host, 1883)
    i += 1
    time.sleep(time_of_proccessed)