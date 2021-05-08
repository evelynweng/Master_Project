from cloudservice.handlerclass.datahandler import dataHandler
from cloudservice.handlerclass.keyvaluefordict import *
from .models import Store, Queue
from django.http import HttpResponse, HttpResponseNotFound

class doService:
    def __init__(self, recv_dict):
        self.input_dict = recv_dict
        self.STOREID = self.get_dic_val(kSTOREID)
        self.STORENAME = self.get_dic_val(kSTORENAME)
        self.STOREPHONE = self.get_dic_val(kSTOREPHONE)
        self.PASSWORD = self.get_dic_val (kPASSWORD)
        self.STORECAPACITY = self.get_dic_val (kSTORECAPACITY)
        self.CUSTOMERS = 1 # currently set to one

    def do_login(self):
        can_login = False # defult to false
        if self.STOREPHONE and self.PASSWORD:
            print(self.STOREPHONE)
            stores = Store.objects.filter(
                store_phone = self.STOREPHONE, 
                password = self.PASSWORD
                )
        
            if stores.exists():
                store = stores.get()
                can_login = True
                store_id = store.store_id
                reply_dict = {kREPLY:can_login, kSTOREID:store_id}
            else:
                reply_dict = {kREPLY:can_login}
        else:
            reply_dict = {kREPLY:can_login}
        return dataHandler().dict_to_HttpResponse(reply_dict)
        
    def do_reg(self) -> HttpResponse:
        print('database do_reg funciton')
        _store, created = Store.objects.get_or_create(
            store_name=self.STORENAME,
            store_phone=self.STOREPHONE,
            defaults={
                kPASSWORD:self.PASSWORD,
                kSTORECAPACITY:self.STORECAPACITY,
                'store_current_count' : 0,
                },
            )
        store_id = _store.store_id 
        reply_dict = {kREPLY:created, kSTOREID:store_id}
        print("database reply dict:",reply_dict)
        return dataHandler().dict_to_HttpResponse(reply_dict)

    def do_start(self):
        success_start = False 
        if self.STOREID:
            stores = Store.objects.filter(store_id = self.STOREID)
            if stores.exists():
                store = stores.get()
                store.store_current_count = 0
                store.save() # reset store_current_count to zero
                success_start = True
        reply_dict = {kREPLY:success_start}
        return dataHandler().dict_to_HttpResponse(reply_dict)
        
    def do_query_capacity(self):
        can_enter = False
        if self.STOREID:
            stores = Store.objects.filter(store_id = self.STOREID)
            if stores.exists():
                store = stores.get() #if queryset not exist but directly get, will raise excpetion
                store_customer_after_enter = self.CUSTOMERS + store.store_current_count
                if  store_customer_after_enter <= store.store_capacity:
                    can_enter = True
                    store.store_current_count = store_customer_after_enter
                    store.save()
        reply_dict = {kREPLY:can_enter}
        return dataHandler().dict_to_HttpResponse(reply_dict)

    def do_nothing(self):
        reply_dict = {keyReply:False}
        return self.dataHandler.dict_to_HttpResponse(reply_dict)

    def get_dic_val(self,dictkey):
        return self.input_dict.get(dictkey,None)
