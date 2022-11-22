from dataclasses import dataclass
from distutils.log import info
from paho.mqtt import client as mqttclient
import subprocess, signal

class MQTTclient:
    def __init__(self, broker, port, client_id):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.pid_to_perform_on = 0
        self.kill_service = False
        self.pause_service = False
        self.resume_service = False

    def connect(self):
        self.client = mqttclient.Client(self.client_id)
        self.client.connect(self.broker, self.port)

    def publish(self, message, topic):
        self.client.publish(topic, message)

    def subscribe(self, topic):
        self.client.subscribe(topic, 1)

    def onMessage(self, client, userdata, message):
        global info
        info = str(message.payload.decode("utf-8"))
        p = subprocess.Popen(['ps', '-To', 'pid:1,cmd:1'], stdout=subprocess.PIPE)

        # Getting PID
        out, err = p.communicate()
        for line in out.splitlines():
            if b'MotionPlanning.py' in line:
                #print("Found service")
                line = line.decode("utf-8")
                print(line)
                #print(line.split(None, 1)[0])
                print(len(line.split(None, 1)[1]))
                if(len(line.split(None, 1)[1]) > 60):
                    pid = int(line.split(None, 1)[0])
                    self.pid_to_perform_on = pid

        # Process message
        if (message.topic == "control/service"):
            if(info == "k-service"):
                print("Got the message to kill service")
                self.kill_service = True
            
            elif(info == "p-service"):
                print("Got the message to pause the service")
                self.pause_service = True

            elif(info == "r-service"):
                print("Got the message to resume the service")
                self.resume_service = True
                

    def loop_start(self):
        self.client.loop_start()

    def init(self, subscribeTopic):
        self.connect()
        self.subscribe(subscribeTopic)
        self.client.on_message = self.onMessage
        self.client.loop_start()

    def writeMessageArray(self):
        print(self.message)