from django import forms
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(forms.Form):

	username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'w3-input w3-light-grey w3-round','style':"margin-bottom: 8px; border: 0px #FAFAFA", 'name': 'name','required':'yes','placeholder':'Your Name'}))
	email=forms.CharField(max_length=100,widget=forms.EmailInput(attrs={'class': 'w3-input w3-light-grey w3-roundl', 'style':"margin-bottom: 8px; border: 0px #FAFAFA",'name': 'email','required':'yes','placeholder':'Enter Your Unique Email'}))
	password = forms.CharField(max_length=75,widget=forms.PasswordInput(attrs={'class': 'w3-input w3-light-grey w3-round ', 'style':"margin-bottom: 8px; border: 0px #FAFAFA",'name': 'email', 'required': 'yes','placeholder': 'Your Password'}))
	confirm_password = forms.CharField(max_length=75,widget=forms.PasswordInput(attrs={'class': 'w3-input w3-light-grey w3-round', 'style':"margin-bottom: 8px; border: 0px #FAFAFA",'name': 'email', 'required': 'yes','placeholder': 'Repeat Your Password'}))

class LoginForm(forms.Form):
	email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class': 'w3-input w3-light-grey w3-round', 'style':"margin-bottom: 8px; border: 0px #FAFAFA",'name': 'name', 'required': 'yes', 'placeholder': 'Enter Your Unique Email'}))
	password = forms.CharField(max_length=75, widget=forms.PasswordInput(attrs={'class': 'w3-input w3-light-grey w3-round ', 'style':"margin-bottom: 8px; border: 0px #FAFAFA", 'name': 'email', 'required': 'yes', 'placeholder': 'Your Password'}))