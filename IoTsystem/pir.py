from gpiozero import MotionSensor
from keyvaluefordict import *
import requests

def pir_in_main():
    PIR_IN = MotionSensor(4) # motion sensor on GPIO 4 for IN
    
    while True:
        PIR_IN.wait_for_motion ()
        PirSend().enter_the_store()
        # send http post request to server to update count

def pir_out_main():
    PIR_OUT = MotionSensor(14) # motion sensor on GPIO 14 for OUT

    while True:
        PIR_OUT.wait_for_motion ()
        PirSend().leave_the_store()

class PirSend():
    def __init__(self):
        self.API_LOCATION  = "http://localhost:8080/cloudservice/"
        self.STOREID = 1

    def enter_the_store(self,):
        send_dict = {
            kVALID: vVALID,
            kSERVICE: vSTOREINOUT,
            kSTOREID: self.STOREID,
            kSTOREINOUT: vSTOREIN
        }
        res = self.send_post_request(send_dict)

    def leave_the_store(self,):
        send_dict = {
            kVALID: vVALID,
            kSERVICE: vSTOREINOUT,
            kSTOREID: self.STOREID,
            kSTOREINOUT:vSTOREOUT
        }
        res = self.send_post_request(send_dict)

    def send_post_request(self, input_dict):
        return requests.post(url = self.API_LOCATION, data = input_dict)



