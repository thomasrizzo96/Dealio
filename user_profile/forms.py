from django.forms import ModelForm
from user_profile.models import UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        fields = ['owner_id']
