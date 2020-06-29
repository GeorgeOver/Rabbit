"""firelog URL Configuration

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

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.sign_in, name='sign_in'),
    path('dashboard/', views.post_sign, name='post_sign'),
    path('logout/', views.logout, name='logout'),
    path('manage/', views.manage, name='manage'),
    path('change_status/', views.change_status, name='change_status'),
    path('change_callback/', views.change_callback, name='change_callback'),
    path('delete_order/', views.delete_order, name='delete_order'),
    path('delete_callback/', views.delete_callback, name='delete_callback'),
    path('post_change_status/', views.post_change_status, name='post_change_status'),
    path('post_change_callback/', views.post_change_callback, name='post_change_callback'),
    path('change_position/', views.change_position, name='change_position'),
    path('delete_position/', views.delete_position, name='delete_position'),
    path('post_change_position/', views.post_change_position, name='post_change_position'),
]
