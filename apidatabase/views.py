from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .doservice import  doService
import json


@csrf_exempt 
# Create your views here.
def index(request):
    
    # Uncomment this line to play with the database API
    # play_with_database()
    
    if request.method == "GET":
        return HttpResponse("this is GET method")
    elif request.method == "POST":
        print('database recv request')

        recv_dict = request.POST.dict()

        SERVICETAG = "SERVICE"
        SERVICE ={
            'LOGIN': doService(recv_dict).do_login,
            'REGISTER':doService(recv_dict).do_reg,
            'STARTDETECT': doService(recv_dict).do_start,
            'ENTRY': doService(recv_dict).do_query_capacity,
        }
        
        if not (SERVICETAG in recv_dict and recv_dict.get(SERVICETAG, None) in SERVICE):
            return HttpResponseNotFound('<h1>illegal request</h1>')
        
        request_service = recv_dict[SERVICETAG] # str: login, register, mask
        print('redirect request to database api')
        response = SERVICE.get(request_service, doService(recv_dict).do_nothing)()  # forward to designate service module, default: donothing
        print("database http respond content:", response.content)
        return response

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

    