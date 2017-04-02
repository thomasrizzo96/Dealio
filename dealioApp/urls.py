from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^restaurants$', views.restaurants, name='restaurants'),
    url(r'^promotions/(?P<restaurant_id>\d+)/$', views.promotions, name='promotions'),#this uses a named group for regex
    url(r'^addPromo/(?P<restaurant_id>\d+)/$', views.add_promo, name='addPromo'),
    url(r'^promotion_confirm_delete/(?P<pk>\d+)/$', views.delete_promo.as_view(), name='promotion-delete'),
    url(r'^restaurant/add/$', views.RestaurantCreate.as_view(), name='restaurant-add'),
    url(r'^restaurant/(?P<pk>\d+)/$', views.RestaurantUpdate.as_view(), name='restaurant-update'),
    url(r'^placefinder$', views.placefinder, name='placefinder'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
]
