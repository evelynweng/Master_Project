from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt



# modified by xm
from apidatabase.models import Store, Queue, Customer
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

@csrf_exempt 
# Create your views here.
# def index(request):
    # """Engress point of the cloudservice application
    # Args:
    #     request (WSGIRequest): https://github.com/django/django/blob/main/django/core/handlers/wsgi.py#L64

    # Returns:
    #     HTTPResponse:
    # """
    # Uncomment this line to play with the database API
    # play_with_database()
    # print(request, type(request))


    # if request.method == "GET":
    #     return HttpResponse("this is GET method")
    # elif request.method == "POST":
    #     q = request.POST
    #     l = list(q.values())
    #     return HttpResponse(l[0])

def index(request):
    store_list = Store.objects.order_by('store_name')
    queue_list = Queue.objects.order_by('queuedate')
    context_dict = {}
    context_dict['stores'] = store_list
    context_dict['queues'] = queue_list
   
    return render(request,'queueweb/index.html',context=context_dict)

def queue_status(request, store_name_slug):
    # Create a context dictionary which wer can pass to 
    # the template rendering engine
    context_dict = {}
    try:
        # Can we find a store name slug with the given name?
        # If we can't, the get() method raises a DoesNotExist exception.
        # Of the .get() method returns one model instance or raises an exception.
        store_tmp = Store.objects.get(slug=store_name_slug)

        # Retrieve all of the associated queues
        # The filter() will return a list of queues or an empty list
        queue = Queue.objects.get_or_create(store = store_tmp, queuedate = datetime.date.today())[0]
        # Add results list to the template context under name queues.
        context_dict['queue'] = queue

        # Add the store object from db to the context dictionary
        context_dict['store'] = store_tmp
    
    except store_tmp.DoesNotExist:
        context_dict['store'] = None
        context_dict['queue'] = None

    return render(request,'queueweb/queue_status.html',context=context_dict)

def customer_register(request,store_name_slug):
    store_tmp = Store.objects.get(slug=store_name_slug)
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            if store_tmp:
                customer = form.save(commit=False)
                customer.store = store_tmp
                q = Queue.objects.get_or_create(store = store_tmp,queuedate=datetime.date.today())[0]
                customer.queue = q
                customer.Customerueue_id = q.last_Customerueue_id + 1
                if q.last_Customerueue_id > 0:
                    former_customer = Customer.objects.get(queue = q, Customerueue_id = q.last_Customerueue_id)
                    customer.potential_wait_time = former_customer.potential_wait_time + former_customer.number_of_people * store_tmp.store_average_waiting_time_for_person
                
                q.last_Customerueue_id = customer.Customerueue_id
                q.current_waiting_time = customer.potential_wait_time
                q.number_people_waiting = q.number_people_waiting + customer.number_of_people
                q.save()
                 # save the new customer to the db
                customer.save()
                
                customer_id = customer.id
                # direct the user to customer_status webpage
                return redirect(reverse('customer_status',
                                       kwargs={'store_name_slug':store_name_slug, 'customer_id':customer_id}))
        else:
        # The supplied form contained errors
            print(form.errors)
    context_dict={'form':form, 'store':store_tmp }
    return render(request, 'queueweb/customer_register.html', context=context_dict)

def customer_status(request, store_name_slug, customer_id):
    store_tmp = Store.objects.get(slug=store_name_slug)
    customer = Customer.objects.get(id = customer_id)
    queue = customer.queue
    number_in_line = queue.number_people_waiting - customer.number_of_people
    context_dict = {}
    context_dict = {'store':store_tmp, 'queue':queue,'customer':customer, 'number_in_line':number_in_line}
    if customer.Customerueue_id == -2:
        return render(request,'queueweb/customer_ticket.html',context=context_dict)
    

    return render(request,'queueweb/customer_status.html',context=context_dict) 

def customer_ticket(request,store_name_slug, customer_id):
    # my_dict = {'insert':"You're in the line!"}
    store_tmp = Store.objects.get(slug=store_name_slug)
    customer = Customer.objects.get(id = customer_id)
    
    
    return render(request,'queueweb/customer_ticket.html') 

def customer_leave(request, store_name_slug, customer_id):

    if request.method == 'POST':
        store_tmp = Store.objects.get(slug=store_name_slug)
        customer = Customer.objects.get(id = customer_id)
        queue = customer.queue
        cus_q_id_tmp = customer.Customerueue_id
        if cus_q_id_tmp < 0:
            context_dict = {'store':store_tmp, 'customer':customer }
            return render(request,'queueweb/customer_leave.html',context=context_dict)

        else:
            customer.Customerueue_id = -1
            customer.save()
            while (cus_q_id_tmp < queue.last_Customerueue_id):
                cus_next = Customer.objects.get(queue = queue, Customerueue_id = cus_q_id_tmp + 1)
                cus_next.Customerueue_id = cus_q_id_tmp
                cus_next.potential_wait_time = cus_next.potential_wait_time - customer.number_of_people * store_tmp.store_average_waiting_time_for_person
                cus_q_id_tmp += 1
                cus_next.save()

            if cus_q_id_tmp == queue.last_Customerueue_id:
        
                queue.last_Customerueue_id = queue.last_Customerueue_id - 1
                queue.current_waiting_time = queue.current_waiting_time - customer.number_of_people * store_tmp.store_average_waiting_time_for_person
                queue.number_people_waiting = queue.number_people_waiting - customer.number_of_people
        
                queue.save()
    
            context_dict = {}
            context_dict = {'store':store_tmp, 'customer':customer }

            return render(request,'queueweb/customer_leave.html',context=context_dict)

    store_tmp = Store.objects.get(slug=store_name_slug)
    customer = Customer.objects.get(id = customer_id)
    context_dict = {'store':store_tmp, 'customer':customer }

    return render(request,'queueweb/customer_leave.html',context=context_dict)


