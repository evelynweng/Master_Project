from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_str
from django.utils import timezone

# modified by xm
from apidatabase.models import Store, Queue, Customer, Advertisement, PromoCode
from queueweb.forms import CustomerForm
from django.shortcuts import redirect
from django.urls import reverse
import datetime
import qrcode
import base64
from io import BytesIO
# def detail(request, question_id):
#    return HttpResponse("You're looking at question %s." % question_id)

import requests
import json


class queue_manager:

    def __init__(self):
        self.buffer_message_confirm_time = 10 # unit is min
        self.buffer_checkin_confirm_time = 30 # unit is min

    def update_queue(self, store_id):
        store_tmp = Store.objects.get(store_id = store_id)
        queue, created = Queue.objects.get_or_create(store = store_tmp,queuedate=datetime.date.today())
        if created:
            return False
        else:
            people_in_waiting_queue = self.update_waiting_queue(store_id)
            diff = store_tmp.store_capacity - store_tmp.store_current_count - people_in_waiting_queue
        # if there is no customer in queue
        # if queue.first_Customerueue_id == queue.last_Customerueue_id:
        #    return render(request, 'test.html') 
        # find the customer who is the first in queue
            customer_enter = Customer.objects.get(queue = queue, Customerueue_id = queue.first_Customerueue_id + 1)
            if diff < customer_enter.number_of_people:
                print('not enough room!')
                return False
            else:
                print("i am going to let poeple in")
                cus_q_id_tmp = customer_enter.Customerueue_id
                # get the qualified customer's join time and get access time to calculate the actual waiting time
                customer_enter.time_get_access = timezone.now()
                customer_enter.Customerueue_id = -2
                # customer_enter.send_ticket() - haven't add this function
                customer_enter.save()
                queue.first_Customerueue_id += 1
                decreased_time = customer_enter.number_of_people * store_tmp.store_average_waiting_time_for_person

                #queue.current_customer_in_store += customer_enter.number_of_people
                queue.current_waiting_time = queue.current_waiting_time - decreased_time
                queue.number_people_waiting = queue.number_people_waiting - customer_enter.number_of_people
                queue.save()

                # update all customer in the queue for their potential wait time
                while cus_q_id_tmp < queue.last_Customerueue_id:
                    cus_next = Customer.objects.get(queue = queue, Customerueue_id = cus_q_id_tmp + 1)
                    cus_next.potential_wait_time = cus_next.potential_wait_time - decreased_time
                    cus_next.save()
                    cus_q_id_tmp += 1
                print('finished inform the customer')
            return True

    def update_waiting_queue(self,store_id):
        store_interested = Store.objects.get(store_id = store_id)
        queue_current = Queue.objects.get_or_create(store = store_interested,queuedate=datetime.date.today())[0] ## might need to use time zone instead of today funciton
        
        customer_waiting = 0
        for customer_tmp in Customer.objects.filter(Customerueue_id = -2, store = store_interested, queue = queue_current):
            threshold_time = customer_tmp.time_get_access + datetime.timedelta(minutes = self.buffer_checkin_confirm_time)
            if threshold_time > timezone.now():
                customer_waiting = +customer_tmp.number_of_people 
            else:
                customer_tmp.Customerueue_id = -4
                customer_tmp.save()
        print("this is how many poeple are in the waiting queue: " + str(customer_waiting))
        return customer_waiting

    def check_space(self, store_id, customer_number):
        store_interested = Store.objects.get(store_id = store_id)
        queue_current = Queue.objects.get_or_create(store = store_interested,queuedate=datetime.date.today())[0] ## might need to use time zone instead of today funciton

        customer_total = store_interested.store_current_count + customer_number + self.update_waiting_queue(store_id)
        
        if  queue_current.number_people_waiting > 0:
            entry_or_not = False
            print('We don\'t have space, please try to add in the queue')
        elif customer_number > store_interested.store_capacity:
            entry_or_not = False
            print('We don\'t have enough room to accomdate such a large group people')
        elif queue_current.number_people_waiting == 0 and customer_total > store_interested.store_capacity:
            entry_or_not = False
            print('We don\'t have space, please try to add in the queue')
        else:
            entry_or_not = True
            print('No need for wait, we do have space for you')
            return True

    def validate_checkin(self, store_id, customer_id):
        try:
            store_tmp = Store.objects.get(store_id=store_id)
            customer_tmp = Customer.objects.get(id=customer_id, store=store_tmp)
            number_of_people = customer_tmp.number_of_people
            customer_status = customer_tmp.Customerueue_id
            q_temp = customer_tmp.queue
            if q_temp.queuedate == datetime.date.today():
                
                if customer_status == -2:
                    print('this check in has been validated')
                    threshold_time = customer_tmp.time_get_access + datetime.timedelta(minutes = self.buffer_checkin_confirm_time)
                    if threshold_time > timezone.now():
                        customer_tmp.Customerueue_id = -3
                        customer_tmp.save()
                        return True, number_of_people
                    else:
                        print("but the time limit has been exceeded")
                        customer_tmp.Customerueue_id = -4
                        customer_tmp.save()
                        return False, number_of_people
                else:
                    print('this customer is in queue, but not validate to entry')
                    return False, number_of_people
            else:
                print('this is a not validate user for today\'s queue')
                return False,number_of_people
        except Store.DoesNotExist:
            print('store does not exist!')
            return False, None
        except Customer.DoesNotExist:
            print('customer does not exist for the current store')
            return False, None
            #Do Something

    def print_for_fun(self, store_id):
        store_tmp = Store.objects.get(store_id=store_id)
        name = store_tmp.store_name
        print("This is the store name: " + name)
        return True

    def update_queue_time_uponregister(self, customer):
        store_tmp = customer.store
        q = customer.queue
        customer.potential_wait_time = q.current_waiting_time + customer.number_of_people * store_tmp.store_average_waiting_time_for_person
        q.last_Customerueue_id = customer.Customerueue_id
        q.current_waiting_time = customer.potential_wait_time
        q.number_people_waiting = q.number_people_waiting + customer.number_of_people
        q.save()
        # save the new customer to the db
        customer.save()

    def register_customer(self, store_id, customer_number,phone_number):
        store_tmp = Store.objects.get(store_id=store_id)
        q = Queue.objects.get_or_create(store = store_tmp,queuedate=datetime.date.today())[0]
        customer, created = Customer.objects.get_or_create(store = store_tmp, queue=q, phone=phone_number)
        if created:
            customer.queue = q
            customer.Customerueue_id = q.last_Customerueue_id + 1
            customer.number_of_people = customer_number
            customer.save()

            # this is for testing purpose when detecting special string for phone number
            if phone_number == '#ZXZ107':
                customer.join_time = customer.join_time + datetime.timedelta(minutes = 30)

            # update q time with new added customer
            self.update_queue_time_uponregister(customer)
            
            customer_id = customer.id
            return True, customer_id
        else:
            print("This Customer already exist ")
            customer_id = None
            return False, customer_id
