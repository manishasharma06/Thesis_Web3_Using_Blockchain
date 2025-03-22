from django import forms
from .models import *

class CarWarehouseForm(forms.ModelForm):
    class Meta:
        model = CarWarehouseModel
        fields = ['model', 'year', 'type', 'price', 'fuel_type', 'transmission', 'stock']

        widgets = {
            'year' : forms.Select(choices=[(year, year) for year in range(1950, 2100)], attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        country = CountryField(blank_label="(select country)")
        fields = ['username', 'address', 'city', 'state', 'country', 'phone_num', 'email', 'wallet_amt']

class Mercedes_OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['car_id', 'user_id', 'status']