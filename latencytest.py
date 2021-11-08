
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
        self.API_LOCATION  = sys_API_LOCATION
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
    
    def check_in(self, customer_id):
        send_dict =  {
            kVALID : 295, 
            kSERVICE:vCHECKIN,
            kSTOREID:'1',
            kCUSTOMERID:customer_id,
            }
        return self.send_post_request(send_dict)


    def send_post_request(self,input_dict):
        return requests.post(url = self.API_LOCATION, data = input_dict)


def mask_latency_test(testcount): 
    total_elapsed_time = timedelta(0)
    print("\n------------------------------------")
    print("Mask detection latency test")
    print("Testcount: ", testcount)
    print("------------------------------------")

    for i in range (testcount):
        result = awsTesting().mask_true()
        print("case:",i+1, result.elapsed)
        total_elapsed_time =  total_elapsed_time + result.elapsed
    averagelatency =  total_elapsed_time/testcount
    print( "\naverage mask detection latency:", averagelatency.seconds, "s", averagelatency.microseconds/1000, "ms")

def vaccination_card_test(testcount):
    total_elapsed_time = timedelta(0)
    print("\n------------------------------------")
    print("Vaccination card latency test")
    print("Testcount: ", testcount)
    print("------------------------------------")

    for i in range (testcount):
        result = awsTesting().vacc_card()
        print("case:",i+1, result.elapsed)
        total_elapsed_time =  total_elapsed_time + result.elapsed
    averagelatency =  total_elapsed_time/testcount
    print( "\naverage vaccination card detection latency:", averagelatency.seconds, "s", averagelatency.microseconds/1000, "ms")

def checkin_test(testcount):
    total_elapsed_time = timedelta(0)
    print("\n------------------------------------")
    print("Check-in latency test")
    print("Testcount: ", testcount)
    print("------------------------------------")
    for i in range (testcount):
        result = awsTesting().check_in(i+2)
        print("case:",i+1, result.elapsed)
        total_elapsed_time =  total_elapsed_time + result.elapsed
    averagelatency =  total_elapsed_time/testcount
    print( "\naverage Check-in latency:", averagelatency.seconds, "s", averagelatency.microseconds/1000, "ms")

if __name__ == '__main__':

    testcount = 20
    mask_latency_test(testcount)
    vaccination_card_test(testcount)
    checkin_test(testcount)



