from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # ex: /cloudservice/
    #path('', views.index, name="index"), 
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    path('', views.home, name = 'Home_Page'),
    path('about/', views.about, name = 'About_Page'),
    path('login/', views.login, name = 'Login'), 
    path('storeRegister/', views.storeRegistration, name = 'Store_Registration'),
    path('registration_success/', views.registration_success, name = 'registration_success'),
    path('logout/', views.logout, name = 'Logout'), 
    path('profile/', views.profile, name = 'Profile'), 
    path('activate-user/<uidb64>/<token>', views.activate_user, name = 'Activate'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)