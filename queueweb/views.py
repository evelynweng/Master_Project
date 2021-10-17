from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_str
from django.utils import timezone



# modified by xm
from apidatabase.models import PromoCode, Store, Queue, Customer, Advertisement, PromoCode
from queueweb.forms import CustomerForm, CustomerUpdateForm
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
from queueweb.queue_addedfunc import queue_manager



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


def advertiment_list_by_store(store_tmp):
    advertisement_list = Advertisement.objects.filter(store_id = store_tmp, start_date__lte=timezone.now(),end_date__gte=timezone.now() )
    return advertisement_list

def real_waiting_time(customer):
    timediff = (customer.time_get_access - customer.join_time)
    timediff = timediff.seconds//60
    return timediff

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
    print("imgstr type:", type(img_str))
    return force_str(img_str)
    #Storercode = base64.b64encode(img_str)
    # return str(Storercode)
        # completeName = os.path.join(save_path, file_name)
        # img.save(completeName) 


def queue_status(request, store_name_slug):
    # Create a context dictionary which wer can pass to 
    # the template rendering engine
    context_dict = {}
    

    try:
        # Can we find a store name slug with the given name?
        # If we can't, the get() method raises a DoesNotExist exception.
        # Of the .get() method returns one model instance or raises an exception.
        store_tmp = Store.objects.get(slug=store_name_slug)
        store_id = store_tmp.store_id
        #queue_manager().print_for_fun(store_id)


        # Retrieve all of the associated queues
        # The filter() will return a list of queues or an empty list
        queue = Queue.objects.get_or_create(store = store_tmp, queuedate = datetime.date.today())[0]

        
        # Add results list to the template context under name queues.
        context_dict['queue'] = queue

        # Add the store object from db to the context dictionary
        context_dict['store'] = store_tmp

        context_dict['advertisements'] = advertiment_list_by_store(store_tmp)
        

    except store_tmp.DoesNotExist:
        context_dict['store'] = None
        context_dict['queue'] = None

    return render(request,'queueweb/queue_status.html',context=context_dict)

@csrf_exempt
def customer_update(request,store_name_slug, customer_id):
    store_tmp = Store.objects.get(slug=store_name_slug)
    customer = Customer.objects.get(id = customer_id)
    queue = customer.queue
    # number_in_line should be indivitual customer 
    number_in_line = customer.potential_wait_time/store_tmp.store_average_waiting_time_for_person - customer.number_of_people
    #number_in_line = queue.number_people_waiting - customer.number_of_people
    cus_num_before = int(number_in_line)
    context_dict = {}
    context_dict = {'store':store_tmp, 'queue':queue,'customer':customer, 'number_in_line':cus_num_before}
    if customer.Customerueue_id == -2:
        return redirect(reverse('customer_ticket',
                    kwargs={'store_name_slug':store_name_slug, 'customer_id':customer_id}))
    context_dict['advertisements'] = advertiment_list_by_store(store_tmp)
    form = CustomerUpdateForm()
    context_dict['form'] = form
    if request.method == 'POST':
        #print('we know you submitted the form')
        form = CustomerUpdateForm(request.POST)
        if form.is_valid():
            #print('we know this is a validate form')
            if customer:
                #print('we know there is a such customer')
                customer.first_name = form.cleaned_data['first_name']
                customer.last_name = form.cleaned_data['last_name']
                customer.phone = form.cleaned_data['phone']
                poeple_delta = customer.number_of_people - form.cleaned_data['number_of_people']
                time_delta = poeple_delta * store_tmp.store_average_waiting_time_for_person
                customer.number_of_people = form.cleaned_data['number_of_people']
                customer.save()
                cus_q_id_tmp = customer.Customerueue_id

                while (cus_q_id_tmp <= queue.last_Customerueue_id):
                    cus_next = Customer.objects.get(queue = queue, Customerueue_id = cus_q_id_tmp)
                    cus_next.potential_wait_time = cus_next.potential_wait_time - time_delta
                    cus_q_id_tmp += 1
                    cus_next.save()

                #if cus_q_id_tmp == queue.last_Customerueue_id:
            
                queue.current_waiting_time = queue.current_waiting_time - time_delta
                queue.number_people_waiting = queue.number_people_waiting - poeple_delta
            
                queue.save()

                return redirect(reverse('customer_status',
                        kwargs={'store_name_slug':store_name_slug, 'customer_id':customer_id}))


    return render(request,'queueweb/customer_update.html',context=context_dict) 

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
                customer.save() 
                customer_id = customer.id
                # save the customer to the db

                # update the queue time based on customer information and save updated queue and customer
                queue_manager().update_queue_time_uponregister(customer)
         
                # direct the user to customer_status webpage
                return redirect(reverse('customer_status',
                                       kwargs={'store_name_slug':store_name_slug, 'customer_id':customer_id}))
        else:
        # The supplied form contained errors
            print(form.errors)
    context_dict={'form':form, 'store':store_tmp }
    context_dict['advertisements'] = advertiment_list_by_store(store_tmp)
    return render(request, 'queueweb/customer_register.html', context=context_dict)

