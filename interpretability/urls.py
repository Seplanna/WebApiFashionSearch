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
from interpretability import views

urlpatterns = [
    url(r'^login_Interpretability/(?P<signal>\w+)/$', views.loginInterpretability, name='login'),
    url(r'^create_account_Interpretability/(?P<signal>\w+)/$', views.CreateAccountInterpretability, name='login'),
    url(r'^landing_Interpretability/(?P<form_id>\w+)/$', views.landingInterpretability, name='landing'),
    url(r'^interpretability_task/(?P<game_id>\w+)/$', views.InterpretabilityFunction, name='Interpretability'),
    url(r'^start_interpretability_task/(?P<user_id>\w+)/$', views.StartInterpretabilityTask, name='StartInterpretability'),
    url(r'^end_interpretability_task/(?P<game_id>\w+)/$', views.EndInterpretabilityTask, name='EndInterpretability')
]
