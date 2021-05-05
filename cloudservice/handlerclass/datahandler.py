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
        return requests.post(url = self.API_LOCATION, data = input_dict)

    def get_database_dictresponse(self, input_dict):
        reply_http = requests.post(url = self.API_LOCATION, data = input_dict)
        reply_dict = json.loads(reply_http.content)
        return reply_dict
    
    # easy get
    def get_store_id (self, input_dict):
        return input_dict.get(keyStoreid)
    
    def get_mask_img (self, input_dict):
        return self.encodeImg_to_img(input_dict.get(keyMaskpic))

    def reply_invalid_data(self):
        return self.dict_to_HttpResponse({keyReply:'invalid image'})