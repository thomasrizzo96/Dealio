from django.shortcuts import render
from dealioApp.models import Restaurant
from dealioApp.models import Promotion
from dealioApp.models import Review
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from dealioApp.forms import addPromo, addReview
from django.views.generic.edit import CreateView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from dealioApp.email_text import send_promo_email, send_promo_text
from django.http import StreamingHttpResponse
from dealioApp.google_scripts import *
from itertools import chain

import logging
log = logging.getLogger(__name__)

# Create your views here.

def index(request):
    if request.method == 'POST':
        location = request.POST['location'] #this is a string with the lat and lon seperated by a space. call print(location) if you would like to test.
        print("The location is: " + location)
        return HttpResponseRedirect('restaurants')

    return render(request, 'dealioApp/home.html')

def about(request):
    return render(request, 'dealioApp/about.html')
@csrf_exempt
def restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'dealioApp/restaurants.html', {'restaurants': restaurants}) #render looks in templates directory #can pass in content into render() such as dictionaries


def promotions(request, restaurant_id):#pass in a restaurant's id into this view to access its promotions via getPromotions
    restaurant = Restaurant.objects.get(id = restaurant_id)
    restaurant.fillPromoList()
    return render(request, 'dealioApp/promotions.html', {'restaurant': restaurant})



@csrf_exempt
def compute_restaurants(request):
    restaurants = list()

    #print(result_list)
    try:
        location = request.POST['apiCoords']
        lat,lng = location.split(",")
        p_locationLat = lat
        p_locationLong = lng
        p_radius = 5
        p_searchType = 'restaurant'
        p_searchKeyWord = ""
        p_numResults = 25
        #log.error(lat)
        #log.error(lng)
        results = retrieve_results(p_locationLat, p_locationLong, p_radius, p_searchType, p_searchKeyWord, p_numResults)

        #log.error(results)
        #log.error("lat,lng = " + lat + "," + lng)
        #result_list = Restaurant.objects.raw("SELECT * FROM 'dealioApp_restaurant' LIMIT 1")
        #result_list = list(Restaurant.objects.raw("SELECT * FROM 'dealioApp_restaurant'WHERE google_id='6aa990172a4a68cf8682a70a3c2a9077f11e435b' LIMIT 1"))
        #log.error(str(result_list))

        #intoparam = "SELECT * FROM 'dealioApp_restaurant'WHERE google_id='d08ba7f48795e44a825b8e8a54d04756468ab997' LIMIT 1"
        #log.error(intoparam)
        #result_list += list(Restaurant.objects.raw(intoparam))
        #log.error("Result list is: ")
        #lolol = Restaurant.objects.raw("SELECT * FROM 'dealioApp_restaurant' LIMIT 15") #this one works!
        #result_list = list(Restaurant.objects.raw("SELECT * FROM dealioApp_restaurant WHERE google_id='ae301c5ce88c4cb7d064ebdf54d47d5b0935d455' LIMIT 1"))
        result_list = list()
        #log.error(type(result_list))
        #result_list = (Restaurant.objects.raw("SELECT * FROM 'dealioApp_restaurant'WHERE google_id='6aa990172a4a68cf8682a70a3c2a9077f11e435b' LIMIT 1")

        for key, value in results.items():
            try:
                currQuery = Restaurant.objects.raw("""SELECT google_id FROM 'dealioApp_restaurant' WHERE google_id='""" + value + """' LIMIT 1""")
                if len(str(currQuery)) == 0:
                    log.error("Could not find restaurant in database...")
                    log.error("Adding to database...")
                    populate_database_django(lat,lng)
                else:
                    query_string = """SELECT * FROM 'dealioApp_restaurant' WHERE google_id='""" + value + """' LIMIT 1"""
                    lalala = list(Restaurant.objects.raw(query_string))

                    result_list += lalala
            except:
                log.error("Problem with querying database for " + key + "," + value)

        return render(request, 'dealioApp/restaurants.html', {'restaurants': result_list})
    except:
        log.error("There is a problem ------------------------------------------------------")
        return render(request, 'dealioApp/restaurants.html', {'restaurant': restaurants})
    #log.error(result_list)
    #return render(request, 'dealioApp/restaurants.html',{'restaurants': result_list })



    #if request.method == "POST":
        #res = request.GET['apiCoords']
        #print(res)
     #   location = request.POST['location']
      #  print(location)
    # do something if form is valid
    #restaurants = Restaurant.objects.all()
       # return HttpResponseRedirect('dealioApp/restaurants.html')
    #return render(request, 'dealioApp/restaurants.html')  # render looks in templates directory #can pass in content into render() such as dictionaries


class RestaurantCreate(CreateView):
    model = Restaurant
    fields = ['owner_number','name','description','phone_number','email_address','website','picture', 'category','rating','yelp','google_id','place_id','address']


class RestaurantUpdate(UpdateView):
    model = Restaurant
    fields = ['owner_number', 'name', 'description', 'phone_number', 'email_address', 'website', 'picture', 'category','rating', 'yelp','google_id','place_id','address']


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


def delete_promo(request, promo_id, restaurant_id):
    promo = Promotion.objects.get(id=promo_id)
    if request.method == 'POST':
        promo.delete()
        return HttpResponseRedirect('/promotions/' + restaurant_id)

    return render(request, 'dealioApp/promotion_confirm_delete.html', {'restaurant_id': restaurant_id})
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
def new_review(request, restaurant_id, promo_id):
    promo = Promotion.objects.get(id=promo_id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = addReview(request.POST)
        if form.is_valid():
            newRev = form.save()
            promo.addReview(newRev)
        return HttpResponseRedirect('/promotions/' + restaurant_id)
    else:
        form = addReview()
    return render(request, 'dealioApp/addReview.html', {'form': form})


# displays review
def display_reviews(request, promo_id):
    promo = Promotion.objects.get(id=promo_id)
    return render(request, 'dealioApp/reviews.html', {'promotion': promo})


# share a promo via email or text
def share_promo(request, promo_id):
    promo = Promotion.objects.get(id=promo_id)
    if request.method == 'POST':
        number = request.POST['number']
        email = request.POST['email']

        if email != '':
            send_promo_email(email, promo.title, promo.description)
        if number != '':
            send_promo_text(number, promo.title, promo.description)
        return HttpResponseRedirect('/promotions/' + str(promo.id))

    return render(request, 'dealioApp/share_promo.html')
