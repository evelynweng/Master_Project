import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud295.settings')

import django
django.setup()
from apidatabase.models import Store_q, Queue_q, Customer_q
import datetime

def populate():
    create_time = datetime.date.today() 
    
    AF_customers = [
        {'name':'AF','queuedate':create_time,'first_name':'Jose', 'last_name':'Zhen', 'phone':'8478011234',
        'number_of_people':1, 'current_waiting_time_individual':3,
        'potential_wait_time':8,'real_wait_time':5},
        {'name':'AF','queuedate':create_time,'first_name':'Anne', 'last_name':'B', 'phone':'8478011111',
        'number_of_people':1, 'current_waiting_time_individual':3,
        'potential_wait_time':8,'real_wait_time':5}
    ]

    AF_queues = [
    {'queuedate':create_time,
    'current_waiting_time':20,
    'number_people_waiting':3},
    {'queuedate':'2021-04-02',
    'current_waiting_time':10,
    'number_people_waiting':2}
    ]
    
    stores = {'AF':{'queues':AF_queues}}  

    for store, store_data in stores.items():
        s = add_store(store)
        for q in store_data['queues']:
            add_queue(s, q['queuedate'],q['current_waiting_time'],q['number_people_waiting']) 

    for cus in AF_customers:
        add_customer(cus['name'],cus['queuedate'],cus['first_name'],cus['last_name'],cus['phone'],
                cus['number_of_people'],cus['current_waiting_time_individual'],
                cus['potential_wait_time'],cus['real_wait_time']) 

def add_customer(name, queuedate, first_name, last_name, phone, number_of_people, 
    current_waiting_time_individual, potential_wait_time, real_wait_time):
    s = Store_q.objects.get_or_create(name = name)[0]
    q = Queue_q.objects.get_or_create(queuedate=queuedate)[0]
    cus = Customer_q.objects.get_or_create(store = s, queue=q, phone=phone)[0]
    cus.first_name = first_name
    cus.last_name = last_name
    cus.number_of_people = number_of_people
    
    cus.current_waiting_time_individual = current_waiting_time_individual
    cus.potential_wait_time = potential_wait_time
    cus.real_wait_time = real_wait_time
    cus.save()

def add_queue(store, queuedate, current_waiting_time, number_people_waiting,views = 0):
    temp_q = Queue_q.objects.get_or_create(store=store, queuedate=queuedate)[0]
    temp_q.current_waiting_time = current_waiting_time
    temp_q.number_people_waiting = number_people_waiting
    temp_q.views = views
    temp_q.save()
    return temp_q

def add_store(name):
    s=Store_q.objects.get_or_create(name=name, capacity=36, url= 'http://nothinghere.com')[0]
    s.save()
    return s

if __name__=='__main__':
    print('Starting population script')
    populate()