
from .datahandler import dataHandler
from .keyvaluefordict import *
from apidatabase.models import Store, Queue


class queueHandler:
    def queue_status(self, store_id) -> bool :
        query_capacity = {keyStoreid:store_id, keyService: vQUERYCAPACITY}
        reply_dict = dataHandler().get_database_dictresponse(query_capacity)
        can_enter = reply_dict.get(keyReply,False)
        return can_enter
    
    def get_qrcode(self, store_id) -> str:
        get_qrcode_dict = {keyService: qrCode, keyStoreid: store_id, }
        encode_qrcode_string = 'need to process'
        return encode_qrcode_string
    
    def store_in_out(self, store_id, store_in) -> int :
        print(type(store_in))
        if store_id:
            stores = Store.objects.filter(store_id = store_id)
            if stores.exists():
                store = stores.get()
                if store_in == vSTOREIN :
                    
                    store.store_current_count += 1
                    store.save()
                else:
                    store.store_current_count -= 1
                    store.save()
                return store.store_current_count
            else:
                return -999
