import unittest

import cv2
import base64
import requests
import json
from django.http import HttpResponse, HttpResponseNotFound
# not enough time to learn writing unit test 
# using self test first, switch to unittest later

class TestCloudservice(unittest.TestCase):

    def test_mask(self):
        input_dict = {'REPLY':True}
        json_string = json.dumps(input_dict)
        r= HttpResponse(json_string, content_type =  "text/html; charset=utf-8")
        get_test = BuidTestServiceRequest().mask()

        self.assertEqual(get_test.content, r.content)
       


class BuidTestServiceRequest:
    def __init__(self):
        self.VALIDTAG = 'CMPE295'
        self.SERVICETAG= 'SERVICE'
        self.STOREID = 'store_id'
        self.MASKPIC = 'mask_pic'
        self.REPLYTAG = 'REPLY'
        self.API_LOCATION  = "http://localhost:8080/cloudservice/"
    
    def mask(self) -> HttpResponse:

        img = cv2.imread('example_01.jpg')
        img_str = base64.b64encode(img)
        send_dict = {self.VALIDTAG : 295, self.SERVICETAG:'MASK',self.STOREID:111, self.MASKPIC:img_str}
        return requests.post(url = self.API_LOCATION, data = send_dict)



if __name__ == '__main__':
    unittest.main()