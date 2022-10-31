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
    #Request
    path('create_request/', create_request, name ='create_request'),
    path('producer_create_request/<id>/', producer_create_request, name ='producer_create_request'),
    path('modify_request/<id>/', modify_request, name ='modify_request'),
    path('modify_request_status/<id>/', modify_request_status, name ='modify_request_status'),
    path('delete_request/<id>/', delete_request, name ='delete_request'),
    path('list_request/', list_request, name ='list_request'),
    path('list_producer_request/', list_producer_request, name ='list_producer_request'),
    path('modify_list_producer_request/<id>/', modify_list_producer_request, name ='modify_list_producer_request'),
    path('delete_modify_list_producer_request/<id>/', delete_modify_list_producer_request, name ='delete_modify_list_producer_request'),
    path('approve_producer_client_request/<id>/', approve_producer_client_request, name ='approve_producer_client_request'),
    path('info_approve_request/<id>/', approve_producer_client_request, name ='info_approve_request'),
    path('reject_producer_client_request/<id>/', reject_producer_client_request, name ='reject_producer_client_request'),
    #Auction (Subasta)
    path('auction/<id>/', participate_auction, name ='participate_auction'),
    path('start_auction/<id>/', start_auction_participate, name ='start_auction_participate'),
    path('participate_auction_carrier/<id>/<id_subasta>', participate_auction_carrier, name ='participate_auction_carrier'),
    path('end_auction/<id>/<id2>/', end_auction, name ='end_auction'),
    path('list_auction/<id>/<nombreCliente>/<id_solicitud>/', list_auction, name ='list_auction'),
    path('delete_auction/<id>/', delete_auction, name ='delete_auction'),
    #Sale/Ticket
    path('sales_list/', sales_list, name ='sales_list'),
    path('create_ticket/<id>/', create_ticket, name ='create_ticket'),
    path('list_ticket/', list_ticket, name ='list_ticket'),
    path('list_ticket_trans/', list_ticket_trans, name ='list_ticket_trans'),
    path('list_ticket_producer/', list_ticket_producer, name ='list_ticket_producer'),
    path('list_ticket_client/', list_ticket_client, name ='list_ticket_client'),
    path('confirm_delivery<id>/', confirm_delivery, name ='confirm_delivery'),
    path('info_ticket/<id>/', info_ticket, name ='info_ticket'),
    #API
    path('api/', include(router.urls)),
    #PDF
    path('pdf_converterViews/<id>/', pdf_converterViews.as_view() , name ='pdf_converterViews'),
    path('pdf_converterTransViews/<id>/', pdf_converterTransViews.as_view() , name ='pdf_converterTransViews'),
    path('pdf_converterProductorViews/<id>/', pdf_converterProductorViews.as_view() , name ='pdf_converterProductorViews'),
    #Graphics
    path('graphics/', graphics, name = 'graphics'),



]