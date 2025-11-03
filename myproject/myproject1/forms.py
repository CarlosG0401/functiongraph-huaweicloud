from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'  

        labels = {
            'oid': 'Order ID',
            'fname': 'First Name',
            'lname': 'Last Name',
            'price': 'Price',
            'mail': 'Email Address',
            'addr': 'Address',
        }

        widgets = {
            'oid': forms.NumberInput(attrs={'placeholder': 'Enter Order ID'}),
            'fname': forms.TextInput(attrs={'placeholder': 'Enter First Name'}),
            'lname': forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter Price'}),
            'mail': forms.EmailInput(attrs={'placeholder': 'Enter Email Address'}),
            'addr': forms.TextInput(attrs={'placeholder': 'Enter Address'}),
        }
        


