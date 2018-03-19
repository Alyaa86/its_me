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

urlpatterns = [
    path('admin/',admin.site.urls),
    path('list/',views.list_profile ),
    path('detail/<int:profile_id>/', views.detail_profile, name='detail_profile'),
    path('signup/',views.signup_profile),
    path('create/',views.create_profile, name='create_profile'),
    path('login/',views.login_profile),
    path('logout/',views.logout_profile),
    path('delete/<int:profile_id>/',views.delete_profile),
    path('update/<int:profile_id>/',views.update_profile, name='update_profile'),  
]