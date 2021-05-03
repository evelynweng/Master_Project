
from django.http import HttpResponse, HttpResponseNotFound
from .detect_mask_image import detect_mask

import base64
import json
import requests

# key to database
keyService = 'SERVICE'
serviceEntry = "ENTRY" #SERVICE
keyStoreid = 'store_id'

# key  to mobil app
keyReply = 'REPLY'
keyQrcode = 'QRCODE'
# service type
qrCode = 'QRCODE'

# item in input dic
keyMaskpic = 'mask_pic'


class dataHandler:
    def __init__(self):
        self.API_LOCATION  = "http://localhost:8080/apidatabase/"
    
    def dict_to_HttpResponse(self, input_dict) -> HttpResponse :
        json_string = json.dumps(input_dict)
        return HttpResponse(json_string, content_type =  "text/html; charset=utf-8")
    def httpresponse_to_Dict(self, httpresponse):
        httpresponse.cont
    def encodeImg_to_img(self, img_encode_str):
        return base64.b64decode(img_encode_str+"========") 

    def img_to_encodeImg(self, image):
        return base64.b64encode(image)
    
    def get_database_httpresponse(self, input_dict):
        return requests.post(url = self.API_LOCATION, data = input_dict)

    def get_database_dictresponse(self, input_dict):
        reply_http = requests.post(url = self.API_LOCATION, data = input_dict)
        reply_dict = json.loads(reply_http.content)
        return reply_dict

    '''
    # service item (service : items)
        login:  store_id, username, pwd -> True/False
        mask: store_id, mask_pic -> True/ False + qr_pic
        register: username, pwd -> True + store_id / False
        
    # HttpResponse 
        HttpResponse.content.decode() to get string 
        req = HttpResponse(js, content_type =  "text/html; charset=utf-8")
        json dict type= {'key_string': 'value_string'}
        json_string = json.dumps(Dictionary)
        dict = json.loads(jason_string)
    '''

class queueHandler:
    def queue_status(self, input_dict) -> bool :
        reply_dict = dataHandler().get_database_dictresponse(input_dict)
        can_enter = reply_dict.get(keyReply,False)
        #return can_enter
        return True
    
    def get_qrcode(self, input_dict) -> str:
        encode_qrcode_string = 'need to process'
        return encode_qrcode_string

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
        # get value from input dict, assume no error
        store_id = input_dict.get(keyStoreid)
        mask_image = self.datahandler.encodeImg_to_img(input_dict.get(keyMaskpic))

        # get bool by : forward the picture to detect_mask_imgage.py
        
        if mask_image:        
            pass_mask = detect_mask(mask_image)
            # pass_mask = True
        else: 
            return self.datahandler.dict_to_HttpResponse({keyReply:'invalid image'})


        # get bool by : temperature
            # currently passing
        pass_temp = True
        
        if pass_mask and pass_temp : 
            # both True: check strore capacity
            # call apidatabase.entry_validation
            query_capacity = {keyStoreid:store_id, keyService: serviceEntry}
            can_enter = self.queuehandler.queue_status(query_capacity)
            # True: 
                # accumulate capacity at database api
                # return HttpResponse
            if can_enter :
                reply_dict = {keyReply:can_enter}

                # False:
                    # call queue function get qrcode.img
                    # encode qecode.img 
                    # produce dictionary
                    # retun HttpResponse
            else:
                get_qrcode_dict = {'SERVICE':qrCode, 'store_id': store_id, }
                qrcode_str = self.queuehandler.get_qrcode(get_qrcode_dict)
                reply_dict = {keyReply:can_enter, keyQrcode: qrcode_str}

        # False fail pass mask: return HttpResponse
        else:
            reply_dict = {keyReply:can_enter}
        
        return self.datahandler.dict_to_HttpResponse(reply_dict)

    def do_checkin(self,input_dict) -> HttpResponse:
        return HttpResponse("not use")

    def do_nothing(self, input_dict) -> HttpResponse :
        reply_dict = {keyReply:False}
        return self.dataHandler.dict_to_HttpResponse(reply_dict)