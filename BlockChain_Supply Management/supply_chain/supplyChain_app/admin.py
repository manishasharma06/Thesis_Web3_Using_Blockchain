from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CompanyAccounts)
admin.site.register(CarWarehouseModel)
admin.site.register(UserModel)
admin.site.register(OrderModel)
admin.site.register(TransactionModel)
admin.site.register(RequestModel)
admin.site.register(RefundModel)
admin.site.register(SentMailModel)
admin.site.register(MerchantModel)
admin.site.register(BlockModel)