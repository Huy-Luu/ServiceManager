from ServiceManager import ServiceManager
from MQTTclient import MQTTclient
import subprocess, signal

client = MQTTclient("broker.hivemq.com", 1883, "ServiceManager")
client.init("control/service")
print("Initialized a client")

service_manager = ServiceManager(client)
while(True):
    service_manager.manage()