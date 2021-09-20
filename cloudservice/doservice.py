
#from os import wait
import threading
from django.http import HttpResponse, HttpResponseNotFound
from tensorflow.python.ops.gen_array_ops import empty
from .detect_mask_image import detect_mask
from cloudservice.handlerclass.datahandler import dataHandler
from cloudservice.handlerclass.queuehandler import queueHandler
from cloudservice.handlerclass.keyvaluefordict import *
import base64
import json
import requests
import numpy as np
import cv2
from apidatabase.models import Store, Queue

import threading
import time
from .detect_body_temp import detect_temperature

class doService:
    def __init__(self):
        self.datahandler = dataHandler()
        self.queuehandler = queueHandler()
    
    def do_login(self,input_dict) -> HttpResponse:
        #call log-in api in database 
        
        return self.datahandler.get_database_httpresponse(input_dict)

    def do_reg(self,input_dict) -> HttpResponse:
        # call register api in database
        return self.datahandler.get_database_httpresponse(input_dict)
        
    def do_detect(self,input_dict) -> HttpResponse:
        store_id = self.datahandler.get_store_id(input_dict)
        if not store_id:
            return self.datahandler.reply_invalid_data()
        elif not (Store.objects.filter(store_id = store_id)):
            return self.datahandler.reply_invalid_data()
        
        customer_numbers = 1 #currently set to one.
        thread_list = []
       
        pass_mask = BoolToken() # defulat as False    
        t1 = threading.Thread(target=self.thread_detect_mask_result, args=(input_dict,pass_mask))
        t1.start()
        thread_list.append(t1)

        pass_temp = BoolToken() # default as False
        t2 = threading.Thread(target=self.thread_temperature_detect_result, args=(store_id,pass_temp))
        t2.start()
        thread_list.append(t2)

        for subtask in thread_list:
            subtask.join()

        if pass_mask.bool_val and pass_temp.bool_val : 
            reply_dict = self.queuehandler.query_status_and_get_dict(store_id, customer_numbers)
            print("mask/temp true detection result: ", reply_dict)
        else:
            reply_dict = {keyReply:False, kQRCODE:None}
        
        return self.datahandler.dict_to_HttpResponse(reply_dict)

    def do_checkin(self,input_dict) -> HttpResponse:
        return HttpResponse("not use")
    
    def do_start(self, input_dict) -> HttpResponse:
        return self.datahandler.get_database_httpresponse(input_dict)

    def do_nothing(self, input_dict) -> HttpResponse :
        reply_dict = {keyReply:False}
        return self.datahandler.dict_to_HttpResponse(reply_dict)

    def do_store_in_out(self, input_dict) -> HttpResponse:
        store_id = self.datahandler.get_store_id(input_dict)
        store_in = self.datahandler.get_store_in_out(input_dict)
        current_customers = self.queuehandler.store_in_out(store_id, store_in)
        reply_dict = {'count': current_customers}
        return self.datahandler.dict_to_HttpResponse(reply_dict)
    
    def do_get_temperature_request(self, input_dict) -> HttpResponse:
        store_id = self.datahandler.get_store_id(input_dict)
        task_in_task_queue = self.queuehandler.check_exist_thermal_task (store_id)
        reply_dict = {keyReply: task_in_task_queue}
        return self.datahandler.dict_to_HttpResponse(reply_dict)
    
    def do_temperature_check(self, input_dict) -> HttpResponse:
        print("body_temp_check_entry")
        store_id = self.datahandler.get_store_id(input_dict)
        if not store_id:
            return self.datahandler.reply_invalid_data()
        
        stores = Store.objects.filter(store_id = store_id)
        store = stores.get()
    
        if stores.exists():
            store = stores.get()
        else : 
            return self.datahandler.reply_invalid_data()
        
        thermal_file = self.datahandler.get_thermal_data(input_dict)
        body_temp_pass = detect_temperature (thermal_file)
        print("bodt temp checkpoint2")
        #body_temp_pass = True
        if body_temp_pass :
            store.thermal_state = 1
        else:
            store.thermal_state = -1
        store.save()
        reply_dict = {keyReply: body_temp_pass}

        return self.datahandler.dict_to_HttpResponse(reply_dict)
        

    def put_temperature_request_in_task_queue (self, store_id):
        if store_id:
            stores = Store.objects.filter(store_id = store_id)
            if stores.exists():
                store = stores.get()
                store.thermal_task_queue = 1
                store.save()
                return True
            else :
                return False

    def thread_detect_mask_result(self, input_dict, pass_mask):
        mask_image = self.datahandler.get_mask_img(input_dict)
        if mask_image.any():        
            pass_mask.set_bool_val( detect_mask(mask_image))
        print("get mask_detect result:", pass_mask.bool_val)

    def thread_temperature_detect_result(self, store_id, pass_temp):
        put_task = self.put_temperature_request_in_task_queue(store_id)
        if put_task:
            timeout = time.time() + 3 # 2s
            stores = Store.objects.filter(store_id = store_id)
            store = stores.get()
            while store.thermal_state == 0 :
                if time.time() > timeout :
                    break
            body_temp_state = store.thermal_state
            store.thermal_state = 0
            if body_temp_state == 0 or body_temp_state == 1 :
                pass_temp.set_bool_val (True)
            else :
                pass_temp.set_bool_val (False)
            print("get body_temp result:", pass_temp.bool_val)
        else:
            print("put task fail")

class BoolToken:
    def __init__(self):
        self.bool_val = False

    def bool_pass(self):
        self.bool_val = True
    
    def set_bool_val (self, boolval):
        self.bool_val = boolval

if __name__ == '__main__':
    #Do testing
    pass