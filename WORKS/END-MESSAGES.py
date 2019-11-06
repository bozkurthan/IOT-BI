import paho.mqtt.publish as publish

pub_topic = "test-server"
hostname = "192.168.1.33"
port = 1883

publish.single(pub_topic, "SL1-C1-SON", 0, False, hostname, port)

publish.single(pub_topic, "SL1-C2-SON", 0, False, hostname, port)

publish.single(pub_topic, "SL1-C3-SON", 0, False, hostname, port)

publish.single(pub_topic, "SL2-C1-SON", 0, False, hostname, port)

publish.single(pub_topic, "SL2-C2-SON", 0, False, hostname, port)

publish.single(pub_topic, "SL2-C3-SON", 0, False, hostname, port)
