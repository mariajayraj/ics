from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from .models import *

class CustomerForm(forms.ModelForm):
    CustomerId    = forms.IntegerField()
    CustomerName  = forms.CharField(max_length=10)

    class Meta:
        model = Customer
        fields = '__all__'

class AddDonorForm(forms.ModelForm):
    OrganizationName    = forms.CharField(max_length=100)
    Salutation          = forms.CharField(max_length=100)
    FirstName           = forms.CharField(max_length=100)
    LastName            = forms.CharField(max_length=100)
    Email               = forms.EmailField(max_length=100)
    PhoneNumber         = forms.CharField(max_length=15)
    Comments            = forms.CharField(max_length=100,required=False)
    StreetAddress       = forms.CharField(max_length=100)
    City                = forms.CharField(max_length=100)
    State               = forms.CharField(max_length=100)
    Zip                 = forms.CharField(max_length=100)
    ICS                 = forms.CharField(max_length=2,required=False)

    class Meta:
        model = Donors
        fields = '__all__'

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

class SearchDonorForm(forms.ModelForm):
    SearchQuery = forms.CharField(max_length=255)

    class Meta:
        model = SearchDonor
        fields = '__all__'

class FeedbackForm(forms.ModelForm):
    SearchQuery = forms.CharField(max_length=255)

    class Meta:
        model = SearchDonor
        fields = '__all__'

class AddInkindForm(forms.ModelForm):
    Donor          = forms.CharField(max_length=100)
    DonationDate   = forms.DateField()
    DonationAmount = forms.IntegerField()
    Description    = forms.CharField(max_length=100,required=False)
    
    class Meta:
        model = InKind
        fields = '__all__'
        
        
