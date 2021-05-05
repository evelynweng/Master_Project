
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
        return self.dataHandler.get_database_httpresponse(input_dict)
        
    def do_detect(self,input_dict) -> HttpResponse:
        store_id = self.datahandler.get_store_id(input_dict)
        mask_image = self.datahandler.get_mask_img(input_dict)

        if mask_image.any():        
            pass_mask = detect_mask(mask_image)
        else: 
            return self.datahandler.reply_invalid_data()


        # get bool by : temperature
            # currently passing
        pass_temp = True
        
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
        
        return self.datahandler.dict_to_HttpResponse(reply_dict)

    def do_checkin(self,input_dict) -> HttpResponse:
        return HttpResponse("not use")

    def do_nothing(self, input_dict) -> HttpResponse :
        reply_dict = {keyReply:False}
        return self.dataHandler.dict_to_HttpResponse(reply_dict)
