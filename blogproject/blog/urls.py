"""
URL configuration for blogproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from .views import *


urlpatterns = [
    path('<pk>/showreply', showreply, name='showreply'),
    path('<pk>/showlikesrep', showlikerep, name='showlikerep'),
    path('<pk>/showlikescomm', showlikecomm, name='showlikecomm'),
    path('<pk>/showcomments', showcomms, name='showcomm'),
    path('<pk>/likespost', showlike, name='showlikes'),
    path('<pk>/blog', showaboutpost, name='showblog'),
    path('removelike', removelike, name='removelikeonblog'),
    path('addlike', addlike, name='addlikeonblog'),
    path('<pk>/profile', showprofile, name='profile'),
    path('<int:pk>/update', Updatepost, name='updatepost'),
    path('<int:pk>/delete', DeletePost.as_view(), name='deletepost'),
    path('', Main, name='mainpage'),
    path('Registration', Register.as_view(), name='register'),
    path('Createpost', creatingpost, name='createpost'),
    path('Login', loginin, name='login'),
    path('Logout', log_out, name='logout'),
    path('addcomment', Create_comment, name='createcomment'),
]
