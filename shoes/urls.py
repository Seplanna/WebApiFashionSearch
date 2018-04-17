"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from shoes import views

urlpatterns = [
    #url(r'^shoes/$', views.landing, name='shoes'),
    url(r'^task_description/(?P<user_id>\w+)/$', views.landing, name='shoes'),
    url(r'^shoes/(?P<task_id>\w+)/(?P<user_id>\w+)/$', views.product_description, name='product_description'),

]
