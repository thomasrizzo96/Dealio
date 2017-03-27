from django.forms import ModelForm
from dealioApp.models import Promotion

class addPromo(ModelForm):
    class Meta:
        model = Promotion
        fields = ['title', 'description', 'rating']

