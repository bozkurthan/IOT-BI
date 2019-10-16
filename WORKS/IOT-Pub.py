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
while i < 1000:
  publish_message="(L1-C1-"+ str(i) + ".paket),["+ str(long(time.time() * 1000))+"],(33.141613,52.87946,36.59778)"
  publish.single("test4646",publish_message,1,False,"localhost",1883)
  publish_message="(L1-C2-"+ str(i) + ".paket),["+ str(long(time.time() * 1000))+"],(33.141613,52.87946,36.59778)"
  publish.single("test4646",publish_message,1,False,"localhost",1883)
  publish_message="(L1-C3-"+ str(i) + ".paket),["+ str(long(time.time() * 1000))+"],(33.141613,52.87946,36.59778)"
  publish.single("test4646",publish_message,1,False,"localhost",1883)
  publish_message="(L2-C1-"+ str(i) + ".paket),["+ str(long(time.time() * 1000))+"],(33.141613,52.87946,36.59778)"
  publish.single("test4646",publish_message,1,False,"localhost",1883)
  publish_message="(L2-C2-"+ str(i) + ".paket),["+ str(long(time.time() * 1000))+"],(33.141613,52.87946,36.59778)"
  publish.single("test4646",publish_message,1,False,"localhost",1883)
  publish_message="(L2-C3-"+ str(i) + ".paket),["+ str(long(time.time() * 1000))+"],(33.141613,52.87946,36.59778)"
  publish.single("test4646",publish_message,1,False,"localhost",1883)
  i += 1
  time.sleep(0.2)

#i = 0
#while i < 10:
#  publish_message = "( (L1-C1-0.Paket), (2019-01-20 16:56:58.792566), ( ( Data: (Light:33.141613,  Humidty:52.87946, Temperature:NaN ) ) )"
#  publish.single("test", publish_message, 1, False, "localhost", 1883)
#  i += 1
#  time.sleep(1)
