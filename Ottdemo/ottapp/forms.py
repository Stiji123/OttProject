# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.html import format_html

from .models import Customer, UserProfile, KidsProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'email', 'username', 'password', 'DoB', 'phonenumber']
        widgets = {
            'password': forms.PasswordInput(),
            'DoB': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')
        # Add custom validation for phone number if needed
        return phonenumber


class VerifyPinForm(forms.Form):
    pin = forms.CharField(widget=forms.PasswordInput(attrs={'maxlength': 6}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'image', 'pin']


# forms.py
class KidProfileForm(forms.ModelForm):
    class Meta:
        model = KidsProfile
        fields = ['name', 'image']


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100,required=False)
