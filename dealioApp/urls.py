from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^restaurants$', views.restaurants, name='restaurants'),
    url(r'^promotions/(?P<restaurant_id>\d+)/$', views.promotions, name='promotions'),#this uses a named group for regex
    url(r'^addPromo/(?P<restaurant_id>\d+)/$', views.add_promo, name='addPromo'),
    url(r'^share_promo/(?P<promo_id>\d+)/$', views.share_promo, name='share_promo'),
    url(r'^promotion_confirm_delete/(?P<restaurant_id>\d+)/(?P<promo_id>\d+)/$', views.delete_promo, name='promotion-delete'),
    url(r'^restaurant/add/$', views.RestaurantCreate.as_view(), name='restaurant-add'),
    url(r'^restaurant/(?P<pk>\d+)/$', views.RestaurantUpdate.as_view(), name='restaurant-update'),
    url(r'^placefinder$', views.placefinder, name='placefinder'),
    url(r'^promo_filtered/(?P<restaurant_id>\d+)/$', views.is_filtered, name='promo_filtered'),
    url(r'^rest_filtered$', views.rest_filtered, name='rest_filtered'),
    url(r'^reset_filtered/$', views.reset_filtered, name='reset_filtered'),
    url(r'^reset_promo_filtered/(?P<restaurant_id>\d+)/$', views.reset_promo_filtered, name='reset_promo_filtered'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^promotion_review/(?P<promo_id>\d+)/$', views.new_review, name='promotion-review'),
    url(r'^promotion_reviewList/(?P<promo_id>\d+)/$', views.display_reviews, name='promotion-reviewList'),
]