def customer_left_store_test(request, store_name_slug):
    store_tmp = Store.objects.get(slug=store_name_slug)
    queue = Queue.objects.get(store = store_tmp,queuedate=datetime.date.today())

    if request.method == 'POST':
        # calculate how many persons could enter the store
        diff = store_tmp.store_capacity - store_tmp.store_current_count
        # find the customer who is the first in queue
        customer_enter = Customer.objects.get(queue = queue, Customerueue_id = queue.first_Customerueue_id + 1)
        if diff < customer_enter.number_of_people:
            return render(request,'queueweb/customer_left_store_test.html')
        else:
            cus_q_id_tmp = customer_enter.Customerueue_id
            customer_enter.Customerueue_id = -2
            # customer_enter.send_ticket() - haven't add this function
            customer_enter.save()
            queue.first_Customerueue_id += 1
            decreased_time = customer_enter.number_of_people * store_tmp.store_average_waiting_time_for_person

            #queue.current_customer_in_store += customer_enter.number_of_people
            queue.current_waiting_time = queue.current_waiting_time - decreased_time
            queue.number_people_waiting = queue.number_people_waiting - customer_enter.number_of_people
            queue.save()
            while cus_q_id_tmp < queue.last_Customerueue_id:
                cus_next = Customer.objects.get(queue = queue, Customerueue_id = cus_q_id_tmp + 1)
                cus_next.potential_wait_time = cus_next.potential_wait_time - decreased_time
                cus_next.save()
                cus_q_id_tmp += 1

    return render(request,'queueweb/customer_left_store_test.html')

@csrf_exempt
def Customeruery(request):

    if request.method == "GET":
        return HttpResponse("this is GET method")
    elif request.method == "POST":

        req_dict = request.POST.dict()
        print(req_dict)
        service = req_dict.get('SERVICE')
        if service == 'ENTRY':
            store_id = req_dict.get('store_id')
            customer_number = int(req_dict.get('customer_numbers'))
            store_interested = Store.objects.get(store_id = store_id)
            queue_current = Queue.objects.get_or_create(store = store_interested,queuedate=datetime.date.today())[0]
            
            customer_total = store_interested.store_current_count + customer_number
            # qrcodeA = A + B # B is related to store.slug
            # imgcode = datahandler.ima_to_encode(qrcodeA)
            if  queue_current.number_people_waiting > 0:
                entry_or_not = False
                store_interested_qrcode = generate_qrcode(store_id)
            elif queue_current.number_people_waiting == 0 and customer_total > store_interested.store_capacity:
                entry_or_not = False
                store_interested_qrcode = generate_qrcode(store_id)
            else:
                #store_interested.current_customer_total += custoer_number
                #store_interested.save()
                entry_or_not = True
                store_interested_qrcode = None
            
            overall_return_dict = {"REPLY":entry_or_not, 'kQRCODE' :store_interested_qrcode}
            #print(store_interested_qrcode)
            #overall_return_dict = {"REPLY":entry_or_not, "QRCODE":12345}
            json_string = json.dumps(overall_return_dict)
            return HttpResponse(json_string, content_type =  "text/html; charset=utf-8")
        else:
            return HttpResponseNotFound('<h1>illegal request</h1>')


# function for generate store qrcode
def generate_qrcode(store_id):
    store_tmp = Store.objects.get(store_id=store_id)
        # currently firstpart is xm's ipaddress + app name
    firstpart = 'http://localhost:8000/queueweb/store/'
    secondpart = store_tmp.slug
    qrcode_url = firstpart + secondpart
    img = qrcode.make(qrcode_url)
        #save_path = 'queueweb/static/'
    
    buffered= BytesIO()
    img.save(buffered,format = "png")
    img_str = base64.b64encode(buffered.getvalue())
    Storercode = base64.b64encode(img_str)
    return str(Storercode)
        # completeName = os.path.join(save_path, file_name)
        # img.save(completeName) 
    
@csrf_exempt
def test_case(request):
    input_dict = {"SERVICE":"ENTRY", "store_id":1, "customer_numbers":5}
    json_string = json.dumps(input_dict)
    #return  requests.get(url = "http://localhost:8000/queueweb/")
    A = requests.post(url = "http://localhost:8000/queueweb/",data = input_dict ).content
    #print(type(A))
    return HttpResponse(A)
    #return HttpResponseNotFound('<h1>illegal request</h1>')