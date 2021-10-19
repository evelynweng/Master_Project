import requests
import json
from django.http import HttpResponse, HttpResponseNotFound
from cloudservice.handlerclass.keyvaluefordict import *

class QueueValidator:
    def __init__(self, store_id, customers):
        self.store_id = store_id
        self.customers = customers
        self.HOSTADDRESS = "http://localhost:8080"
        self.API_LOCATION  = self.HOSTADDRESS + "/cloudservice/"
        self.QUEUEWEB_LOCATION = self.HOSTADDRESS + "/queueweb/"

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
        self.send_post_request_toqueueweb(self.store_id) # added by XM for illustration purpose
        return self.get_httpreponse_current_customers(res)
    
    def validate_register(self, store_id, custoer_number, phone_number):
        input_dict = {"SERVICE":"REGISTER", "store_id":store_id, "customer_numbers":custoer_number, "phone_number":phone_number}
        return requests.post(url =self.QUEUEWEB_LOCATION, data = input_dict)           
    
    def validate_entry(self, store_id, custoer_number):
        input_dict = {"SERVICE":"ENTRY", "store_id":store_id, "customer_numbers":custoer_number}
        return requests.post(url = self.QUEUEWEB_LOCATION, data = input_dict)    
    
    def send_post_request(self,input_dict):
        return requests.post(url = self.API_LOCATION, data = input_dict)

    def send_post_request_toqueueweb(self,store_id):# added by XM for illustration purpose
        input_dict = {"SERVICE":"LEAVE", "store_id":store_id}
        return requests.post(url = self.QUEUEWEB_LOCATION, data = input_dict)
    
    def get_httpreponse_current_customers(self, httpresponse) -> int:
        recv_dict =   json.loads(httpresponse.content)
        return recv_dict ['count']
    
    def validate_checkin(self, store_id,  customer_id):
        input_dict = {"SERVICE":"CHECKIN", "store_id":store_id, "customer_id": customer_id}
        return requests.post(url = self.QUEUEWEB_LOCATION, data = input_dict)


if __name__ == '__main__':
    store_id = 1
    customers= 1
    ms = QueueValidator(store_id, customers)
    while True:
        action = input("Enter your choice: (1) Enter, (2) Leave, (3) Close MS, (4) request for entry, (5) request for register, (6) request for validate: ")
        if action == '1' :
            current_count = ms.enter_the_store()
            print("store current count:", current_count)
        elif action == '2' :
            current_count = ms.leave_the_store()
            print("store current count:", current_count)
        elif action == '3': 
            print("Close Motion Simulator")
            break
        elif action == '4':
            #ms.validate_entry()
            action_2 = input("Enter your choice of store id: ")
            action_3 = input("Enter your choice of customer number: ")
            store_id = int(action_2)
            customer_number = int(action_3)
            ms.validate_entry(store_id,customer_number)
        elif action == '5':
            action_2 = input("Enter your choice of store id: ")
            action_3 = input("Enter your choice of customer number: ")
            action_4 = input("Enter your choice of phone number: ")
            store_id = int(action_2)
            customer_number = int(action_3)
            ms.validate_register(store_id,customer_number,action_4)
        elif action == '6':
            action_2 = input("Enter your choice of store id: ")
            action_3 = input("Enter your choice of customer id: ")
            store_id = int(action_2)
            customer_id = int(action_3)
            ms.validate_checkin(store_id,customer_id)
        else:
            print ("wrong option!")
        
    

