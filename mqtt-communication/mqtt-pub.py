import paho.mqtt.client as mqtt
import time
import random

#function to generate a random number between 60 and 120 with 1 decimal place
def random_number():
    return round(random.uniform(60, 120), 1)

broker_address = "192.168.160.19"
#Client instance
client = mqtt.Client("ppg-client-pub")

client.connect(broker_address, port=1883, keepalive=60)

while(True):
    num = random_number()
    print("Publishing: ", num)
    client.publish("ppg/data", num)
    time.sleep(1)


