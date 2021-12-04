import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
import requests
from keyvaluefordict import *
from numpy import savetxt, loadtxt
import json
import base64

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # start MLX90640
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate
mlx_shape = (24,32)


def thermal_cam_main():
    print("start temperature thread")
    t_cam =  thermalcamSend()
    #thermalstr = "36,36"
    while True:
        gettask =  t_cam.get_task_from_cloud()        
        if gettask : 
            print("got temp task from server")
            thermalstr = save_temps()
            print("send thermalstr:", thermalstr)
            t_cam.send_temperature_to_cloud(thermalstr)
        else:
            time.sleep(0.1)

def save_temps():
    try:
        frame = np.zeros((24*32,)) # setup temperature array
        mlx.getFrame(frame) # read MLX temperatures
        u = np.mean(frame)
        s = np.std(frame)
        median = np.median(frame)
        frame[(u - 3 * s > frame) | (u + 3 * s < frame)] = median
        # data_array = (np.reshape(frame,mlx_shape)) # reshape to 24x32
        return base64.b64encode(frame.tostring())
    except ValueError as err:
        print("get body temp err: ", err)
        raise err 

class thermalcamSend():
    def __init__(self):
        self.API_LOCATION  = IPServer
        self.STOREID = 1

    def get_task_from_cloud(self) -> bool :
        send_dict = {
            kVALID: vVALID,
            kSERVICE: vGET_TEMP_REQ,
            kSTOREID: self.STOREID,
        }
        res = self.send_post_request(send_dict)
        dicret = self.httpresponse_to_Dict(res)
        # print("got task: ", dicret.get(keyReply))
        return dicret.get(keyReply,False)

    def send_temperature_to_cloud (self, thermalstr):
        send_dict = {
            kVALID: vVALID,
            kSERVICE: vTEMP_DATA,
            kSTOREID: self.STOREID,
            kTEMP_DATA:thermalstr
        }
        self.send_post_request(send_dict)
        return

    def send_post_request(self, input_dict):
        return requests.post(url = self.API_LOCATION, data = input_dict)
    
    def httpresponse_to_Dict(self, httpresponse):
        return json.loads(httpresponse.content)
