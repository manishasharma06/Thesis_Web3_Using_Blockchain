from django.shortcuts import render,redirect
from .forms import *
from .models import *
import datetime as dt
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
import hashlib

#Create a block for blockchain
def generate_hash(data):
    data_str = str(data)
    hash_object = hashlib.sha256(data_str.encode())
    hex_dig = hash_object.hexdigest()
    short_hash = hex_dig[:8]
    return short_hash

def blockchain(request):
    search_query = request.GET.get('search_query')
    if search_query:
        # Perform the search based on order ID or customer name
        order_id = search_query
        genesis = None
        block = None
        try:
            order = OrderModel.objects.get(order_id=order_id)
            msg = None
            try:
                genesis = BlockModel.objects.get(order=order, sender="Customer")
                block = BlockModel.objects.get(order=order, sender="Company")
                msg = None
            except BlockModel.DoesNotExist:
                msg = "Block does not exists"
        except OrderModel.DoesNotExist:
            msg = "Invalid Order ID."

        context = {
            "genesis" : genesis,
            "chain" : block,
            "msg" : msg
        }
        return render(request, 'blockchain_page.html', context)
    else:    
        return render(request, 'blockchain_page.html', {"msg" : "Search Order ID"})

#Configuration of mail to send receipts, updates and make contact
def config_mail(subject, message, mail_id, html_message):
    send_mail(
        subject,
        message,
        'vivekgamer.2019@gmail.com',
        [mail_id],
        fail_silently=False,
        html_message=html_message
    )

#Contact Customer via mail
def contact_mail(request, order_id):
    if request.method == "POST":
        subject = request.POST.get('subject')
        content = request.POST.get('content')
    order = OrderModel.objects.get(order_id=order_id)

    SentMailModel.objects.create(
        order = order,
        subject = subject,
        body = content
    )

    mail_id = order.user_id.email
    config_mail(subject, content, mail_id, html_message=None)
    return redirect('company_actions', option=3)

def send_receipt(request, re_type, order_id):
    order = OrderModel.objects.get(order_id=order_id)
    base_price = order.car_id.price
    if re_type == 1:
        subject = "Receipt for your Order From BMW.!"
        context = {
            "customer_name" : order.user_id.username,
            "model_name" : order.car_id.model,
            "order_id" : order.order_id,
            "amount" : order.order_amt,
            "base_amount" : base_price,
            'purchase_date' : order.dt,
            'type' : "send_receipt"
        }
        message = render_to_string('purchase_mail.html', context)
        mail_id = order.user_id.email
        config_mail(subject, message, mail_id, html_message=message)
    elif re_type == 2:
        request = RequestModel.objects.get(order=order)
        refund = RefundModel.objects.get(request=request)
        refund_id = refund.refund_id
        amount = refund.refund_amt
        refund_dt = refund.time
        subject = "Refund Receipt for your Order."
        context = {
            "customer_name" : order.user_id.username,
            "order_id" : order.order_id,
            "refund_id" : refund_id,
            "amount" : amount,
            "refund_date" : refund_dt,
            'type' : "send_refund_receipt"
        }
        message = render_to_string('purchase_mail.html', context)
        mail_id = order.user_id.email
        config_mail(subject, message, mail_id, html_message=message)
    else:
        print("Server Error : 500")

    return redirect('home')

#Contains create and update profile and order made.
def home(request):

    user_id = request.session.get('user_id') #checks if userid is in session or not

    # Check if user is logged in to account
    if user_id is not None:

        user_instance = UserModel.objects.get(user_id=user_id)

        if request.method == 'POST': #update ur profile
            update_form = UserForm(request.POST, instance=user_instance)
            if update_form.is_valid():
                update_form.save()
                return redirect('home')
            else:
                pass
        else:
            orders = OrderModel.objects.filter(user_id=user_id)
            update_form = UserForm(instance=user_instance)
        return render(request, 'home.html', {"update_form" : update_form, "orders" : orders})
    
    #Else shows all the accounts you can log into
    else:

        users = UserModel.objects.all()
        
        if request.method == "POST":
            data = UserForm(request.POST)
            if data.is_valid():
                data.save()

                context = {
                    "msg" : "User Created",
                    "fm" : UserForm,
                    "users" : users
                }

                return render(request, 'home.html', context)
            else:
                msg = data
                return render(request, 'home.html', {"msg" : msg, "users" : users})
        else:
            fm = UserForm()
            return render(request, 'home.html', {"fm" : fm, "users" : users})
        
