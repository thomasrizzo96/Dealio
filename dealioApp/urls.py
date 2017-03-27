from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^restaurants$', views.restaurants, name='restaurants'),
    url(r'^promotions/(?P<restaurant_id>\d+)/$', views.promotions, name='promotions'),#this uses a named group for regex
    url(r'^addPromo/(?P<restaurant_id>\d+)/$', views.add_promo, name='addPromo'),
    url(r'^promotion_confirm_delete/(?P<pk>\d+)/$', views.delete_promo.as_view(), name='promotion-delete'),
    url(r'^restaurant/add/$', views.RestaurantCreate.as_view(), name='restaurant-add'),
    url(r'^restaurant/(?P<pk>\d+)/$', views.RestaurantUpdate.as_view(), name='restaurant-update'),
    url(r'^ownerSignUp$', views.ownerSignUp, name ='ownerSignUp'),
    url(r'^ownerLogin$', auth_views.login, {'template_name': 'dealioApp\ownerLogin.html'}, name ='ownerLogin'),
    url(r'^ownerLogout/$', auth_views.logout, {'template_name': 'dealioApp\ownerLogout.html', 'next_page': '/'}, name='logout'),
    url(r'^placefinder$', views.placefinder, name='placefinder'),
    url(r'^promo_filtered/(?P<restaurant_id>\d+)/$', views.is_filtered, name='promo_filtered'),
    url(r'^rest_filtered/(?P<restaurant_id>\d+)/$', views.rest_filtered, name='rest_filtered'),
]
