from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^areas/?P<area>.+)/$',views.areas)
    url(r'^polls/(?<poll_id>\d+)/$)',views.polls)
]
