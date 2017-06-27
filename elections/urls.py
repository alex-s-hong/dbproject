# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^areas/(?P<area>[A-Za-z0-9]+)/$', views.areas), 
    url(r'^areas/(?P<area>[A-Za-z0-9]+)/results$', views.results), 
    url(r'^polls/(?P<poll_id>\d+)/$',views.polls),
    url(r'^create',views.create_user),
    
    
    url(r'^accounts/login', views.login),
    url(r'accounts/logout', views.logout),
    url(r'accounts/authenticate', views.authenticate),
    url(r'accounts/signup', views.signup),
    url(r'accounts/create', views.create),
]