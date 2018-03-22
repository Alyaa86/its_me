"""AR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from its_me import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',admin.site.urls),
    path('list/',views.list_profile, name='profile_list'),
    path('detail/<int:profile_id>/', views.detail_profile, name='detail_profile'),
    path('signup/',views.signup_profile, name='register'),
    path('create/',views.create_profile, name='create_profile'),
    path('login/',views.login_profile, name='login'),
    path('logout/',views.logout_profile),
    path('delete/<int:profile_id>/',views.delete_profile, name='profile_delete'),
    path('update/<int:profile_id>/',views.update_profile, name='update_profile'),  
    path('post/create/',views.create_post, name ='create_post'),
    path('post/update/<int:post_id>',views.update_post, name ='update_post'),
    path('post/delete/<int:post_id>',views.delete, name='delete_post'),
    path('follow/<int:profile_id>',views.follow, name ='follow'),
    path('following/<int:user_id>', views.following_list, name ='following'),
    path('followers/<int:user_id>',views.follower_list, name ='followers'),
    path('feeds/',views.feeds, name ='feeds'),
    path('post/list/<int:profile_id>',views.posts_list, name ='posts_list'),


]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

