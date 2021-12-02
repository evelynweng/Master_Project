
from numpy.lib.function_base import average
from cloudservice.handlerclass.keyvaluefordict import *

import os,subprocess
import random
from datetime import timedelta
import numpy as np
import cv2
import base64, requests, json
from django.http import HttpResponse, HttpResponseNotFound

class awsTesting:
    def __init__(self):
        self.API_LOCATION  = "http://54.177.165.188:8080/cloudservice/"
        self.STOREPHONE = '12345678'
        self.PASSWORD='testpwd'
        self.STORENAME='KFC'
        self.STORECAPACITY = 3
        self.STOREID = 1
    
    def mask_true(self) -> HttpResponse:
        maskdir = "mask_dataset/with_mask"
        maskfile = random.choice(os.listdir(maskdir))
        maskfiledest = maskdir + "/" + maskfile
        with open( maskfiledest, "rb") as image_file:
            img_str = base64.b64encode(image_file.read())
        send_dict = {kVALID : 295, kSERVICE:'MASK',kSTOREID:1, kMASKPIC:img_str,kVACCINATION:False}   
        return self.send_post_request(send_dict)

    def vacc_card(self) -> HttpResponse:
        maskdir = "mask_dataset/without_mask"
        maskfile = random.choice(os.listdir(maskdir))
        maskfiledest = maskdir + "/" + maskfile
        with open( maskfiledest, "rb") as image_file:
            img_str = base64.b64encode(image_file.read())
        send_dict = {kVALID : 295, kSERVICE:'MASK',kSTOREID:1, kMASKPIC:img_str,kVACCINATION:True}   
        return self.send_post_request(send_dict)
    
    def check_in(self):
        send_dict =  {
            kVALID : 295, 
            kSERVICE:vCHECKIN,
            kSTOREID:'1',
            kCUSTOMERID:18,
            }
        return self.send_post_request(send_dict)


    def send_post_request(self,input_dict):
        return requests.post(url = self.API_LOCATION, data = input_dict)



def server_perform(testcount):
    total_elapsed_time = timedelta(0)
    print("------------------------------------------------------------")
    print("start server testing")
    print("random caes pool: check-in, mask detect, vaccination card")
    print("------------------------------------------------------------")
    testing = awsTesting()
    choice_func = [testing.mask_true, testing.check_in, testing.vacc_card]
    for i in range (testcount):
        result = random.choice(choice_func)()
        print("case",i,":", result.elapsed)
        total_elapsed_time =  total_elapsed_time + result.elapsed
    print( "\ntotal test time:",total_elapsed_time.seconds, "s", total_elapsed_time.microseconds/1000, "ms")


if __name__ == '__main__':

    testcount = 100
    server_perform(testcount)





