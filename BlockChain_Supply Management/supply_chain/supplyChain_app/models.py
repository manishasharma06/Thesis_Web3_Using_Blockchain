from django.db import models
from django_countries.fields import CountryField
from random import randint

# Create your models here.
class CompanyAccounts(models.Model):
    company_name = models.CharField(max_length=20)
    available_amt = models.FloatField()
    
    def __str__(self):
        return f"{self.company_name} -- {self.available_amt}"

class CarWarehouseModel(models.Model):
    car_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=40)
    TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Coupe', 'Coupe'),
        ('Hatchback', 'Hatchback'),
    ]
    type = models.CharField(max_length=20, choices=TYPES)
    year = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    FUEL_TYPES = [
        ('Gasoline', 'Gasoline'),
        ('Diseal', 'Diseal'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]
    fuel_type = models.CharField(max_length=100, choices=FUEL_TYPES)
    TRANSMISSION_TYPES = [
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
        
    ]
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_TYPES)
    AVAILABILITY = [
        ('In stock', 'In Stock'),
        ('Out Of Stock', 'Out Of Stock'),
    ]
    stock = models.CharField(max_length=20, choices=AVAILABILITY)

    def __str__(self):
        return f"{self.car_id} -- {self.model}"
    
#------------------/ User Info /-----------------

class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=200, null=True, choices=CountryField().choices + [('', 'Select Country')])
    phone_num = models.PositiveIntegerField()
    email = models.EmailField()
    wallet_amt = models.IntegerField()

    def __str__(self):
        return f"{self.user_id} - {self.username}"

#------------------/ Order request logs /-----------------

class OrderModel(models.Model):
    order_id = models.AutoField(primary_key=True)
    car_id = models.ForeignKey(CarWarehouseModel, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    order_amt = models.PositiveIntegerField()
    STATUS = [
        ('Confirming', 'Confirming'),
        ('At Assembly', 'At Assembly'),
        ('Ready to Dispatch', 'Ready to Dispatch'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=40, choices=STATUS)
    dt = models.DateTimeField()
    est_del = models.DateField()

    def __str__(self):
        return f"{self.order_id} - {self.user_id.username}"
    
class MerchantModel(models.Model):
    merchant = models.CharField(max_length=20)
    ship_id = models.AutoField(primary_key=True, unique=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    order_date = models.DateTimeField(auto_now_add=True)
    est_del = models.DateField()
    remarks = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.ship_id} - {self.order.user_id.username}"

#------------------/ Transaction logs(mercedes) /-----------------
    
class TransactionModel(models.Model):
    transaction_id = models.PositiveIntegerField(primary_key=True, unique=True)
    orders = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.transaction_id:
            existing_ids = TransactionModel.objects.values_list('transaction_id', flat=True)
            while True:
                new_id = randint(10000000, 99999999)
                if new_id not in existing_ids:
                    self.transaction_id = new_id
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_id} - {self.orders.order_id} - {self.action}"


class RequestModel(models.Model):
    request_id = models.PositiveIntegerField(primary_key=True, unique=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    client_reason = models.CharField(max_length=150)
    company_reason = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.request_id:
            existing_requests = RequestModel.objects.values_list('request_id', flat=True)
            while True:
                new_request = randint(10000000, 99999999)
                if new_request not in existing_requests:
                    self.request_id = new_request
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request_id} - {self.order.order_id} - {self.type}"
    
class RefundModel(models.Model):
    refund_id = models.PositiveIntegerField(primary_key=True, unique=True)
    request = models.ForeignKey(RequestModel, on_delete=models.CASCADE)
    refund_amt = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.refund_id:
            existing_refunds = RefundModel.objects.values_list('refund_id', flat=True)
            while True:
                new_refund = randint(10000000, 99999999)
                if new_refund not in existing_refunds:
                    self.refund_id = new_refund
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.refund_id} - {self.request.order.order_id} - {self.request.order.user_id.username}"
    
class SentMailModel(models.Model):
    mail_id = models.AutoField(primary_key=True, unique=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=75)
    body = models.CharField(max_length=5000)
    sent_at = models.DateTimeField(auto_now_add=True)

    
    def save(self, *args, **kwargs):
        if not self.mail_id:
            existing_mails = SentMailModel.objects.values_list('mail_id', flat=True)
            while True:
                new_ids = randint(10000000, 99999999)
                if new_ids not in existing_mails:
                    self.mail_id = new_ids
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order.user_id.username} - {self.subject}"
    
class BlockModel(models.Model):
    hash = models.CharField(max_length=255)
    previous_hash = models.CharField(max_length=255, null=True, blank=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    sender = models.CharField(max_length=20)
    receiver = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hash: {self.hash}, Sender: {self.sender}, Receiver: {self.receiver}"