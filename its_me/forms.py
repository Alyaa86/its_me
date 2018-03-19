from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = "__all__" 
		exclude = ["owner"]


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = "__all__"
		exclude = ["post"]

class UserLoginForm(forms.Form):
	username= forms.CharField(required=True)
	password= forms.CharField(required=True, widget=forms.PasswordInput())

class UserSignupForm(forms.ModelForm):
	class Meta:
		model= User
		fields= ['username', 'first_name', 'last_name', 'email', 'password']

		widgets= {
			'password': forms.PasswordInput()
		}