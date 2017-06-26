# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^areas/(?P<area>[a-z]+)/$', views.areas), 
    url(r'^areas/(?P<area>[a-z]+)/results$', views.results), 
    url(r'^polls/(?P<poll_id>\d+)/$', views.polls),
    url(r'^create',views.create_user)
]