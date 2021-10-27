from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#from .models import Store
from apidatabase.models import Store, Advertisement
from .forms import StoreRegistrationForm, LoginForm,ProfileUpdateForm,GenerateAdCouponForm,GeneratePromoCodeForm,ResetPassword_EmailForm,ResetPassword_PasswordForm
from .decorators import user_login_required
#from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.urls import reverse
import threading
from PIL import Image 
from PIL import ImageFont
from PIL import ImageDraw

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

def home(request):
    if 'user_id' in request.session:
        store_info = get_user(request)
        store_id =store_info.store_id
        owner_first_name = store_info.owner_first_name
        profile_pic = store_info.profile_pic
        context={"store_id":store_id,"owner_first_name":owner_first_name, "profile_pic":profile_pic}
        return render(request,'uiweb/home3.html',{'context':context})
    
    return render(request, 'uiweb/home3.html')

"""def about(request):
    return render(request, 'uiweb/about.html')"""        

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
@user_login_required
def logout(request):
    if 'user_id' in request.session:
      del request.session['user_id'] # delete user session
    return redirect('Home_Page')    

def get_user(request):
    user = Store.objects.get(store_id=request.session['user_id'])   
    return user 

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


def storeRegistration(request):
    if request.method == 'POST':
        form = StoreRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            user = Store.objects.get(email = email)
            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,
                                 'We sent you an email to verify your account.Please check your inbox.')
            return redirect('Login')   
        else:
            print(StoreRegistrationForm.errors)         
    else:
        form = StoreRegistrationForm()
    context = {'form': form}
    return render(request, 'uiweb/storeRegister.html', context)

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


def registration_success(request):
    return render(request, 'uiweb/success.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_login_required
def profile(request):
    info= get_user(request)
    
    if request.method == 'POST':
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=info)
       
        if profile_update_form.is_valid:
            profile_update_form.save()
            messages.add_message(request, messages.SUCCESS,
                             'Your profile has been updated!')
            return redirect('Profile')
    else:
            profile_update_form = ProfileUpdateForm(instance = info)

    store_id =info.store_id
    profile_pic = Store.objects.get(store_id = store_id)

    context = {'profile_update_form':profile_update_form,'profile_pic':profile_pic, 'store_name':info.store_name, 'email':info.email,"owner_first_name":info.owner_first_name}
    return render(request, 'uiweb/profile.html', context)
 
@user_login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def generateAdCoupon(request):
    info= get_user(request)
    
    if request.method == 'POST':
        generate_ad_coupon_form = GenerateAdCouponForm(request.POST, request.FILES)
       
        if generate_ad_coupon_form.is_valid():
            ad = generate_ad_coupon_form.save(commit=False)
            ad.store_id = Store.objects.get(store_id = info.store_id)
            store_name = Store.objects.get(store_name = info.store_name)
    
            font_store_name = ImageFont.truetype("/Library/fonts/Georgia Italic.ttf", 34)
            font_ad = ImageFont.truetype("/Library/fonts/Comic Sans MS.ttf", 40)  #Chalkduster.ttf
            font_validity= ImageFont.truetype("/Library/fonts/Arial.ttf", 15) #Arial.ttf
            img = Image.open(ad.ad_image)
            draw = ImageDraw.Draw(img)
            draw.text((300, 10),str(store_name)[2:],(255,255,255),font=font_store_name)
            draw.text((45, 130),ad.ad_description,(255,255,255),font=font_ad)
            draw.text((80,270 ),"Starts from "+str(ad.start_date)[:11]+" till "+str(ad.end_date)[:11],(255,255,255),font=font_validity)

            img.save('media/ad_code.jpg')
            if ad.start_date>ad.end_date:
                messages.add_message(request, messages.WARNING,
                             'End date should be later date than the start date.')
            else:
                ad.save()
                Advertisement.objects.filter(pk=ad.ad_id).update(ad_image='ad_code.jpg')
                messages.add_message(request, messages.SUCCESS,
                             'Coupon has been generated!')
                return redirect('GenerateAdCoupon')
    else:
            generate_ad_coupon_form = GenerateAdCouponForm()

    store_id =info.store_id
    profile_pic = Store.objects.get(store_id = store_id)

    context = {'generate_ad_coupon_form':generate_ad_coupon_form,'profile_pic':profile_pic}
    return render(request, 'uiweb/generateAdCoupon.html', context)    
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_login_required
def generatePromoCode(request):
    info= get_user(request)
    
    if request.method == 'POST':
        generate_promocode_form = GeneratePromoCodeForm(request.POST, request.FILES)
       
        if generate_promocode_form.is_valid():
            promo =generate_promocode_form.save(commit=False)
            promo.store_id = Store.objects.get(store_id = info.store_id)
            if promo.start_date>promo.end_date:
                messages.add_message(request, messages.WARNING,
                             'End date should be later date than the start date.')
            else:                 
                generate_promocode_form.save()
                messages.add_message(request, messages.SUCCESS,
                             'Coupon has been generated!')
                return redirect('GeneratePromoCode')   
    else:
            generate_promocode_form = GeneratePromoCodeForm()

    store_id =info.store_id
    profile_pic = Store.objects.get(store_id = store_id)

    context = {'generate_promocode_form':generate_promocode_form,'profile_pic':profile_pic}
    return render(request, 'uiweb/generatePromoCode.html', context)  

def passwordReset(request):
    if request.method == 'POST':
        resetPwdForm=ResetPassword_EmailForm(request.POST)
        if resetPwdForm.is_valid():
            data = resetPwdForm.cleaned_data
            userEmail= data['email']
            if Store.objects.filter(email=userEmail).exists():
                user = Store.objects.get(email = userEmail)
                send_pwd_reset_email(user, request)
                #print(userEmail)
                messages.add_message(request, messages.SUCCESS,
                                 'We have sent you a link for password reset on your email.Please check your inbox.')
                #sreturn redirect('Password_Reset_Confirm')  
            else:
                messages.add_message(request,messages.ERROR,'This email id is not registered. Please create an account.')
                    
    else:
        resetPwdForm=ResetPassword_EmailForm()       
    return render(request,'uiweb/Password_Reset.html',{'resetPwdForm':resetPwdForm})
       
def send_pwd_reset_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Reset Password link'
    email_body = render_to_string('uiweb/password_reset_mail.html', {
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


def password_reset_cnf(request, uidb64, token):    
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Store.objects.get(pk=uid)
    except Exception as e:
        user = None
    if request.method == 'POST':
        resetPwd_passwordForm=ResetPassword_PasswordForm(request.POST)
        if resetPwd_passwordForm.is_valid():
            data = resetPwd_passwordForm.cleaned_data
            pwd= data['password']
            cnf_pwd= data['confirm_password']
            if pwd==cnf_pwd:
                Store.objects.filter(email=user.email).update(password=pwd)
                messages.add_message(request, messages.SUCCESS,
                                 'Your password has been reset.You may login now.')      
    else:
        resetPwd_passwordForm=ResetPassword_PasswordForm()

    return render(request,'uiweb/Password_Reset_Confirm.html',{'resetPwd_passwordForm':resetPwd_passwordForm})    

def getStarted(request):
    return render(request, 'uiweb/getStarted.html')    