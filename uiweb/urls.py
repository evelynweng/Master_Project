from django.urls import path

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
    
]