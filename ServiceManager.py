from MQTTclient import MQTTclient
import os, signal
import time

class ServiceManager():
    def __init__(self, mqttclient):
        self.mqttclient = mqttclient
        self.re_run_cmd = 'python3 ~/MotionPlaninngSimulation/MotionPlanning.py &'

    def manage(self):
        while(True):
            while (self.mqttclient.kill_service == False):
                pass
            pid = self.mqttclient.pid_to_kill
            print("Killing main service")
            os.kill(pid, signal.SIGTERM)
            print("Finish killing main service")
            time.sleep(5)
            print("Re-running main service")
            os.system(self.re_run_cmd)
            print("Ran main service")
            self.mqttclient.kill_service = False