def track_order(request, order_id):
    order = OrderModel.objects.get(order_id=order_id)
    transactions = TransactionModel.objects.filter(orders=order)
    return render(request, "track_order.html", {"transactions" : transactions, "order" : order})

def logout(request):
    request.session.clear()
    return redirect('home')
    
def login(request, user_id):
    request.session['user_id'] = user_id
    return redirect('client')
       
#Company Views starts here.
def company_landing_page(request):
    return render(request, 'company_landing_page.html')

def company_actions(request, option):
    search_query = request.GET.get('search_query')
    data = OrderModel.objects.all()
    requests = RequestModel.objects.all()
    transactions = None
    order_31 = None
    order_5 = OrderModel.objects.filter(status="Ready to Dispatch")
    msg = "Please Select Order ID"
    mails = None

    if search_query:
        # Perform the search based on order ID or customer name
        if option == 1:
            data = OrderModel.objects.filter(
                Q(order_id__icontains=search_query) | Q(user_id__username__icontains=search_query)
            )
        elif option == 2:
            order_id = search_query
            transactions = TransactionModel.objects.filter(orders__order_id=order_id)
        elif option == 31:
            order_id = search_query
            try:
                order_31 = OrderModel.objects.get(order_id=order_id)
                msg = order_id
                mails = SentMailModel.objects.filter(order=order_31).order_by('-sent_at')
                option = 3
            except OrderModel.DoesNotExist:
                msg = "ID does not exist!"
                option = 3
        elif option == 4:
            requests = RequestModel.objects.filter(
                Q(request_id__icontains=search_query) | Q(order__order_id__icontains=search_query)
            )
        elif option == 5:
            pass

    context = {
        'search_query': search_query,
        "data" : data,
        "option" : option,
        "requests" : requests,
        "transactions" : transactions,
        "order_31" : order_31,
        "orders_5" : order_5,
        "msg" : msg,
        "mails" : mails
    }
    return render(request, 'company_action.html', context)
    
def update_status(request, id):
    if request.method == "POST":
        new_status = request.POST.get('status')
        
        order = OrderModel.objects.get(order_id=id)

        if new_status=="1":
            order.status = "Confirmed"
            TransactionModel.objects.create(
                orders = order,
                user = order.user_id,
                action = "Confirmed"
            )
        elif new_status=="2":
            order.status = "At Assembly"
            TransactionModel.objects.create(
                orders = order,
                user = order.user_id,
                action = "At Assembly"
            )
        elif new_status=="3":
            order.status = "Ready to Dispatch"
            TransactionModel.objects.create(
                orders = order,
                user = order.user_id,
                action = "Ready to Dispatch"
            )
        elif new_status=="4":
            order.status = "Dispatched"
            TransactionModel.objects.create(
                orders = order,
                user = order.user_id,
                action = "Dispatched"
            )
            
        order.save()
        
    subject = "Update on Your Order Status!"
    context = {
        "customer_name" : order.user_id.username,
        "order_id" : order.order_id,
        "status" : order.status,
        'type' : "order_update"
    }
    message = render_to_string('purchase_mail.html', context)
    mail_id = order.user_id.email
    config_mail(subject, message, mail_id, html_message=message)

    return redirect('company_actions', option=1)

def cancel_order(request, order_id):

    order = OrderModel.objects.get(order_id=order_id)

    order.status = "Cancelled"

    TransactionModel.objects.create(
                orders = order,
                user = order.user_id,
                action = "Cancelled"
            )

    order.save()

    return redirect('company_actions', option=1)


