from django.db import models
from django.contrib.auth.models import User
from dealioApp.models import *

# Create your models here.

# User profile that extends the base user
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    restaurants = models.ManyToManyField(Restaurant)
    owner_id = models.CharField(max_length=25, unique=True)

    # weird workaround to fix the "doesn't declare an explicit app_label" error
    class Meta:
        app_label = 'app_model_belongs_to'

    def __str__(self):
        return self.owner_id

    def __unicode__(self):
        return self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver

# a signal that creates a user profile whenever a user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance)
