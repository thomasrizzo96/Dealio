from django.shortcuts import render
from dealioApp.models import Restaurant
from dealioApp.models import Promotion
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from dealioApp.forms import addPromo
from django.views.generic.edit import CreateView, UpdateView
# Create your views here.


def index(request):
    return render(request, 'dealioApp/home.html') #render looks in templates directory


def restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'dealioApp/restaurants.html', {'restaurants': restaurants}) #render looks in templates directory #can pass in content into render() such as dictionaries


def promotions(request, restaurant_id):#pass in a restaurant's id into this view to access its promotions via getPromotions
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(request, 'dealioApp/promotions.html', {'restaurant': restaurant})

def ownerSignUp(request):
    return render(request, 'dealioApp/ownerSignUp.html')

class RestaurantCreate(CreateView):
    model = Restaurant
    fields = ['name', 'category', 'review_link']

class RestaurantUpdate(UpdateView):
    model = Restaurant
    fields = ['name', 'category', 'review_link']

def placefinder(request):
    return render(request, 'dealioApp/placefinder.html')

def add_promo(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = addPromo(request.POST)
        if form.is_valid():
            newPromo = form.save()
            restaurant.addPromo(newPromo)
        return HttpResponseRedirect('/promotions/' + restaurant_id)
    else:
        form = addPromo()
    return render(request, 'dealioApp/addPromo.html', {'form':form})

class delete_promo(DeleteView):
    model = Promotion
    success_url = reverse_lazy('restaurants')

def is_filtered(request,restaurant_id):
    """
    Display appropriate promotions.
    """
    restaurant = Restaurant.objects.get(id=restaurant_id)
    try:
        if request.POST["MostPopular"] is '1':
            restaurant.mostPop()
    except:
        restaurant.leastPop()

    return render(request, 'dealioApp/promotions.html', {'restaurant': restaurant})

def rest_filtered(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    return render(request, 'dealioApp/restaurants.html', {'restaurant': restaurant})

