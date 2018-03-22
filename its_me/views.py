from django.shortcuts import render, redirect
from .models import Profile, Post, Follow
from django.contrib.auth import authenticate
from django.contrib.auth import login 
from django.contrib.auth import logout
from .forms import ProfileForm, PostForm, UserLoginForm, UserSignupForm
from django.contrib.auth.models import User
# Create your views here.


def list_profile(request):
	list= Profile.objects.all()
	context={
		'list':list
	}

	return render(request, 'list.html', context)


def detail_profile(request, profile_id):
	profile_obj = Profile.objects.get(id=profile_id)
	posts = Post.objects.filter(owner=profile_id) 
	context = {
		'posts':posts,
		'profile':profile_obj,
		'profile_id':profile_id
	}
	return render(request, 'detail.html', context)


def signup_profile(request):
	form= UserSignupForm()
	if request.method=='POST':
		form= UserSignupForm(request.POST)
		if form.is_valid():
			user= form.save(commit=False)
			user.set_password(user.password)
			user.save()
			login(request, user)
			return redirect('create_profile')

	context={
		'signup':form 
	}
	return render (request,'signup.html' ,context)



def create_profile(request):
	form = ProfileForm()
	if request.method == 'POST':
		form = ProfileForm(request.POST ,request.FILES or None)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.owner = request.user
			profile.save()
			return redirect('/list/')
	context={
		'form':form
	}
	return render(request, 'new.html', context)
	
	


def login_profile(request):
	form= UserLoginForm()
	if request.method== 'POST':
		form= UserLoginForm(request.POST)	
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('/list/')

	context={
		'form':form
	}
	
	return render(request, 'login.html', context)


def logout_profile(request):
	logout(request)
	return redirect("/list/")

def update_profile(request , profile_id):
	profile_obj = Profile.objects.get(id=profile_id)
	form = ProfileForm(instance= profile_obj)
	if request.method =='POST':
		form=ProfileForm(request.POST, request.FILES or None, instance=profile_obj)
		if form.is_valid():
			form.save()
			return redirect('detail_profile',profile_id=profile_id) 

	context={
		'form':form,
		'profile_obj':profile_obj
	}
	return render(request, 'update.html' , context)



def delete_profile(request, profile_id):
	Profile.objects.get(id=profile_id).delete()
	return redirect('/list/')

def create_post(request):
	form = PostForm()
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES or None)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.owner = request.user
			new_post.save()
			
			return redirect ('/list/')

	context= {
		'form':form,
	}

	return render (request, 'create_post.html', context)

def posts_list(request,profile_id):
	profile_obj = Profile.objects.get(id=profile_id)
	posts = Post.objects.filter(owner=profile_id) 
	context = {
		'posts':posts
	}

	return render (request, 'posts_list.html', context)

def update_post(request, post_id):
	post_obj = Post.objects.get(id=post_id)
	form = PostForm(instance=post_obj)
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES or None, instance= post_obj)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.profile_obj = request.user
			new_post.save()
			
			return redirect ('/list/')

	context= {
		'form':form,
		'post_obj':post_obj,
	}

	return render (request, 'update_post.html', context)


def delete(request, post_id):
	Post.objects.get(id=post_id).delete()
	return redirect ('/list/')

def follow (request, profile_id):
	profile = Profile.objects.get(id=profile_id)
	user = profile.owner
	follow_obj, created=Follow.objects.get_or_create(user_from=request.user, user_to=user)
	if created:
		action="follow"
	else:
		action="unfollow"
		follow_obj.delete()

		context={
			'action':action
		}

	return redirect('detail_profile',profile_id=profile_id)

def following_list(request, user_id):
	user = User.objects.get(id=user_id)
	following = user.rel_following.all()
	following_list = []
	for i in following:
		following_list.append(i.user_to)
	
	context={
		'following':following
	}
	return render(request, 'following.html', context)
	

def follower_list(request, user_id):
	user = User.objects.get(id=user_id)
	followers = request.user.rel_following.all()
	follower_list = []
	for i in followers:
		follower_list.append(i.user_from)
	context={
		'followers':followers,
	}
	return render(request, 'followers.html', context)

def feeds(request):
	following = request.user.rel_following.all()
	following_list = []
	for i in following:
		following_list.append(i.user_to)

	feeds = Post.objects.filter(owner__in=following_list)
	context={
		'feeds':feeds,
	}

	return render (request, 'feeds.html', context)
