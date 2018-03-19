from django.shortcuts import render, redirect
from .models import Profile, Post
from .forms import PostForm

# Create your views here.
def create_post(request, profile_id):
	profile_obj = Profile.objects.get(id=profile_id)
	form = PostForm()
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES or None)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.user = request.owner
			new_post.save()
			
			return redirect ('post_list')

	context= {
		'form':form,
		'profile':profile_obj
	}

	return render (request, 'create_post.html', context)

def posts_list(request,profile_id):
	profile_obj = Profile.objects.get(id=profile_id)
	posts = Post.objects.filter(owner=profile_obj) 
	context = {
		'posts':posts
	}

	return render (request, 'post_list.html', context)

def update_post(request, post_id, profile_id):
	profile_obj = Profile.objects.get(id=profile_id)
	posts = Post.objects.filter(owner=profile_obj)
	post_obj = posts.get(id=post_id)
	form = PostForm(instance=post_obj)
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES or None, instance= post_obj)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.user = request.profile_obj
			new_post.save()
			
			return redirect ('/post/list/<int:profile_id>/')

	context= {
		'form':form,
		'post_obj':post_obj,
		'profile_obj':profile_obj
	}

	return render (request, 'update_post.html', context)


def delete(request, post_id):
	Post.objects.get(id=post_id).delete()
	return redirect ('post_list')


