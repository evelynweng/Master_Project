
from django.http import HttpResponse, HttpResponseNotFound
from .detect_mask_image import detect_mask
from cloudservice.handlerclass.datahandler import dataHandler
from cloudservice.handlerclass.queuehandler import queueHandler
from cloudservice.handlerclass.keyvaluefordict import *
import base64
import json
import requests
import numpy as np
import cv2

class doService:
    def __init__(self):
        self.datahandler = dataHandler()
        self.queuehandler = queueHandler()
    
    def do_login(self,input_dict) -> HttpResponse:
        #call log-in api in database 
        
        return self.datahandler.get_database_httpresponse(input_dict)

    def do_reg(self,input_dict) -> HttpResponse:
        # call register api in database
        print("enter do_reg sent to datahandler")
        return self.datahandler.get_database_httpresponse(input_dict)
        
    def do_detect(self,input_dict) -> HttpResponse:
        store_id = self.datahandler.get_store_id(input_dict)
        mask_image = self.datahandler.get_mask_img(input_dict)
        customer_numbers = 1 #currently set to one.
        if mask_image.any():        
            pass_mask = detect_mask(mask_image)
        else: 
            return self.datahandler.reply_invalid_data()

        
        # get bool by : temperature
            # currently passing
        pass_temp = True
        if pass_mask and pass_temp : 
            reply_dict = self.queuehandler.query_status_and_get_dict(store_id, customer_numbers)
        else:
            reply_dict = {keyReply:False}
        '''
        can_enter = False # can_enter default to False
        if pass_mask and pass_temp : 
            can_enter = self.queuehandler.queue_status(store_id)

            if can_enter :
                reply_dict = {keyReply:can_enter}
            else:
                qrcode_str = self.queuehandler.get_qrcode(store_id)
                reply_dict = {keyReply:can_enter, keyQrcode: qrcode_str}
        else: 
            reply_dict = {keyReply:False}
        '''
        return self.datahandler.dict_to_HttpResponse(reply_dict)

    def do_checkin(self,input_dict) -> HttpResponse:
        return HttpResponse("not use")
    
    def do_start(self, input_dict) -> HttpResponse:
        print("send request to database")
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