def initiate_refund(request, order_id):

    order = OrderModel.objects.get(order_id=order_id)
    user_instance = UserModel.objects.get(user_id=order.user_id.user_id)
    order.status = "Cancelled & Refunded"

    refund_amt = order.order_amt * 0.75
    user_instance.wallet_amt = user_instance.wallet_amt + refund_amt
    
    TransactionModel.objects.create(
                orders = order,
                user = order.user_id,
                action = "Cancelled & Refunded"
            )

    order.save()
    user_instance.save()

    
    subject = "Refund Initiated for Your Order!"
    context = {
        "customer_name" : order.user_id.username,
        "order_id" : order.order_id,
        "status" : order.status,
        "refund_amt" : refund_amt,
        'type' : "initiated_refund"
    }
    message = render_to_string('purchase_mail.html', context)
    mail_id = order.user_id.email
    config_mail(subject, message, mail_id, html_message=message)

    return redirect('company_actions', option=1)


def company_orders(request):
    orders = OrderModel.objects.all()
    context = {
        "orders" : orders,
    }
    return render(request, 'company_orders.html', context)

def company_inventory(request):
        car_inventory = CarWarehouseModel.objects.all()
        if request.method == "POST":
            data = CarWarehouseForm(request.POST)
            if data.is_valid():
                data.save()
                msg = "Entry Created"
                fm = CarWarehouseForm()
                context = {
                    "fm" : fm,
                    "msg" : msg,
                    "car_inv" : car_inventory,
                }
                return render(request, 'company_inventory.html', context)
            else:
                msg = data
                context = {
                    "msg" : msg,
                    "car_inv" : car_inventory,
                }
                return render(request, 'company_inventory.html', context)
        else:
            fm = CarWarehouseForm()
            context = {
                    "fm" : fm,
                    "car_inv" : car_inventory,
                }
            return render(request, 'company_inventory.html', context)
        
def delete_car(request, car_id):
    car = CarWarehouseModel.objects.get(car_id=car_id)
    car.delete()
    return redirect('company_inventory')
    
def client(request):
    user_id = request.session.get('user_id')
    user = UserModel.objects.get(user_id=user_id)
    car_inventory = CarWarehouseModel.objects.all()
    context = {
        "user" : user,
        "car_inv" : car_inventory
    }
    return render(request, 'client.html', context)

def client_order(request,car_id,user_id):
    car = CarWarehouseModel.objects.get(car_id=car_id)
    user = UserModel.objects.get(user_id=user_id)
    date = dt.datetime.now()
    est_del = date + dt.timedelta(days=30)
    wallet_amt = user.wallet_amt
    final_price = car.price + (car.price * 0.19)
    updated_wallet = round(wallet_amt - final_price,0)
    context = {
        "user" : user,
        "car" : car,
        "final_price" : final_price,
        "est_del" : est_del,
        "updated_wallet" : updated_wallet
    }
    return render(request, 'client_order.html', context)

def place_order(request,car_id,user_id, order_amt, updated_wallet):
    car_instance = CarWarehouseModel.objects.get(car_id=car_id)
    user_instance = UserModel.objects.get(user_id=user_id)
    date = dt.datetime.now()
    est_del = date + dt.timedelta(days=30)
    order = OrderModel.objects.create(car_id=car_instance, user_id=user_instance, order_amt=float(order_amt), status="Confirming", dt=date, est_del=est_del)
    order_id = order.order_id
    request.session["order_id"] = order_id
    user_instance.wallet_amt = float(updated_wallet)
    user_instance.save()
    TransactionModel.objects.create(
                orders = order,
                user = order.user_id,
                action = "Order Placed"
            )
    hashed_order_id = generate_hash(order_id)
    BlockModel.objects.create(
        hash = hashed_order_id,
        previous_hash = None,
        order = order,
        sender = "Customer",
        receiver = "Company",
        amount = float(order_amt)
    )
    company = CompanyAccounts.objects.get(company_name="BMW")
    company_wallet = company.available_amt
    company.available_amt = company_wallet + float(order_amt)
    company.save()
    subject = "Thank You for Your Recent Car Purchase from Mercedes!"
    context = {
        'customer_name': user_instance.username,
        'car_model': car_instance.model,
        'type' : "purchase_made"
    }
    message = render_to_string('purchase_mail.html', context)
    mail_id = user_instance.email
    config_mail(subject, message, mail_id, html_message=message)
    return redirect('success_page')

