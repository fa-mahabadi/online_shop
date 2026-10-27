from .models import Order
from django import forms

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name' ,'last_name','email','address','postal_code','city']