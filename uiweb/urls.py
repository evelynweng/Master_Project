from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ex: /cloudservice/
    #path('', views.index, name="index"), 
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    path('', views.home, name = 'Home_Page'),
    #path('about/', views.about, name = 'About_Page'),
    path('login/', views.login, name = 'Login'), 
    path('storeRegister/', views.storeRegistration, name = 'Store_Registration'),
    #path('registration_success/', views.registration_success, name = 'registration_success'),
    path('logout/', views.logout, name = 'Logout'), 
    path('profile/', views.profile, name = 'Profile'), 
    path('activate-user/<uidb64>/<token>', views.activate_user, name = 'Activate'),
    path('generateAdCoupon/', views.generateAdCoupon, name = 'GenerateAdCoupon'), 
    path('generatePromoCode/', views.generatePromoCode, name = 'GeneratePromoCode'), 
    path('passwordReset/', views.passwordReset, name = 'Password_Reset'),
    path('password_reset_cnf/<uidb64>/<token>', views.password_reset_cnf, name = 'Password_Reset_Confirm'),    
    path('getStarted/', views.getStarted, name = 'Get_Started'), 
    
         
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)