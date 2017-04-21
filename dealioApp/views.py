from django.shortcuts import render
from dealioApp.models import Restaurant
from dealioApp.models import Promotion
from dealioApp.models import Review
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from dealioApp.forms import addPromo, addReview
from django.views.generic.edit import CreateView, UpdateView
# Create your views here.


def index(request):
    return render(request, 'dealioApp/home.html') #render looks in templates directory

def about(request):
    return render(request, 'dealioApp/about.html')

def restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'dealioApp/restaurants.html', {'restaurants': restaurants}) #render looks in templates directory #can pass in content into render() such as dictionaries


def promotions(request, restaurant_id):#pass in a restaurant's id into this view to access its promotions via getPromotions
    restaurant = Restaurant.objects.get(id = restaurant_id)
    restaurant.fillPromoList()
    return render(request, 'dealioApp/promotions.html', {'restaurant': restaurant})


def ownerSignUp(request):
    return render(request, 'dealioApp/ownerSignUp.html')


class RestaurantCreate(CreateView):
    model = Restaurant
    fields = ['owner_number','name','description','phone_number','email_address','website','picture', 'category','rating','yelp']


class RestaurantUpdate(UpdateView):
    model = Restaurant
    fields = ['owner_number', 'name', 'description', 'phone_number', 'email_address', 'website', 'picture', 'category','rating', 'yelp']


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
    return render(request, 'dealioApp/addPromo.html', {'form': form})


class delete_promo(DeleteView):
    model = Promotion
    success_url = reverse_lazy('restaurants')

# Display appropriate Promotions
def is_filtered(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    try:
        if request.POST["filter"] is "1":
            restaurant.mostPop()
        else:
            restaurant.leastPop()
    except:
        return render(request, 'dealioApp/promotions.html', {'restaurant': restaurant})

    return render(request, 'dealioApp/promotions.html', {'restaurant': restaurant})


# Restaurant filtering
def rest_filtered(request):
    restaurantList = Restaurant.objects.all()
    try:
        catList = request.POST.getlist('resFilter[]')
        for rest in restaurantList:
            if rest.category in catList:
                rest.set_filter_status(True)
            else:
                rest.set_filter_status(False)
    except:
        return render(request, 'dealioApp/restaurants.html', {'restaurants': restaurantList})
    return render(request, 'dealioApp/restaurants.html', {'restaurants': restaurantList})


# resets all previous restaurant filters by setting each restaurants filtering option to true
def reset_filtered(request):
    restaurantList = Restaurant.objects.all()
    try:
        for rest in restaurantList:
            rest.set_filter_status(True)
    except:
        return render(request, 'dealioApp/restaurants.html', {'restaurants': restaurantList})
    render(request, 'dealioApp/restaurants.html', {'restaurants': restaurantList})
    return HttpResponseRedirect('/restaurants')


# resets all promotional filters
def reset_promo_filtered(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    try:
       restaurant.fillPromoList()
    except:
        return render(request, 'dealioApp/promotions.html', {'restaurant': restaurant})

    return render(request, 'dealioApp/promotions.html', {'restaurant': restaurant})

# add new review to promotion
def new_review(request, promo_id):
    promo = Promotion.objects.get(id=promo_id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = addReview(request.POST)
        if form.is_valid():
            newRev = form.save()
            promo.addReview(newRev)
        return HttpResponseRedirect('/promotions/' + promo_id)
    else:
        form = addReview()
    return render(request, 'dealioApp/addReview.html', {'form': form})

#displays review
def display_reviews(request, promo_id):
    promo = Promotion.objects.get(id=promo_id)
    return render(request, 'dealioApp/reviews.html', {'promotion': promo})


