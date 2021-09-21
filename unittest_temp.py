import unittest
import numpy as np
import cv2
import base64
import requests
import json
from django.http import HttpResponse, HttpResponseNotFound
from cloudservice.handlerclass.keyvaluefordict import *
from cloudservice.handlerclass.datahandler import dataHandler

# not enough time to learn writing unit test 
# using self test first, switch to unittest later

def get_httpreponse_content(input_dict):
        json_string = json.dumps(input_dict)
        r= HttpResponse(json_string, content_type =  "text/html; charset=utf-8")
        return  r.content


class TestCloudservice(unittest.TestCase):
    '''
    def test_register_true(self):
        input_dict =  {kREPLY:True, kSTOREID: 1}
        expect_result = get_httpreponse_content(input_dict)
        test_result = BuidTestServiceRequest().register_true()
        print("send")
        self.assertEqual(test_result, expect_result)
    
    
    def test_login_true(self):
        input_dict = {kREPLY:True, kSTOREID:1}
        expect_result = get_httpreponse_content(input_dict)
        test_result = BuidTestServiceRequest().login_true()
        self.assertEqual(test_result, expect_result)
    
    def test_login_false(self):
        input_dict = {kREPLY:False}
        expect_result = get_httpreponse_content(input_dict)
        test_result = BuidTestServiceRequest().login_false()
        self.assertEqual(test_result, expect_result)
    '''
    def test_mask_true(self):
        input_dict = {kREPLY:True, kQRCODE:None}
        expect_result = get_httpreponse_content(input_dict)
        test_result = BuidTestServiceRequest().mask_true()

        # print(get_test.content)
        self.assertEqual(test_result, expect_result)
    '''
    #currently will fail because not put in qrcode img
    def test_mask_false(self):
        input_dict = {kREPLY:False, kQRCODE:None}
        expect_result = get_httpreponse_content(input_dict)
        test_result = BuidTestServiceRequest().mask_false()
        #print(get_test.content)
        self.assertEqual(test_result, expect_result)
    
    
    def test_startdetect_true(self):
        input_dict = {kREPLY:True}
        expect_result = get_httpreponse_content(input_dict)
        test_result = BuidTestServiceRequest().startdetect_true()
        #print(get_test.content)
        self.assertEqual(test_result, expect_result)
    
    def test_startdetect_false(self):
        input_dict = {kREPLY:False}
        expect_result = get_httpreponse_content(input_dict)
        test_result = BuidTestServiceRequest().startdetect_false()
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
        self.STOREID = 1
    
    def mask_true(self) -> HttpResponse:
        with open('test.jpg', "rb") as image_file:
            img_str = base64.b64encode(image_file.read())
        send_dict = {kVALID : 295, kSERVICE:'MASK',kSTOREID:1, kMASKPIC:img_str}   
        return self.send_post_request_and_get_response_content(send_dict)
    
    def mask_false(self) -> HttpResponse:
        with open('test02.jpg', "rb") as image_file:
            img_str = base64.b64encode(image_file.read())
        send_dict = {kVALID : 295, kSERVICE:'MASK',kSTOREID:1, kMASKPIC:img_str}
        return self.send_post_request_and_get_response_content(send_dict)

    def register_true(self) ->HttpResponse.content:
        send_dict =  {
            kVALID : 295, 
            kSERVICE: vREGISTER,
            kSTOREPHONE:self.STOREPHONE,
            kPASSWORD: self.PASSWORD, 
            kSTORENAME: self.STORENAME,
            kSTORECAPACITY: self.STORECAPACITY
            }
        return self.send_post_request_and_get_response_content(send_dict)

    def login_true(self):
        send_dict =  {
            kVALID : 295, 
            kSERVICE:vLOGIN,
            kSTOREPHONE:self.STOREPHONE,
            kPASSWORD:self.PASSWORD
            }
        return self.send_post_request_and_get_response_content(send_dict)

    def login_false(self):
        send_dict =  {
            kVALID : 295, 
            kSERVICE:vLOGIN,
            kSTOREPHONE:'87654321',
            kPASSWORD:'fakepwd',
            }
        return self.send_post_request_and_get_response_content(send_dict)

    def startdetect_true(self):
        send_dict =  {
            kVALID : 295, 
            kSERVICE:vSTARTDETECT,
            kSTOREID:self.STOREID
            }
        return self.send_post_request_and_get_response_content(send_dict)

    def startdetect_false(self):
        send_dict =  {
            kVALID : 295, 
            kSERVICE:vSTARTDETECT,
            kSTOREID: 789  #dont exist
            }
        return self.send_post_request_and_get_response_content(send_dict)
    
    # helper
    def send_post_request_and_get_response_content(self,input_dict):
        return requests.post(url = self.API_LOCATION, data = input_dict).content


if __name__ == '__main__':
    unittest.main()
    '''
    test_result = BuidTestServiceRequest().mask_true()
    r_dict = json.loads(test_result)
    print(r_dict)
    img_str = r_dict['QRCODE']
    img = dataHandler().encodeImg_to_img(img_str)
    cv2.imshow("test", img)
    cv2.waitKey(0)
    
    
    with open('example_01.jpg', "rb") as image_file:    
        img_str = base64.b64encode(image_file.read())

    img2 = base64.b64decode(img_str)  
    npimg = np.fromstring(img2, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
    print(type(source))

    cv2.imshow("test", source)
    cv2.waitKey(0)
    '''