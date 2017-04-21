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
searchKeyWord = '' #What you're searching for                            #
mile_radius = 5 #Insert                                                         #
return_n_results = 25 #how many you want displayed. set to 0 for unlimited       #
use_current_location = True                                                #
zipcode = '84321'                                                               #
                                                                                #
#################################################################################

import urllib
import json
import requests
import urllib.request, json
import codecs

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
    urlData = urllib.request.urlopen(zipURL)
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
    encodedType = urllib.request.quote(searchType)

    #searchKeyWord = 'burger' #Use this to search for a keyword. I.e Burger
    encodedKeyWord = urllib.request.quote(searchKeyWord)


    rawData = urllib.request.urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(locationLat) + ',' + str(locationLong) + '&radius=' + str(radius) + '&type=' + encodedType + '&keyword=' + encodedKeyWord + '&key=' + API_key)
    reader = codecs.getreader("utf-8")
    obj = json.load(reader(rawData))
    #rawData = urllib.urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=41.745161,-111.8119312&radius=8000&type=bar&keyword=&key=AIzaSyBueezSv1I_p8lywu8vm88YevVptloCcjo

    #jsonData = json.load(obj)
    searchResults = obj['results']
    return searchResults

########################################
#Connect to database
import sqlite3
import sys

try:
    connection = sqlite3.connect("db.sqlite3")
    
    cursor = connection.cursor()
    
    print("Now trying to write to database")

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

        #picture_reference = er['photos'][0]['photo_reference']
        #picURL = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=' + picture_reference + '&key=' + API_key
        
    #print ('The name of restaurant is: ' + name)
    #print ('The unique ID is: ' + str(restaurantID))
    #print ('The google restaurant rating is: ' + str(restaurantRating))
    #print ('The address is: ' + vicinity)
    #print types

        lat = er['geometry']['location']['lat']
        lng = er['geometry']['location']['lng']

        yelpURL = get_yelp_url(lat,lng)
        if yelpURL is None: yelpURL = ''

        unique_id = er['id']
        owner_id = 0
        name = er['name']
        description = "To be implemented"
        address = er['vicinity']
        phone_number = "To be implemented"
        email_address = "To be implemented"
        website = "To be implemented"
        picture = "To be implemented"
        rating = er['rating']
        yelp = yelpURL

        category = ""
        for i in er['types']:
            category +=i + ','

        print("Writing " + name + " to Database")

        try:
            string = """INSERT INTO dealioApp_restaurant VALUES ('""" + unique_id + """',""" + str(owner_id) + """,'""" + name + """','"""+ description + """','""" + address + """','""" + phone_number + """','""" + email_address + """','""" + website + """','""" + picture + """','""" + category + """','""" + str(rating) + """','""" + yelp + """');"""
            print(string)
            cursor.execute(string)
            connection.commit()
            
        except sqlite3.Error as e:
    
            if connection:
                connection.rollback()
                print("\n\n")
                print("Error %s:" % e.args[0])
                print("\n\n")
except sqlite3.Error as e:
    
    if connection:
        connection.rollback()
        
    print ("Error %s:" % e.args[0])

finally:
    
    if connection:
        connection.close() 

    
##########################################################################

    #unique_id
    #owner_id
    #name
    #description
    #address
    #phone_number
    #email_address
    #website
    #picture
    #category
    #rating
    #yelp

