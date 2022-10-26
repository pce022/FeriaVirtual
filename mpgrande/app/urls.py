import django
from django.contrib.auth import views
from django.urls import path
from django.urls.conf import include
from app.views import *
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import routers
from django.views.generic import TemplateView


router = routers.DefaultRouter()

urlpatterns = [
    path('', home, name='home'),
    path('index/', index, name='index'),
    path('register/', register, name='register'),
    path('message_register/', message_register, name ='message_register'),
    #User
    path('create_user/', create_user, name ='create_user'),
    path('list_user/', list_user, name ='list_user'),
    path('delete_user/<id>/', delete_user, name ='delete_user'),
    path('modify_user/<id>/', modify_user, name ='modify_user'),
    #Staff
    path('create_staff/', create_staff, name ='create_staff'),
    path('list_staff/', list_staff, name ='list_staff'),
    path('delete_staff/<id>/', delete_staff, name ='delete_staff'),
    path('modify_staff/<id>/', modify_staff, name ='modify_staff'),
    #Product
    path('create_product/', create_product, name ='create_product'),
    path('post_create_product/', post_create_product, name ='post_create_product'),
    path('list_product/', list_product, name ='list_product'),
    path('delete_product/<id>/', delete_product, name ='delete_product'),
    path('delete_post_product/<id>/', delete_post_product, name ='delete_post_product'),
    path('modify_product/<id>/', modify_product, name ='modify_product'),
    path('modify_post_product/<id>/', modify_post_product, name ='modify_post_product'),
    #Sales
    path('my_sales/', my_sales, name ='my_sales'),
    path('create_sale/<id>', create_sale, name ='create_sale'),
    path('list_sales/', list_sales, name ='list_sales'),
    path('delete_sales/<id>/', delete_sales, name ='delete_sales'),
    path('modify_sales/<id>/', modify_sales, name ='modify_sales'),


] 