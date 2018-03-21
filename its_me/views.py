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
	posts = Post.objects.filter(owner=profile_obj) 
	context = {
		'posts':posts,
		'profile':profile_obj,
		'profile_id':profile_id
	}

	# return render (request, 'list.html', context)

	# detail= Profile.objects.get(id= profile_id)
	# context={
	# 	'profile_obj':profile_obj,
	# # 	'profile_id':profile_id
	# }
	return render(request, 'detail.html', context)


def signup_profile(request):
	form= UserSignupForm()
	if request.method=='POST':
		# # if user.exsist():
		# 	return redirect("login")
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
		form = ProfileForm(request.POST)
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
			return redirect('detail_profile',profile_id=profile_obj) 

	context={
		'form':form,
		'profile_obj':profile_obj
	}
	return render(request, 'update.html' , context)



def delete_profile(request, profile_id):
	Profile.objects.get(id=profile_id).delete()
	return redirect('/list/')

def create_post(request, profile_id):
	profile_obj = Profile.objects.get(id=profile_id)
	form = PostForm()
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES or None)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.owner = Profile.objects.get(owner=request.user)
			new_post.save()
			
			return redirect ('/list/')

	context= {
		'form':form,
		'profile':profile_obj
	}

	return render (request, 'create_post.html', context)

# def posts_list(request,profile_id):
# 	profile_obj = Profile.objects.get(id=profile_id)
# 	posts = Post.objects.filter(owner=profile_obj) 
# 	context = {
# 		'posts':posts
# 	}

# 	return render (request, 'list.html', context)

def update_post(request, post_id, profile_id):
	profile_obj = Profile.objects.get(id=profile_id)
	posts = Post.objects.filter(owner=profile_obj)
	post_obj = posts.get(id=post_id)
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
		'profile_obj':profile_obj
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

	#check if there is a follow_obj exsist


	return redirect('detail_profile',profile_id=profile_id)

def following_list(request, profile_id):
	profile = Profile.objects.get(id=profile_id)
	user = profile.owner
	print (profile)
	i_follow = user.following.all()
	# for following_obj in i_follow:
	# 	return following_obj.user_from.all()
	context={
		'following':i_follow,
		'profile_id':profile_id
	}
	return render(request, 'following.html', context)

def follower_list(request, profile_id):
	profile = Profile.objects.get(id=profile_id)
	user = profile.owner
	followers = user.followed_by.all()
	# for following_obj in i_follow:
	# 	return following_obj.user_from.all()
	context={
		'followers':followers,
		'profile_id':profile_id
	}
	return render(request, 'followers.html', context)

def feeds(request, profile_id):
	# profile = Profile.objects.get(id=profile_id)
	# user = profile.owner
	# i_follow = user.following.all()
	# print (i_follow)
	# feeds = Post.objects.filter(id__in=i_follow)

	following = request.user.following.all()
	list = []
	for i in following:
		list.append(i.user_to.profile_set.all()[0])

	feeds = Post.objects.filter(owner__in=list)


	# profile = Profile.objects.get(id=profile_id)
	# user = profile.owner
	# i_follow = user.following.all()
	# feeds = Post.objects.filter(i_follow)
	# # # we want to disply the feeds of ppl i follow 
	# # feeds= Post.i_follow.all()

	context={
		'feeds':feeds,
	}

	return render (request, 'feeds.html', context)



# def follow (request, profile_id):
# 	profile = Profile.objects.get(id=profile_id)
# 	user = profile.owner
# 	follow_obj, created=Follow.objects.get_or_create(user_from=request.user, user_to=user)
# 	if created:
# 		action="follow"
# 	else:
# 		action="unfollow"
# 		follow_obj.delete()

# 	#check if there is a follow_obj exsist


# 	return redirect('detail_profile',profile_id=profile_id)
	
#nbi nsawi list 
	# following_list = Follow.objects.filter(id)
	# follower_list = 
	


# def example(request, detail_id):
# 	# make request.user follow the other user
# 	follow.create()w what
# 	# after that is done, take them to list page
# 	return redirect("/list/")

# restaurant_obj = Restaurant.objects.get(id=x_id)
# 	favourite_obj, created = Favourite.objects.get_or_create(user=request.user, restaurant=restaurant_obj)
# 	if created:
# 		action="favourite"
# 	else:
# 		action="unfavourite"
# 		favourite_obj.delete()

# 	favourite_count= restaurant_obj.favourite_set.all().count()

# 	context = {
# 		'action':action,
# 		'count': favourite_count
# 	}
# 	return JsonResponse(context, safe=False)

# def log_out(request):
# 	logout(request)
# 	return redirect("login")


	# following = User.following.all()
	# following = User.following.filter(id=profile_id)
	# if request.method == 'POST':
	# 	follow =request.user.is_authenticate()
	# 	follow.save()
	# 	return redirct('/list/')
	# return redirct('login')









# Create your views here.
