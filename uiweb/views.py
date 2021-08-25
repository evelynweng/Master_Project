from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#from .models import Store
from apidatabase.models import Store
from .forms import StoreRegistrationForm, LoginForm
from .decorators import user_login_required
#from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if Store.objects.filter(email=email, password=password).exists():
            user = Store.objects.get(email=email)
            ###
            if user and not user.is_email_verified:
                messages.add_message(request, messages.ERROR,
                                 'Email is not verified, please check your email inbox')
                #return render(request, 'authentication/login.html', context, status=401)
                return render(request, 'uiweb/login.html', {'form': form})
            ###
            request.session['user_id'] = user.store_id # This is a session variable and will remain existing as long as you don't delete this manually or clear your browser cache
            owner_name = user.owner_first_name + user.owner_last_name
            print(owner_name)
            return redirect('Home_Page')
        else:
            messages.warning(request, "Wrong email or password.\n Please try again.")
    return render(request, 'uiweb/login.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def logout(request):
    if 'user_id' in request.session:
      del request.session['user_id'] # delete user session
    return redirect('Home_Page')    

def get_user(request):
    user = Store.objects.get(store_id=request.session['user_id'])   
    return user 
###
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('uiweb/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )
    #email.send() 
    EmailThread(email).start()                    
###

def storeRegistration(request):
    if request.method == 'POST':
        form = StoreRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            #inactive_user = send_verification_email(request, form)
            ###
            user = Store.objects.get(email = email)
            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,
                                 'We sent you an email to verify your account.Please check your inbox.')
            #return redirect('registration_success') 
            return redirect('Login')
            ###    
        else:
            print(StoreRegistrationForm.errors)         
    else:
        form = StoreRegistrationForm()
    context = {'form': form}
    return render(request, 'uiweb/storeRegister.html', context)

###
def activate_user(request, uidb64, token):
    
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = Store.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('Login'))

    return render(request, 'uiweb/activate-failed.html', {"user": user})
###




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




