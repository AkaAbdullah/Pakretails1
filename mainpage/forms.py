from django.forms import fields
from mainpage import models
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from .models import Customer
from .models import Feedback
from .models import OrderPlaced

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['password1'].widget.attrs['class'] = 'input'
        self.fields['password2'].widget.attrs['class'] = 'input'

class myLoginForm(AuthenticationForm):
    class Meta:
        model=User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(myLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['password'].widget.attrs['class'] = 'input'

class myPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model=User
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(myPasswordChangeForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['class'] = 'input'
        self.fields['new_password1'].widget.attrs['class'] = 'input'
        self.fields['new_password2'].widget.attrs['class'] = 'input'

class AddressForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields=['fullname','city','state','address','email','phone_no']
        widgets={
		'fullname':forms.TextInput(attrs={'class':'input'}),
		'city':forms.TextInput(attrs={'class':'input'}),
		'state':forms.Select(attrs={'class':'input'}),
		'address':forms.TextInput(attrs={'class':'textarea'}),
		'email':forms.EmailInput(attrs={'class':'input'}),
		'phone_no':forms.NumberInput(attrs={'class':'input'})
		}

class FeedBackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets={
		'message':forms.TextInput(attrs={'class':'textarea'}),
		}

class OrderPlacedForm(forms.ModelForm):
    class Meta:
        model = OrderPlaced
        fields = ['paymentmethod']
        widgets={
		'paymentmethod':forms.Select(attrs={'class':'input'}),
		}