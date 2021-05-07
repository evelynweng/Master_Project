from django.urls import path

from . import views

urlpatterns = [
    # ex: /cloudservice/
    path('', views.index, name="index"),
    path('store/<slug:store_name_slug>/',views.queue_status,name='queue_status'),
    path('store/<slug:store_name_slug>/customer_register',views.customer_register,name='customer_register'),
    path('store/<slug:store_name_slug>/<int:customer_id>/customer_status',views.customer_status,name='customer_status'),
    path('customer_ticket',views.customer_ticket,name='customer_ticket'),
    path('store/<slug:store_name_slug>/<int:customer_id>/customer_leave',views.customer_leave,name='customer_leave'),
    path('store/<slug:store_name_slug>/customer_left_store_test',views.customer_left_store_test,name='customer_left_store_test'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
]