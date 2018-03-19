from django import forms
from .models import Profile, Post

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ['owner']