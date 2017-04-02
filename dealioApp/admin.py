from django.contrib import admin
from dealioApp.models import Promotion, Restaurant
# Register your models here.


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['title']
    filter_horizontal = ('proms',)

class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']


admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
