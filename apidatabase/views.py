from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt 
# Create your views here.
def index(request):
    
    # Uncomment this line to play with the database API
    # play_with_database()
    print(request, type(request))

    if request.method == "GET":
        return HttpResponse("this is GET method")
    elif request.method == "POST":
        '''
        VALIDTAG ="CMPE295"
        SERVICETAG = "SERVICE"
        SERVICE ={
            'LOGIN': classmethod(doService.do_login),
            'REGISTER': classmethod(doService.do_reg),
            'MASK': classmethod(doService.do_detect),
            'CHECKIN': classmethod(doService.do_checkin), 
        }
        '''
        temp_reply = {"REPLY": True}
        json_string = json.dumps(temp_reply)
        return HttpResponse(json_string, content_type =  "text/html; charset=utf-8")

def play_with_database():
    from models import Store, Queue

    print("=========================================")
    print("Show all Stores after creating KFC")
    new_store = Store(store_id=1, store_name="KFC")
    new_store.save()
    print(Store.objects.all())

    print("=========================================")
    print("Show all items after changing KFC to McDonald's")
    new_store.store_name = "McDonald's"
    new_store.save()
    print(Store.objects.all())

    print("=========================================")
    print("Show all items after adding KFC and In-and-Out")
    Store(store_id=2, store_name="KFC").save()
    Store(store_id=3, store_name="In-and-Out").save()
    print(Store.objects.all())

    # Table lookup APIs
    # https://docs.djangoproject.com/en/3.1/topics/db/queries/#field-lookups-intro
    print("=========================================")
    print("SELECT * FROM Store WHERE store_id = 2")
    print(Store.objects.filter(store_id=2))

    print("=========================================")
    print("SELECT * FROM Store WHERE store_id <= 2")
    print(Store.objects.filter(store_id__lte=2))

    print("=========================================")
    print("SELECT * FROM Store WHERE store_name like 'In%'")
    print(Store.objects.filter(store_name__startswith="In"))

    print("=========================================")
    print("Delete all items from Store")
    Store.objects.all().delete()
    print(Store.objects.all())