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
from search import views

urlpatterns = [
    url(r'^search/(?P<game_id>\w+)/$', views.landing, name='landing'),
    url(r'^iterpretability/(?P<game_id>\w+)/$', views.InterpretabilityFunction, name='Interpretability'),
    url(r'^first_step/(?P<game_id>\w+)/$', views.FirstStepInGame, name='first_step'),
    url(r'^best_image/(?P<game_id>\w+)/$', views.ChoseTheBestPicture, name='best_image'),
    url(r'^finish/(?P<game_id>\w+)/$', views.Finish, name='Finish'),
    url(r'^will_you_buy/(?P<game_id>\w+)/(?P<product_id>\w+)/$', views.Will_you_buy, name='will_you_buy'),
    url(r'^start_session/(?P<user_id>\w+)/(?P<task_id>\w+)/$', views.SearchSessionStart, name='SearchSessionStart'),
    url(r'^description_best_image/(?P<game_id>\w+)/(?P<product_id>\w+)/$', views.Description, name='Description'),
    url(r'^search_session_end/(?P<game_id>\w+)/$', views.SearchSessionEnd, name='SearchSessionEnd'),
    url(r'^end_the_game/(?P<game_id>\w+)/$', views.EndGame, name='EndGame')


]
