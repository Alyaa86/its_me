from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
 	name= models.CharField(max_length= 500)
 	img_profile= models.ImageField(null=True, blank=True)
 	owner= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
 	posts= models.TextField()
 	last_updated= models.DateTimeField(auto_now=True)

 	def __str__(self):
 		return self.name

class Post(models.Model):
	title= models.CharField(max_length= 500)
	img_post= models.ImageField(null=True, blank=True)
	content= models.TextField(blank=True)
	owner= models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

	def __str__(self):
 		return self.title