def customer_status(request, store_name_slug, customer_id):
    store_tmp = Store.objects.get(slug=store_name_slug)
    customer = Customer.objects.get(id = customer_id)
    queue = customer.queue
    # number_in_line should be indivitual customer 
    number_in_line = customer.potential_wait_time/store_tmp.store_average_waiting_time_for_person - customer.number_of_people
    #number_in_line = queue.number_people_waiting - customer.number_of_people
    cus_num_before = int(number_in_line)
    context_dict = {}
    context_dict = {'store':store_tmp, 'queue':queue,'customer':customer, 'number_in_line':cus_num_before}
    if customer.Customerueue_id == -2:
        return redirect(reverse('customer_ticket',
                    kwargs={'store_name_slug':store_name_slug, 'customer_id':customer_id}))
    context_dict['advertisements'] = advertiment_list_by_store(store_tmp)
    return render(request,'queueweb/customer_status.html',context=context_dict) 


def customer_ticket(request,store_name_slug, customer_id):
    # my_dict = {'insert':"You're in the line!"}
    store_tmp = Store.objects.get(slug=store_name_slug)
    customer = Customer.objects.get(id = customer_id)
    real_wait_time = real_waiting_time(customer)
    # get the promocode (not include active)
    promocodes = PromoCode.objects.filter(store_id = store_tmp,start_date__lte=timezone.now(),end_date__gte=timezone.now(),wait_time__lte=real_wait_time)
    context_dict = {}
    ticket_dict = {'store':store_tmp.store_name,'customer.id':customer.id, 
    'customer.number_of_people':customer.number_of_people}
    customer_ticket = qrcode.make(ticket_dict)
    customer_ticket_path = 'queueweb/static/' 
    filename = store_tmp.store_name +'-temp-'+str(customer_id) +'.png'
    savename = customer_ticket_path + filename
    print(filename)
    customer_ticket.save(savename)
    #save_path = 'queueweb/static/'
    context_dict = {'customer':customer,'filename':filename}
    context_dict['advertisements'] = advertiment_list_by_store(store_tmp)
    context_dict['promocodes'] = promocodes
    context_dict['timediff'] = real_wait_time
    return render(request,'queueweb/customer_ticket.html',context=context_dict) 

def customer_leave(request, store_name_slug, customer_id):
    # this function deteremines what custermer will do when he/she decides to leave the queue

    if request.method == 'POST':
        store_tmp = Store.objects.get(slug=store_name_slug)
        customer = Customer.objects.get(id = customer_id)
        queue = customer.queue
        cus_q_id_tmp = customer.Customerueue_id
        if cus_q_id_tmp < 0:
            context_dict = {'store':store_tmp, 'customer':customer }
            return render(request,'queueweb/customer_leave.html',context=context_dict)

        else:
            # modify the left customerqueue id to -1, show every one who is nolonger waitting in the queue, customerueue_id is -1
            customer.Customerueue_id = -4
            customer.save()
            # the condition when the left customer is middle of the queue, others behand him/her will move forward
            while (cus_q_id_tmp < queue.last_Customerueue_id):
                cus_next = Customer.objects.get(queue = queue, Customerueue_id = cus_q_id_tmp + 1)
                cus_next.Customerueue_id = cus_q_id_tmp
                cus_next.potential_wait_time = cus_next.potential_wait_time - customer.number_of_people * store_tmp.store_average_waiting_time_for_person
                cus_q_id_tmp += 1
                cus_next.save()

            #if cus_q_id_tmp == queue.last_Customerueue_id:
        
            queue.last_Customerueue_id = queue.last_Customerueue_id - 1
            queue.current_waiting_time = queue.current_waiting_time - customer.number_of_people * store_tmp.store_average_waiting_time_for_person
            queue.number_people_waiting = queue.number_people_waiting - customer.number_of_people
        
            queue.save()
    
            context_dict = {}
            context_dict = {'store':store_tmp, 'customer':customer }
            context_dict['advertisements'] = advertiment_list_by_store(store_tmp)

            return render(request,'queueweb/customer_leave.html',context=context_dict)

    store_tmp = Store.objects.get(slug=store_name_slug)
    customer = Customer.objects.get(id = customer_id)
    context_dict = {'store':store_tmp, 'customer':customer }
    context_dict['advertisements'] = advertiment_list_by_store(store_tmp)

    return render(request,'queueweb/customer_leave.html',context=context_dict)


