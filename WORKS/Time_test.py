import time
from numpy import long

i = 0
while i < 100:
    publish_message = str(long(time.time() * 1000))
    print(publish_message)
    i += 1
    time.sleep(1.5)