def success_page(request):
    order_id = request.session.get('order_id')
    order = OrderModel.objects.get(order_id=order_id)
    context = {
        "order_id" : order_id,
        "order" : order
    }
    return render(request, "success_page.html", context)


def request_cancellation(request,id):
    order = OrderModel.objects.get(order_id=id)
    order_amt = order.order_amt
    deduction = order_amt * 0.25
    refund_amt = order_amt - deduction
    context = {
        'order' : order,
        'deduction' : deduction,
        'refund_amt' : refund_amt
    }
    return render(request, 'client_cancel.html', context)

def cancellation(request, id): #need to update the order status to "Request Cancellation" -- Done
    order = OrderModel.objects.get(order_id=id)
    if request.method == "POST":
        reason = request.POST.get("reason")
        RequestModel.objects.create(
                order = order,
                type = "Cancel",
                client_reason = reason,
                status = "Requested"
            )
        
        TransactionModel.objects.create(
                orders = order,
                user = order.user_id,
                action = "Requested Cancellation"
            )
        order.status = "Requested Cancellation"
        order.save()

    request_made = RequestModel.objects.get(order=order)
        
    subject = "Acknowledgement of Cancellation Request Confirmation!"
    context = {
        "customer_name" : order.user_id.username,
        'request_id': request_made.request_id,
        'type' : "request_cancellation"
    }
    message = render_to_string('purchase_mail.html', context)
    mail_id = order.user_id.email
    config_mail(subject, message, mail_id, html_message=message)
    return redirect("home")

def handle_request(request, request_id):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        requestm = RequestModel.objects.get(request_id=request_id)
        order = requestm.order
        # Check which button was clicked (Accept or Reject)
        if 'accept' in request.POST:
            requestm.status = "Accepted"
            requestm.company_reason = reason
            order.status = "Cancellation Accepted"
            order.save()
            requestm.save()

            refund_amt = order.order_amt * 0.75

            company = CompanyAccounts.objects.get(company_name="BMW")
            company_wallet = company.available_amt
            company.available_amt = company_wallet - float(refund_amt)
            company.save()
            
            TransactionModel.objects.create(
                orders = order,
                user = order.user_id,
                action = "Cancellation Accepted"
            )
            RefundModel.objects.create(
                request = requestm,
                refund_amt = refund_amt
            )

        elif 'reject' in request.POST:
            requestm.status = "Rejected"
            requestm.company_reason = reason
            order.status = "Cancellation Rejected"
            order.save()
            requestm.save()

            TransactionModel.objects.create(
                orders = order,
                user = order.user_id,
                action = "Cancellation Rejected"
            )
    
    subject = "Confirmation of Cancellation Request Status!"
    context = {
        "customer_name" : order.user_id.username,
        "order_id" : order.order_id,
        "status" : order.status,
        "reason" : requestm.company_reason,
        'type' : "request_update"
    }
    message = render_to_string('purchase_mail.html', context)
    mail_id = order.user_id.email
    config_mail(subject, message, mail_id, html_message=message)

    return redirect('company_actions', option=4)

