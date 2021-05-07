from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# modified by xm
from apidatabase.models import Store_q, Queue_q, Customer_q
from queueweb.forms import CustomerForm
from django.shortcuts import redirect
from django.urls import reverse
import datetime
import qrcode
# def detail(request, question_id):
#    return HttpResponse("You're looking at question %s." % question_id)



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
    store_list = Store_q.objects.order_by('name')
    queue_list = Queue_q.objects.order_by('queuedate')
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
        store_tmp = Store_q.objects.get(slug=store_name_slug)

        # Retrieve all of the associated queues
        # The filter() will return a list of queues or an empty list
        queue = Queue_q.objects.get_or_create(store = store_tmp, queuedate = datetime.date.today())[0]
        # Add results list to the template context under name queues.
        context_dict['queue'] = queue

        # Add the store object from db to the context dictionary
        context_dict['store'] = store_tmp
    
    except store_tmp.DoesNotExist:
        context_dict['store'] = None
        context_dict['queue'] = None

    return render(request,'queueweb/queue_status.html',context=context_dict)

def customer_register(request,store_name_slug):
    store_tmp = Store_q.objects.get(slug=store_name_slug)
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            if store_tmp:
                customer = form.save(commit=False)
                customer.store = store_tmp
                q = Queue_q.objects.get_or_create(store = store_tmp,queuedate=datetime.date.today())[0]
                customer.queue = q
                customer.customer_queue_id = q.last_customer_queue_id + 1
                if q.last_customer_queue_id > 0:
                    former_customer = Customer_q.objects.get(queue = q, customer_queue_id = q.last_customer_queue_id)
                    customer.potential_wait_time = former_customer.potential_wait_time + former_customer.number_of_people * store_tmp.average_waiting_time_for_person
                
                q.last_customer_queue_id = customer.customer_queue_id
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
    store_tmp = Store_q.objects.get(slug=store_name_slug)
    customer = Customer_q.objects.get(id = customer_id)
    queue = customer.queue
    number_in_line = queue.number_people_waiting - customer.number_of_people
    context_dict = {}
    context_dict = {'store':store_tmp, 'queue':queue,'customer':customer, 'number_in_line':number_in_line}
    if customer.customer_queue_id == -2:
        return render(request,'queueweb/customer_ticket.html',context=context_dict)
    

    return render(request,'queueweb/customer_status.html',context=context_dict) 

def customer_ticket(request,store_name_slug, customer_id):
    # my_dict = {'insert':"You're in the line!"}
    store_tmp = Store_q.objects.get(slug=store_name_slug)
    customer = Customer_q.objects.get(id = customer_id)
    
    
    return render(request,'queueweb/customer_ticket.html') 

def customer_leave(request, store_name_slug, customer_id):

    if request.method == 'POST':
        store_tmp = Store_q.objects.get(slug=store_name_slug)
        customer = Customer_q.objects.get(id = customer_id)
        queue = customer.queue
        cus_q_id_tmp = customer.customer_queue_id
        if cus_q_id_tmp < 0:
            context_dict = {'store':store_tmp, 'customer':customer }
            return render(request,'queueweb/customer_leave.html',context=context_dict)

        else:
            customer.customer_queue_id = -1
            customer.save()
            while (cus_q_id_tmp < queue.last_customer_queue_id):
                cus_next = Customer_q.objects.get(queue = queue, customer_queue_id = cus_q_id_tmp + 1)
                cus_next.customer_queue_id = cus_q_id_tmp
                cus_next.potential_wait_time = cus_next.potential_wait_time - customer.number_of_people * store_tmp.average_waiting_time_for_person
                cus_q_id_tmp += 1
                cus_next.save()

            if cus_q_id_tmp == queue.last_customer_queue_id:
        
                queue.last_customer_queue_id = queue.last_customer_queue_id - 1
                queue.current_waiting_time = queue.current_waiting_time - customer.number_of_people * store_tmp.average_waiting_time_for_person
                queue.number_people_waiting = queue.number_people_waiting - customer.number_of_people
        
                queue.save()
    
            context_dict = {}
            context_dict = {'store':store_tmp, 'customer':customer }

            return render(request,'queueweb/customer_leave.html',context=context_dict)

    store_tmp = Store_q.objects.get(slug=store_name_slug)
    customer = Customer_q.objects.get(id = customer_id)
    context_dict = {'store':store_tmp, 'customer':customer }

    return render(request,'queueweb/customer_leave.html',context=context_dict)


def customer_left_store_test(request, store_name_slug):
    store_tmp = Store_q.objects.get(slug=store_name_slug)
    queue = Queue_q.objects.get(store = store_tmp,queuedate=datetime.date.today())

    if request.method == 'POST':
        queue.current_customer_in_store -= 1
        queue.save()
        # calculate how many persons could enter the store
        diff = store_tmp.capacity - queue.current_customer_in_store
        # find the customer who is the first in queue
        customer_enter = Customer_q.objects.get(queue = queue, customer_queue_id = queue.first_customer_queue_id + 1)
        if diff < customer_enter.number_of_people:
            return render(request,'queueweb/customer_left_store_test.html')
        else:
            cus_q_id_tmp = customer_enter.customer_queue_id
            customer_enter.customer_queue_id = -2
            # customer_enter.send_ticket() - haven't add this function
            customer_enter.save()
            queue.first_customer_queue_id += 1
            decreased_time = customer_enter.number_of_people * store_tmp.average_waiting_time_for_person
            # consume customer_enter already enters the store, actually queue.current_customer_in_store should be 
            # modified by people leave store and people enter store
            queue.current_customer_in_store += customer_enter.number_of_people
            queue.current_waiting_time = queue.current_waiting_time - decreased_time
            queue.number_people_waiting = queue.number_people_waiting - customer_enter.number_of_people
            queue.save()
            while cus_q_id_tmp < queue.last_customer_queue_id:
                cus_next = Customer_q.objects.get(queue = queue, customer_queue_id = cus_q_id_tmp + 1)
                cus_next.potential_wait_time = cus_next.potential_wait_time - decreased_time
                cus_next.save()
                cus_q_id_tmp += 1

    return render(request,'queueweb/customer_left_store_test.html')