def customer_left_store_test(request, store_name_slug):
    # this function is a testing function, to tested the motion sensor's functionality
    store_tmp = Store.objects.get(slug=store_name_slug)
    context_dict['advertisements'] = advertiment_list_by_store(store_tmp)
    queue = Queue.objects.get(store = store_tmp,queuedate=datetime.date.today())

    if request.method == 'POST':
        # calculate how many persons could enter the store
        
        store_tmp.store_current_count -= 1
        store_tmp.save()
        diff = store_tmp.store_capacity - store_tmp.store_current_count
        # if there is no customer in queue
        # if queue.first_Customerueue_id == queue.last_Customerueue_id:
        #    return render(request, 'test.html') 
        # find the customer who is the first in queue
        customer_enter = Customer.objects.get(queue = queue, Customerueue_id = queue.first_Customerueue_id + 1)
        # the first cus in queue cannot enter
        if diff < customer_enter.number_of_people:
            return render(request,'queueweb/customer_left_store_test.html')
        
        # the first cus in queue can enter the store
        else:
            cus_q_id_tmp = customer_enter.Customerueue_id
            # if the cus can enter the store, set it's customerueue_id to -2
            customer_enter.Customerueue_id = -2
            # customer_enter.send_ticket() - haven't add this function
            customer_enter.save()
            # update all others in queue
            queue.first_Customerueue_id += 1
            decreased_time = customer_enter.number_of_people * store_tmp.store_average_waiting_time_for_person

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
def leave_case(request):# what happened when the motion sensor detect customer left the store

    if request.method == "GET":
        return HttpResponse("this is GET method")
    elif request.method == "POST":
        
        print("You are here!") # print for debug purpose
        
        req_dict = request.POST.dict()
        store_id = req_dict.get('store_id')

        store_tmp = Store.objects.get(store_id = store_id)
        queue = Queue.objects.get_or_create(store = store_tmp,queuedate=datetime.date.today())[0]

        diff = store_tmp.store_capacity - store_tmp.store_current_count
        # if there is no customer in queue
        # if queue.first_Customerueue_id == queue.last_Customerueue_id:
        #    return render(request, 'test.html') 
        # find the customer who is the first in queue
        customer_enter = Customer.objects.get(queue = queue, Customerueue_id = queue.first_Customerueue_id + 1)
        if diff < customer_enter.number_of_people:
            return render(request,'queueweb/customer_left_store_test.html')
        else:
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

        return HttpResponse("this is POST method")

# deal with http post request to ask for qrcode (store based)
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
            entry_or_not = queue_manager().check_space(store_id,customer_number) # wrapper function to check space
            if entry_or_not == False:
                store_interested_qrcode = generate_qrcode(store_id)
            else:
                store_interested_qrcode = None            
            overall_return_dict = {"REPLY":entry_or_not, 'QRCODE' :store_interested_qrcode}
            json_string = json.dumps(overall_return_dict)
            return HttpResponse(json_string, content_type =  "text/html; charset=utf-8")
        elif service == 'REGISTER': # for testing purpose, no need to be compatable with cloud service
            store_id = req_dict.get('store_id')
            customer_number = int(req_dict.get('customer_numbers'))
            phone_number = req_dict.get('phone_number')
            register_or_not, c_id = queue_manager().register_customer(store_id,customer_number,phone_number)
            overall_return_dict = {"REPLY":register_or_not, 'C_id' :c_id}
            json_string = json.dumps(overall_return_dict)
            return HttpResponse(json_string, content_type =  "text/html; charset=utf-8")
        elif service == 'LEAVE':
            store_id = req_dict.get('store_id')
            invited_or_not = queue_manager().update_queue(store_id)
            return HttpResponse("The server knows people has left, and we have checked the store")        
        elif service == 'CHECKIN':
            store_id = req_dict.get('store_id')
            customer_id = req_dict.get('customer_id')
            validate_or_not, customer_number = queue_manager().validate_checkin(store_id,customer_id )
            overall_return_dict = {"REPLY":validate_or_not, 'customer_number' :customer_number}
            json_string = json.dumps(overall_return_dict)
            return HttpResponse(json_string, content_type =  "text/html; charset=utf-8")
        else:
            return HttpResponseNotFound('<h1>illegal request</h1>')

   
@csrf_exempt
def test_case(request):
    input_dict = {"SERVICE":"ENTRY", "store_id":1, "customer_numbers":5}
    json_string = json.dumps(input_dict)
    #return  requests.get(url = "http://localhost:8000/queueweb/")
    A = requests.post(url = "http://localhost:8000/queueweb/",data = input_dict ).content
    #print(type(A))
    return HttpResponse(A)
    #return HttpResponseNotFound('<h1>illegal request</h1>')