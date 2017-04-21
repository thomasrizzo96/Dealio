#################################################################################
#                                                                               #
#                         User Input Section                                    #               
#                                                                               #
#################################################################################
API_key = 'AIzaSyBueezSv1I_p8lywu8vm88YevVptloCcjo' #Google API key             #
                                                                                #
#Obtain these from Yelp's manage access picURL                                  #
consumer_key = "KdToqI0MOZpwy__h9P0G5Q"                                         #
consumer_secret = "gyLFUGT8qdPx5s0Y7-DuwPjW1pY"                                 #
token = "5shzFD20R6U7veZrMKUU8I0CwVD_qcEC"                                      #
token_secret = "Tlu11jZiJhgapgW1WEZD3Yf4A3U"                                    #
                                                                                #
#zipcodeapi.com converts zipcode to lat long coordinates for google maps api    #
zipcode_API = 'ScsZ7CgJqKKfH0p74zrXGn1X1UjstvSlIllQXBzomjD4k2coBDmh1nf3iyvL4o7N'#
                                                                                #
searchType = 'restaurant' #uses all the types found on google places website    #
searchKeyWord = 'Mexican' #What you're searching for                            #
mile_radius = 3 #Insert                                                         #
return_n_results = 5 #how many you want displayed. set to 0 for unlimited       #
use_current_location = False                                                #
zipcode = '84321'                                                               #
                                                                                #
#################################################################################

import urllib
import json
import requests
from PIL import Image

radius = mile_radius * 1609 #converts miles into meters
####################################
# Used to determine location

if use_current_location:
    send_url = 'http://freegeoip.net/json' #Gets a json list of IP information to locate you
    r = requests.get(send_url)
    j = json.loads(r.text)
    locationLat = j['latitude']
    locationLong = j['longitude']
    #print locationLat #used for testing latitude coordinates
    #print locationLong #used for testing longitude coordinates
else:
    zipURL = 'https://www.zipcodeapi.com/rest/' + zipcode_API + '/info.json/' + zipcode + '/degrees'
    urlData = urllib.urlopen(zipURL)
    jsonData = json.load(urlData)
    locationLat = jsonData['lat']
    locationLong = jsonData['lng']

#######################################

#locationLat = 41.745161 #lat and long for Logan, Ut
#locationLong = -111.8119312

########################################
#Yelp API for Yelp URL
import rauth
def get_search_parameters(lat,lng):
  #See the Yelp API for more details
  params = {}
  params["term"] = searchKeyWord
  params["ll"] = "{},{}".format(str(lat),str(lng))
  params["radius_filter"] = "30"
  params["limit"] = "20"
  return params

def get_results(params):   
  session = rauth.OAuth1Session(
    consumer_key = consumer_key
    ,consumer_secret = consumer_secret
    ,access_token = token
    ,access_token_secret = token_secret)
     
  request = session.get("http://api.yelp.com/v2/search",params=params)
  #Transforms the JSON API response into a Python dictionary
  data = request.json()
  session.close()
   
  return data

def get_yelp_url(lat,lng):
    try:
        yelpData = get_results(get_search_parameters(lat,lng))
        if yelpData is not None:
            if yelpData['businesses'] is not None:
                if yelpData['businesses'][0] is not None:
                    if yelpData['businesses'][0]['url'] is not None:
                        yelpURL = yelpData['businesses'][0]['url']
                        return yelpURL
    except:
        pass

#########################################
def google_search(searchType, searchKeyWord, radius):
        

    #searchType = 'restaurant' #configure this from one here: https://developers.google.com/places/supported_types
    encodedType = urllib.quote(searchType)

    #searchKeyWord = 'burger' #Use this to search for a keyword. I.e Burger
    encodedKeyWord = urllib.quote(searchKeyWord)


    rawData = urllib.urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(locationLat) + ',' + str(locationLong) + '&radius=' + str(radius) + '&type=' + encodedType + '&keyword=' + encodedKeyWord + '&key=' + API_key)

    #rawData = urllib.urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=41.745161,-111.8119312&radius=8000&type=bar&keyword=&key=AIzaSyBueezSv1I_p8lywu8vm88YevVptloCcjo

    jsonData = json.load(rawData)
    searchResults = jsonData['results']
    return searchResults


########################################
#printing Results
count = 0
for er in google_search(searchType,searchKeyWord, radius):
    if count >= return_n_results:
        break
    count += 1
    name = er['name']
    restaurantID = er['id']
    restaurantRating = er['rating']
    vicinity = er['vicinity']
    types = er['types']

    try:
        picture_reference = er['photos'][0]['photo_reference']
        picURL = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=' + picture_reference + '&key=' + API_key
        resource = urllib.urlopen(picURL)
        fileName = restaurantID + '.jpg'
        output = open("file01.jpg","wb")
        output.write(resource.read())
        output.close()

        img = Image.open('file01.jpg')
        img.show()
        
    except KeyError:
        output = None

    #pic = urllib.urlretrieve(picURL, "pic.jpg")
    #img = Image.open(pic)
    #img.show()
    
    print 'The name of restaurant is: ' + name
    print 'The unique ID is: ' + str(restaurantID)
    print 'The google restaurant rating is: ' + str(restaurantRating)
    print 'The address is: ' + vicinity
    #print types

    lat = er['geometry']['location']['lat']
    lng = er['geometry']['location']['lng']

    yelpURL = get_yelp_url(lat,lng)
    if yelpURL is not None: print yelpURL
    print '''

            '''
#yelpURL = get_yelp_url(lat,lng)
#if yelpURL is not None: print yelpURL
