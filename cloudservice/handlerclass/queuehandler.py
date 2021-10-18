
from .datahandler import dataHandler
from .keyvaluefordict import *
from apidatabase.models import Store, Queue


class queueHandler:
    def query_status_and_get_dict(self, store_id, customer_numbers) ->dict:
        query_capacity = {keyStoreid:store_id, keyService: vQUERYCAPACITY, kCUSTOMERNUMBERS:customer_numbers}
        reply_dict = dataHandler().get_queue_dictresponse(query_capacity)
        return reply_dict

    def checkin_with_queue(self, input_dict):
        store_id = dataHandler().get_store_id(input_dict)
        if not store_id:
            return {kREPLY:False, kCUSTOMERNUMBERS:0}
        verify_checkin = input_dict
        reply_dict = dataHandler().get_queue_dictresponse(verify_checkin)
        return reply_dict
    
    '''
    def get_qrcode(self, store_id) -> str:
        get_qrcode_dict = {keyService: qrCode, keyStoreid: store_id, }
        encode_qrcode_string = 'need to process'
        return encode_qrcode_string
    ''' 

    def store_in_out(self, store_id, store_in) -> int :
        if store_id:
            stores = Store.objects.filter(store_id = store_id)
            if stores.exists():
                store = stores.get()
                if store_in == vSTOREIN :                    
                    store.store_current_count += 1
                    store.save()
                else:
                    if(store.store_current_count - 1 < 0):
                        store.store_current_count = 0
                        store.save()
                    else:
                        store.store_current_count -= 1
                        store.save()
                        
                        # send request to queue
                        send_dict = {kSERVICE:vLEAVE, kSTOREID:store_id}
                        q_reply = dataHandler().get_queue_dictresponse(send_dict)
                return store.store_current_count
                
            else:
                return -999
    
    def check_exist_thermal_task (self, store_id) -> bool:
        if store_id:
            stores = Store.objects.filter(store_id = store_id)
            if stores.exists():
                store = stores.get()
                if store.thermal_task_queue != 0 :
                    store.thermal_task_queue = 0 # get the task and set task to zero
                    store.save()
                    return True
                else:
                    return False