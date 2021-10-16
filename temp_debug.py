import requests
import time
import json
from django.http import HttpResponse, HttpResponseNotFound
from cloudservice.handlerclass.keyvaluefordict import *
from cloudservice.handlerclass.datahandler import dataHandler


def thermal_cam_main():
    print("start thermal_cam")
    t_cam =  thermalcamSend()
    thermalstr = ""
    
    while True:
        gettask =  t_cam.get_task_from_cloud()        
        if gettask : 
            print("got task from server")
            thermalstr = save_temps()
            t_cam.send_temperature_to_cloud(thermalstr)
        else:
            print("time.sleep")
            time.sleep(0.1)

def save_temps():
    print(" camera getting body temp")
    return "36,30,28,37"


class thermalcamSend():
    def __init__(self):
        self.API_LOCATION  = sys_API_LOCATION
        self.STOREID = 1

    def get_task_from_cloud(self) -> bool :
        send_dict = {
            kVALID: vVALID,
            kSERVICE: vGET_TEMP_REQ,
            kSTOREID: self.STOREID,
        }
        res = self.send_post_request(send_dict)
        dicret = self.httpresponse_to_Dict(res)
        print("reply from server:", dicret.get(keyReply,False)
        )
        # print("got task: ", dicret.get(keyReply))
        return dicret.get(keyReply,False)

    def send_temperature_to_cloud (self, thermalstr):
        print("send thermal data to cloud")
        send_dict = {
            kVALID: vVALID,
            kSTOREID: self.STOREID,
            kSERVICE: vTEMP_DATA,
            kTEMP_DATA:thermalstr
        }
        self.send_post_request(send_dict)
        return

    def send_post_request(self, input_dict):
        return requests.post(url = self.API_LOCATION, data = input_dict)
    
    def httpresponse_to_Dict(self, httpresponse):
        return json.loads(httpresponse.content)

if __name__ == '__main__':
    thermal_cam_main()
    