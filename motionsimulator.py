import requests
import json
from django.http import HttpResponse, HttpResponseNotFound
from cloudservice.handlerclass.keyvaluefordict import *

class MotionSimulator:
    def __init__(self, store_id, customers):
        self.store_id = store_id
        self.customers = customers
        self.API_LOCATION  = sys_API_LOCATION

    def enter_the_store(self):
        send_dict = {
            kVALID: vVALID,
            kSERVICE: vSTOREINOUT,
            kSTOREID:self.store_id,
            kSTOREINOUT:vSTOREIN
        }
        res = self.send_post_request(send_dict)
        return self.get_httpreponse_current_customers(res)

    def leave_the_store(self):
        send_dict = {
            kVALID: vVALID,
            kSERVICE: vSTOREINOUT,
            kSTOREID:self.store_id,
            kSTOREINOUT:vSTOREOUT
        }
        
        res = self.send_post_request(send_dict)
        self.send_post_request_toqueueweb(send_dict) # added by XM for illustration purpose
        return self.get_httpreponse_current_customers(res)
    
    def send_post_request(self,input_dict):
        return requests.post(url = self.API_LOCATION, data = input_dict)

    def send_post_request_toqueueweb(self,input_dict):# added by XM for illustration purpose
        return requests.post(url = "http://localhost:8080/queueweb/leave", data = input_dict)
    
    def get_httpreponse_current_customers(self, httpresponse) -> int:
        recv_dict =   json.loads(httpresponse.content)
        return recv_dict ['count']


if __name__ == '__main__':
    store_id = 1
    customers= 1
    ms = MotionSimulator(store_id, customers)
    while True:
        action = input("Enter your choice: (1) Enter, (2) Leave, (3) Close MS: ")
        if action == '1' :
            current_count = ms.enter_the_store()
            print("store current count:", current_count)
        elif action == '2' :
            current_count = ms.leave_the_store()
            print("store current count:", current_count)
        elif action == '3': 
            print("Close Motion Simulator")
            break
        else:
            print ("wrong option!")
        
    

