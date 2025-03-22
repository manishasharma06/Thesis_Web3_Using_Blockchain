"""supply_chain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from supplyChain_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = "home"),
    path('track_order/<int:order_id>/', track_order, name="track_order"),
    path('send_receipt/<int:re_type>/<int:order_id>/', send_receipt, name = "send_receipt"),
    path('merchant_page/<int:option>/<int:selected_id>/', merchant_page, name = "merchant_page"),
    path('merchant_update/<int:option>/<int:selected_id>/', merchant_update, name = "merchant_update"),
    path('contact_mail/<int:order_id>/', contact_mail, name = "contact_mail"),
    path('company_landing_page/', company_landing_page, name = "company_landing_page"),
    path('company_inventory/', company_inventory, name = "company_inventory"),
    path('delete_car/<int:car_id>/', delete_car, name="delete_car"),
    path('company_orders/', company_orders, name="company_orders"),
    path('company_actions/<int:option>/', company_actions, name="company_actions"),
    path('update_status/<int:id>/', update_status, name='update_status'),
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),
    path('initiate_refund/<int:order_id>/', initiate_refund, name='initiate_refund'),
    path('client/', client, name="client"),
    path('client_order/<int:car_id>/<int:user_id>/', client_order, name="client_order"),
    path('place_order/<int:car_id>/<int:user_id>/<order_amt>/<updated_wallet>/', place_order, name="place_order"),
    path('client_cancel/<int:id>/', request_cancellation, name="client_cancel"),
    path('cancel_request/<int:id>/', cancellation, name="cancel_request"),
    path('handle_request/<int:request_id>/', handle_request, name="handle_request"),
    path('login/<int:user_id>/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('success_page/', success_page, name="success_page"),
    path('merchant_action/<int:merch_id>/<int:order_id>/', merchant_action, name="merchant_action"),
    path('blockchain/', blockchain, name="blockchain"),
]
