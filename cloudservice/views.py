from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# def detail(request, question_id):
#    return HttpResponse("You're looking at question %s." % question_id)



@csrf_exempt 
# Create your views here.
def index(request):
    """Engress point of the cloudservice application
    Args:
        request (WSGIRequest): https://github.com/django/django/blob/main/django/core/handlers/wsgi.py#L64

    Returns:
        HTTPResponse:
    """
    # Uncomment this line to play with the database API
    # play_with_database()
    print(request, type(request))


    if request.method == "GET":
        return HttpResponse("this is GET method")
    elif request.method == "POST":
        q = request.POST
        l = list(q.values())
        return HttpResponse(l[0])


