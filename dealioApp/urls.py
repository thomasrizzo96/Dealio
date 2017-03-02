from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^restaurants$', views.restaurants, name='restaurants'),
    url(r'^promotions/(?P<restaurant_id>\d+)/$', views.promotions, name='promotions'),#this uses a named group for regex

]
