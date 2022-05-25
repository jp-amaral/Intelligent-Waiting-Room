import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("message received ", data)

def on_log(client, userdata, level, buf):
    # print("log: ", str(buf))
    with open("log.txt", "a") as log:
        log.write(str(buf) +"\n")


broker_address = "192.168.160.19"

client = mqtt.Client("ppg-client-sub")
client.on_message = on_message
client.on_log = on_log

client.connect(broker_address, port=1883, keepalive=60)

client.subscribe("ppg/data")


client.loop_forever()

