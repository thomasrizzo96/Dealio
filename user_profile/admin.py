from django.contrib import admin
from user_profile.models import Promotion, Restaurant, Review
# Register your models here.


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['title']
    filter_horizontal = ('proms',)


class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']
    filter_horizontal = ('review',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author',)
    search_fields = ['author']


admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review, ReviewAdmin)
