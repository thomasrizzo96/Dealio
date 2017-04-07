from django.forms import ModelForm
from dealioApp.models import Promotion, Review

class addPromo(ModelForm):
    class Meta:
        model = Promotion
        fields = ['title', 'description', 'rating']

class addReview(ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'description', 'rating']