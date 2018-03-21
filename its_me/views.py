from django.shortcuts import render, redirect
from .models import Profile, Post
from django.contrib.auth import authenticate
from django.contrib.auth import login 
from django.contrib.auth import logout
from .forms import ProfileForm, PostForm, UserLoginForm, UserSignupForm
# Create your views here.


def list_profile(request):
	profile= Profile.objects.all()
		# if Profile.objects.img.is_valid():
		# 	img_profile= img.save(commit=True)
		# 	img_profile.save()
		# return redirect('detail_profile')

	profile= profile.order_by('name')
	query= request.GET.get('q')
	if query:
		profile= profile.filter(name__contains='name')
	context={
		'list':profile
	}

	return render(request, 'list.html', context)


def detail_profile(request, profile_id):
	detail= Profile.objects.get(id= profile_id)
	posts= Post.objects.filter(owner=detail)
	context={
		'detail':detail,
		'profile_id':profile_id,
		'posts':posts
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
	if not request.user.is_authenticated:
		return redirect(login)
	form = ProfileForm()
	if request.method == 'POST':
		form = ProfileForm(request.POST)
		if form.is_valid():
			form.save()
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
			return redirect('/list/') 

	context={
		'form':form,
		'profile_obj':profile_obj
	}
	return render(request, 'update.html' , context)



def delete_profile(request, profile_id):
	Profile.objects.get(id=profile_id).delete()
	return redirect('/list/')

def create_post(request, profile_id):
	if not request.user.is_authenticated:
		return redirect(login)
	profile_obj = Profile.objects.get(id=profile_id)
	form = PostForm()
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES or None)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.user = profile_obj
			new_post.save()
			
			return redirect ('/list/')

	context= {
		'form':form,
		'profile':profile_obj
	}

	return render (request, 'create_post.html', context)

def posts_list(request,profile_id):
	if not request.user.is_authenticated:
		return redirect(login)
	profile_obj = Profile.objects.get(id=profile_id)
	posts = Post.objects.filter(owner=profile_obj) 
	context = {
		'posts':posts
	}

	return render (request, 'list.html', context)

def update_post(request, post_id, profile_id):
	profile_obj = Profile.objects.get(id=profile_id)
	posts = Post.objects.filter(owner=profile_obj)
	post_obj = posts.get(id=post_id)
	form = PostForm(instance=post_obj)
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES or None, instance= post_obj)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.profile_obj= request.User
			new_post.save()
			
			return redirect ('/list/')

	context= {
		'form':form,
		'post_obj':post_obj,
		'profile_obj':profile_obj
	}

	return render (request, 'update_post.html', context)


def delete(request, post_id):
	Post.objects.get(id=post_id).delete()
	return redirect ('/list/')


