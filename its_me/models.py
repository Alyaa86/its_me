from django.db import models
from django.contrib.auth.models import User


brain_test = (
    ('L','mostly left'),
    ('R','mostly right'),
    ('R&L','both equal'),
)

class Profile(models.Model):
	name = models.CharField(max_length=500)
	DOB= models.DateField(null=True)
	img = models.ImageField(null=True, blank=True)
	brain_test= models.CharField(max_length=500, choices=brain_test)	
	owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	last_updated = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=500)
	img = models.ImageField(null=True, blank=True)
	content = models.TextField(blank=True)
	owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	last_updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

class Follow(models.Model):
	user_from = models.ForeignKey(User, related_name='rel_following', on_delete=models.CASCADE)
	user_to = models.ForeignKey(User, related_name='rel_followed_by',on_delete=models.CASCADE)

	def __str__(self):
		return "{} is following {}".format(self.user_from, self.user_to)
	# following= models.Bool

# User.add_to_class('following', models.ManyToManyField('self', through=Follow, related_name='followers',symmetrical=False))

# those you follow = request.user.following.all()
# list = those you follow

