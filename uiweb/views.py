from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#from .models import Store
from apidatabase.models import Store
from .forms import StoreRegistrationForm, LoginForm

# def detail(request, question_id):
#    return HttpResponse("You're looking at question %s." % question_id)


''' 
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
 '''

def home(request):
    return render(request, 'uiweb/home.html')


def about(request):
    return render(request, 'uiweb/about.html')        

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if Store.objects.filter(email=email, password=password).exists():
            user = Store.objects.get(email=email)
            # request.session['user_id'] = user.id # This is a session variable and will remain existing as long as you don't delete this manually or clear your browser cache
            return redirect('Home_Page')
        else:
            messages.warning(request, "Wrong email or password.\n Please try again.")
    return render(request, 'uiweb/login.html', {'form': form})

def storeRegistration(request):
    if request.method == 'POST':
        form = StoreRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('store_name')
            #inactive_user = send_verification_email(request, form)
            return redirect('registration_success')    
        else:
            print(StoreRegistrationForm.errors)         
    else:
        form = StoreRegistrationForm()
    context = {'form': form}
    return render(request, 'uiweb/storeRegister.html', context)


def registration_success(request):
    return render(request, 'uiweb/success.html')




