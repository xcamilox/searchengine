from django.conf.urls import url

from . import  views


app_name = "Search"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('sourceList', views.sourceList, name='sourcelist'),
    url('sampList', views.sampList, name='samplist'),
    url('sampMessage', views.sampMessage, name='sampmessage'),
    url('observation', views.observationList, name='observationList'),
    url('sendSED', views.sampSEDMessage, name='sendsed'),
]