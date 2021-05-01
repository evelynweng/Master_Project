from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from helperfunction import dataHandler, doService

@csrf_exempt 
# Create your views here.
def index(request):
    """Engress point of the cloudservice application
    Args:
        request (WSGIRequest): https://github.com/django/django/blob/main/django/core/handlers/wsgi.py#L64

    Returns:
        HTTPResponse:
    """

    # print(request, type(request))


    if request.method == "GET":
        return HttpResponse("this is GET method")
    elif request.method == "POST":
        
        # get the dictionary from httpRequest->QueruDict->dict
        recv_dict = request.POST.dict()

        # get the label of service
        VALIDTAG ="CMPE295"
        SERVICETAG = "SERVICE"
        SERVICE ={
            'LOGIN': classmethod(doService.do_login),
            'REGISTER': classmethod(doService.do_reg),
            'MASK': classmethod(doService.do_detect),
            'CHECKIN': classmethod(doService.do_checkin), 
        }

        ''' 
        # dictionary field:
            valid_tag + service_tag + items (different according to service)
        '''
        # check if the packet is valid packet.
        # check if service(key) exist
        # check type of service(value) exist
        # be careful, if not find SERVICETAG first, recv_dict[SERVICETAG] will compiler error
        if VALIDTAG not in recv_dict or not (SERVICETAG in recv_dict and recv_dict.get(SERVICETAG, default=None) in SERVICE):
            return HttpResponseNotFound('<h1>illegal request</h1>')
        
        
        request_service = recv_dict[SERVICETAG] # str: login, register, mask
        response = SERVICE.get(request_service, classmethod(doService.do_nothing))(recv_dict)  # forward to designate service module, default: donothing
        
        return response






