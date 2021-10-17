from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#from .models import Store
from apidatabase.models import Store
from .forms import StoreRegistrationForm, LoginForm
from .decorators import user_login_required
#from django.contrib.auth import authenticate,login,logout

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
#@user_login_required
def home(request):
    if 'user_id' in request.session:
        user_name = get_user(request)
        print(user_name)
        owner_name = user_name.owner_first_name + " " + user_name.owner_last_name
        print(owner_name)
        return render(request, 'uiweb/home2.html', {'user_name': user_name, 'owner_name':owner_name}) #this is temporary page to show logout
    else:
        return render(request, 'uiweb/home.html')    

    ''' user = get_user(request)
    return render(request, 'uiweb/home.html', {'user': user}) '''

def about(request):
    return render(request, 'uiweb/about.html')        

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if Store.objects.filter(email=email, password=password).exists():
            user = Store.objects.get(email=email)
            request.session['user_id'] = user.store_id # This is a session variable and will remain existing as long as you don't delete this manually or clear your browser cache
            owner_name = user.owner_first_name + user.owner_last_name
            print(owner_name)
            return redirect('Home_Page')
        else:
            messages.warning(request, "Wrong email or password.\n Please try again.")
    return render(request, 'uiweb/login.html', {'form': form})

def logout(request):
    if 'user_id' in request.session:
      del request.session['user_id'] # delete user session
    return redirect('Home_Page')    

def get_user(request):
    user = Store.objects.get(store_id=request.session['user_id'])   
    return user 

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

def profile(request):
    if 'user_id' in request.session:
        user_name = get_user(request)
        firstname = user_name.owner_first_name + "'s profile"
        name = user_name.owner_first_name + " " + user_name.owner_last_name
        store_name = user_name.store_name
        email = user_name.email
        phone = user_name.store_phone
        address = user_name.store_address
        url = user_name.store_url
        date_joined = user_name.registration_date
        context = {'name':name, 'store_name':store_name,'email':email,'phone':phone,'address':address,'url' : url, 'date_joined':date_joined}

    return render(request, 'uiweb/profile.html', {'context':context})    




