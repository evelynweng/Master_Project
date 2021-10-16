from django.http import HttpResponse
from .keyvaluefordict import *
import base64
import json
import requests
import numpy as np
import cv2



class dataHandler:
    def __init__(self):
        self.API_LOCATION  = "http://localhost:8080/apidatabase/"
        self.Q_API_LOCATION = "http://localhost:8080/queueweb/"
    
    def dict_to_HttpResponse(self, input_dict) -> HttpResponse :
        json_string = json.dumps(input_dict)
        return HttpResponse(json_string, content_type =  "text/html; charset=utf-8")
    def httpresponse_to_Dict(self, httpresponse):
        return json.loads(httpresponse.content)
        
    def encodeImg_to_img(self, img_encode_str):
        img = base64.b64decode(img_encode_str)  
        npimg = np.fromstring(img, dtype=np.uint8)
        cv2img = cv2.imdecode(npimg, 1)
        return cv2img

    def img_to_encodeImg(self, image):
        return base64.b64encode(image)
    
    def get_database_httpresponse(self, input_dict):
        print("send to database")
        r = requests.post(url = self.API_LOCATION, data = input_dict)
        send_dict = self.httpresponse_to_Dict(r)
        return self.dict_to_HttpResponse(send_dict)

    def get_database_dictresponse(self, input_dict) -> dict:
        reply_http = requests.post(url = self.API_LOCATION, data = input_dict)
        reply_dict = json.loads(reply_http.content)
        print("reply_dict from database:",reply_dict)
        return reply_dict

    def get_queue_dictresponse(self, input_dict) -> dict:
        reply_http = requests.post(url = self.Q_API_LOCATION, data = input_dict)
        reply_dict = json.loads(reply_http.content)
        print("reply_dict from database:",reply_dict)
        return reply_dict
    
    # easy get
    def get_store_id (self, input_dict):
        return input_dict.get(keyStoreid,None)
    
    def get_mask_img (self, input_dict):
        return self.encodeImg_to_img(input_dict.get(keyMaskpic,None))

    def reply_invalid_data(self):
        return self.dict_to_HttpResponse({keyReply:'invalid data'})
    
    def get_store_in_out (self, input_dict):
        return input_dict.get(kSTOREINOUT,False)
        
    def get_temp_request (self, input_dict):
        return input_dict.get(kGET_TEMP_REQ,False)

    def get_thermal_data(self,input_dict):
        # self.encodeImg_to_img(input_dict.get(kTEMP_DATA,None))
        return input_dict.get(kTEMP_DATA,"36,37")    

    def get_vaccination_status(self, input_dict):
        return input_dict.get(kVACCINATION, False)