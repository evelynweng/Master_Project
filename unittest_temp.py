import unittest
import numpy as np
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
        # print(get_test.content)
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
        
        with open('example_01.jpg', "rb") as image_file:
            img_str = base64.b64encode(image_file.read())

    
        send_dict = {self.VALIDTAG : 295, self.SERVICETAG:'MASK',self.STOREID:111, self.MASKPIC:img_str}
        
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