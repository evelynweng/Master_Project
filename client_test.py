import json
from django.http import HttpResponse
input_dict = {"SERVICE":"ENTRY", "store_id":1, "customer_numbers":5}
json_string = json.dumps(input_dict)
print(json_string)
a = HttpResponse(json_string,content_type =  "text/html; charset=utf-8")
print(a)