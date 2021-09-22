from django import forms
from .models import *
from django.contrib.auth.models import User
from datetime import datetime


class SignupForm(forms.Form):
	username=forms.EmailField(widget=forms.EmailInput())
	password=forms.CharField(widget=forms.PasswordInput())
	confirm_password=forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ['username','email','password','confirm_password']
	

class SendMailForm(forms.Form):
	recepient=forms.EmailField(widget=forms.EmailInput())
	subject=forms.CharField(widget=forms.TextInput())
	message=forms.CharField(widget=forms.Textarea())
class LoginForm(forms.Form):
	username=forms.EmailField(widget=forms.EmailInput())
	password=forms.CharField(widget=forms.PasswordInput())

class BlogCreateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields= ['name','image','address','contact']


class BlogUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields= ['name','image','address','contact']

class PasswordForgotForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter the email used in customer account..."
    }))

    def clean_email(self):
        e = self.cleaned_data.get("email")
        print(e)
        if Profile.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError(
                "Customer with this account does not exists..Plz enter valid email.")
        return e


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Enter New Password',
    }), label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Confirm New Password',
    }), label="Confirm New Password")

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Passwords did not match!")
        return confirm_new_password
