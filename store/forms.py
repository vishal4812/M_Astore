from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('s','Stripe'),
    ('p','Paypal')
)

class CheckoutForm(forms.Form):
    street_address=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 main st',
        'class': 'form-control' 
        
    }))
    apartment_address= forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'apartment of suite',
             'class': 'form-control'     
    }))
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    zip=forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'    
    }))
    same_shipping_addess=forms.BooleanField(required=False)
    save_info=forms.BooleanField(required=False)
    #payment_option=forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES)
