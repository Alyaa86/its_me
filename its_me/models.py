from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	name = models.CharField(max_length=500)
	img = models.ImageField(null=True, blank=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	last_updated = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=500)
	img = models.ImageField(null=True, blank=True)
	content = models.TextField(blank=True)
	owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.title

class Follow(models.Model):
	user_from = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
	user_to = models.ForeignKey(User, related_name='followed_by',on_delete=models.CASCADE)
	# following= models.Bool

# User.add_to_class('following', models.ManyToManyField('self', through=Follow, related_name='followers',symmetrical=False))
