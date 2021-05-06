
from .datahandler import dataHandler
from .keyvaluefordict import *


class queueHandler:
    def queue_status(self, store_id) -> bool :
        query_capacity = {keyStoreid:store_id, keyService: serviceEntry}
        reply_dict = dataHandler().get_database_dictresponse(query_capacity)
        can_enter = reply_dict.get(keyReply,False)
        return can_enter
    
    def get_qrcode(self, store_id) -> str:
        get_qrcode_dict = {keyService: qrCode, keyStoreid: store_id, }
        encode_qrcode_string = 'need to process'
        return encode_qrcode_string