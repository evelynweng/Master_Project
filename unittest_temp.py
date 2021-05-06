import unittest
import numpy as np
import cv2
import base64
import requests
import json
from django.http import HttpResponse, HttpResponseNotFound
from cloudservice.handlerclass.keyvaluefordict import *

# not enough time to learn writing unit test 
# using self test first, switch to unittest later

def get_httpreponse_content(input_dict):
        json_string = json.dumps(input_dict)
        r= HttpResponse(json_string, content_type =  "text/html; charset=utf-8")
        return  r.content

class TestCloudservice(unittest.TestCase):

    def test_register_true(self):
        input_dict =  {kREPLY:True, kSTOREID: 1}
        expect_result = get_httpreponse_content(input_dict)
        test_result = BuidTestServiceRequest().register_true().content
        self.assertEqual(test_result, expect_result)
    '''
    def test_login_true(self):
        input_dict = {kREPLY:True, kSTOREID:1}
        expect_result = get_httpreponse_content(input_dict)
        test_result = BuidTestServiceRequest().login_true().content
        self.assertEqual(test_result, expect_result)

    def test_mask_true(self):
        input_dict = {'REPLY':True}
        expect_result = get_httpreponse_content(input_dict)
        test_result = BuidTestServiceRequest().mask_true().content
        # print(get_test.content)
        self.assertEqual(test_result, expect_result)
    
    def test_mask_false(self):
        input_dict = {'REPLY':False}
        expect_result = get_httpreponse_content(input_dict)
        test_result = BuidTestServiceRequest().mask_false().content
        #print(get_test.content)
        self.assertEqual(test_result, expect_result)
    '''

class BuidTestServiceRequest:
    def __init__(self):
        self.API_LOCATION  = "http://localhost:8080/cloudservice/"
        self.STOREPHONE = '12345678'
        self.PASSWORD='testpwd'
        self.STORENAME='KFC'
        self.STORECAPACITY = 3
    
    def mask_true(self) -> HttpResponse:
        
        with open('test.jpg', "rb") as image_file:
            img_str = base64.b64encode(image_file.read())
        send_dict = {kVALID : 295, kSERVICE:'MASK',kSTOREID:1, kMASKPIC:img_str}
        return requests.post(url = self.API_LOCATION, data = send_dict)
    
    def mask_false(self) -> HttpResponse:
        
        with open('test02.jpg', "rb") as image_file:
            img_str = base64.b64encode(image_file.read())
        send_dict = {kVALID : 295, kSERVICE:'MASK',kSTOREID:1, kMASKPIC:img_str}       
        return requests.post(url = self.API_LOCATION, data = send_dict)

    def register_true(self) ->HttpResponse:
        send_dict =  {
            kVALID : 295, 
            kSERVICE: vREGISTER,
            kSTOREPHONE:self.STOREPHONE,
            kPASSWORD: self.PASSWORD, 
            kSTORENAME: self.STOREPHONE,
            kSTORECAPACITY: self.STORECAPACITY
            }
        return requests.post(url = self.API_LOCATION, data = send_dict)

    def login_true(self) ->HttpResponse:
        send_dict =  {
            kVALID : 295, 
            kSERVICE:vLOGIN,
            kSTOREPHONE:self.STOREPHONE,
            kPASSWORD:self.PASSWORD
            }
        return requests.post(url = self.API_LOCATION, data = send_dict)



if __name__ == '__main__':
    unittest.main()
    '''
    with open('example_01.jpg', "rb") as image_file:    
        img_str = base64.b64encode(image_file.read())

    img2 = base64.b64decode(img_str)  
    npimg = np.fromstring(img2, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
    print(type(source))

    cv2.imshow("test", source)
    cv2.waitKey(0)
    '''