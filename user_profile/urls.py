from django.conf.urls import include, url
from . import views

# 3 url patterns for a profile page(not logged in), update profile, and profile page(logged in)
urlpatterns = [
   url(r'^profile/(?P<profile_id>\d+)/$', views.profile, name='profile'),
   url(r'^update_profile/$', views.update_profile, name='update_profile'),
   url(r'^your_profile/$', views.your_profile, name='your_profile'),
]