#Merchant View Starts here.
def merchant_page(request, option, selected_id):
    if selected_id > 0:
        shipment = MerchantModel.objects.get(ship_id=selected_id)
    else:
        shipment = None
    if option == 1:
        company = "Arihaat Transports"
        wallet = CompanyAccounts.objects.get(company_name="Arihaat Transports").available_amt
        orders = MerchantModel.objects.filter(merchant="Arihaat Transports")
    else:
        company = "Vilosma Services"
        wallet = CompanyAccounts.objects.get(company_name="Vilosma Services").available_amt
        orders = MerchantModel.objects.filter(merchant="Vilosma Services")
    context = {
        "company" : company,
        "wallet" : wallet,
        "orders" : orders,
        "option" : option,
        "shipment" : shipment
    }
    return render(request, 'merchant_page.html', context)

def merchant_update(request, option, selected_id): #order_done merchant_done trasaction_done sendmail
    if request.method=="POST":
        status = request.POST.get("update_order")
        shipment = MerchantModel.objects.get(ship_id=selected_id)
        order = OrderModel.objects.get(order_id=shipment.order.order_id)
        if status == "1":
            new_status = "Preparing Shipment"
        elif status == "2":
            new_status = "InTransit"
            order.status = "Dispatched"
            order.save()
        elif status == "3":
            new_status = "Delivered"
            order.status = new_status
            order.save()

        shipment.status = new_status
        shipment.save()

        TransactionModel.objects.create(
            orders = order,
            user = order.user_id,
            action = new_status
        )
        
        subject = "Order Update!"
        context = {
            "customer_name" : order.user_id.username,
            "order_id" : order.order_id,
            "status" : new_status,
            'type' : "order_update"
        }
        message = render_to_string('purchase_mail.html', context)
        mail_id = order.user_id.email
        config_mail(subject, message, mail_id, html_message=message)

    return redirect('merchant_page', option=option, selected_id=selected_id)

def merchant_action(request, merch_id, order_id):
    date = dt.datetime.now()
    bmw = CompanyAccounts.objects.get(company_name="BMW")
    order = OrderModel.objects.get(order_id=order_id)
    if request.method == "POST":
        if merch_id == 1:
            merchant_name = "Arihaat Transports"
            company = CompanyAccounts.objects.get(company_name="Arihaat Transports")
            charge = 510
            company.available_amt = company.available_amt + charge
            company.save()
            bmw.available_amt = bmw.available_amt - charge
            bmw.save()
        else:
            merchant_name = "Vilosma Services"
            if request.POST.get("dispatch_option") == "1":
                company = CompanyAccounts.objects.get(company_name="Vilosma Services")
                charge = 440
                company.available_amt = company.available_amt + charge
                company.save()
                bmw.available_amt = bmw.available_amt - charge
                bmw.save()
            else:
                company = CompanyAccounts.objects.get(company_name="Vilosma Services")
                charge = 1280
                company.available_amt = company.available_amt + charge
                company.save()
                bmw.available_amt = bmw.available_amt - charge
                bmw.save()
        
        if request.POST.get("dispatch_option") == "1":
            service_type = "Domestic"
            est_del = date + dt.timedelta(days=5)
        else:
            service_type = "International"
            if merch_id == 1:
                est_del = date + dt.timedelta(days=12)
            else:
                est_del = date + dt.timedelta(days=8)

        MerchantModel.objects.create(
            merchant = merchant_name,
            order = order,
            type = service_type,
            status = "Confirmed",
            est_del = est_del,
            remarks = "En-Route"
        )
        order.status = "Dispatched"
        order.save()

        merchant_id = MerchantModel.objects.get(order=order)
        prev_block = BlockModel.objects.get(order=order)
        prev_block_hash = prev_block.hash

        hashed_order_id = generate_hash(merchant_id)
        BlockModel.objects.create(
            hash = hashed_order_id,
            previous_hash = prev_block_hash,
            order = order,
            sender = "Company",
            receiver = "Merchant",
            amount = float(charge)
        )

        TransactionModel.objects.create(
                orders = order,
                user = order.user_id,
                action = "Dispatched"
            )
        #mail
        return redirect('company_actions', option=5)