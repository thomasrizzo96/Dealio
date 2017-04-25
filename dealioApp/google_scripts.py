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
#searchType = 'restaurant' #uses all the types found on google places website    #
#searchKeyWord = 'Mexican' #What you're searching for                            #
#mile_radius = 3 #Insert                                                         #
#return_n_results = 5 #how many you want displayed. set to 0 for unlimited       #
#use_current_location = True                                                #
#zipcode = '84321'                                                               #
                                                                                #
#################################################################################
import logging
log = logging.getLogger(__name__)

import urllib
import json
import requests
import codecs
import urllib.parse
#from PIL import Image

#radius = mile_radius * 1609 #converts miles into meters
####################################
# Used to determine location

#if use_current_location:
#    send_url = 'http://freegeoip.net/json' #Gets a json list of IP information to locate you
#    r = requests.get(send_url)
#    j = json.loads(r.text)
#    locationLat = j['latitude']
#    locationLong = j['longitude']
#    #print locationLat #used for testing latitude coordinates
#    #print locationLong #used for testing longitude coordinates
#else:
#    zipURL = 'https://www.zipcodeapi.com/rest/' + zipcode_API + '/info.json/' + zipcode + '/degrees'
#    urlData = urllib.request.urlopen(zipURL)
#    jsonData = json.load(urlData)
#    locationLat = jsonData['lat']
#    locationLong = jsonData['lng']

#######################################

#locationLat = 41.745161 #lat and long for Logan, Ut
#locationLong = -111.8119312

########################################
#This is the function called by django to return a dictionary populated with unique google IDs
def retrieve_results(p_locationLat,p_locationLong,p_radius,p_searchType,p_searchKeyWord,p_numResults):

    search_results = google_search(p_searchType, p_searchKeyWord, p_radius,p_locationLat,p_locationLong)

    dictionary = {}
    count = 0
    for er in search_results:
        if count >= p_numResults:
            break
        count += 1
        restaurantID = er['id']
        dictionary[count] = restaurantID
    return dictionary

import sqlite3
import sys
def populate_database(p_locationLat,p_locationLong):
    search_results = google_search('restaurant','',20,p_locationLat,p_locationLong)

    try:
        connection = sqlite3.connect("../db.sqlite3")

        cursor = connection.cursor()

        #print("Now trying to write to database")

        for er in search_results:
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
            print("Yelp Website: " + yelp)

            category = ""
            for i in er['types']:
                category +=i + ','

            try:
                find_string = "SELECT * FROM 'dealioApp_restaurant' WHERE google_id ='" + unique_id + "' LIMIT 1;"
                cursor.execute(find_string)
                results = cursor.fetchall()
                #print(results)
                if len(results)==0:
                    print(name + " was not in database. Inserting now.")

                    string = """INSERT INTO dealioApp_restaurant(owner_number, name, description, address, phone_number, email_address, website, picture, category, rating, yelp, google_id) VALUES (""" + str(owner_id) + """," """ + name + """",'"""+ description + """','""" + address + """','""" + phone_number + """','""" + email_address + """','""" + website + """','""" + picture + """','""" + category + """','""" + str(rating) + """','""" + yelp + """','""" + unique_id + """');"""

                    #string = """INSERT INTO dealioApp_restaurant VALUES (""" + str(owner_id) + """,'""" + name + """','"""+ description + """','""" + address + """','""" + phone_number + """','""" + email_address + """','""" + website + """','""" + picture + """','""" + category + """','""" + str(rating) + """','""" + yelp + """','""" + unique_id + """');"""
                    #print(string)
                    cursor.execute(string)
                    connection.commit()
                else:
                    print(name + " is already in database. Skipping entry...")
                    continue

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



########################################
#Yelp API for Yelp URL
import rauth #Used for the Yelp URL API

def get_search_parameters(lat,lng):
  #See the Yelp API for more details
  params = {}
  params["term"] = '' #change this to serach for keyword
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

def google_search(p_searchType, p_searchKeyWord, p_radius,p_locationLat,p_locationLong):

    p_radius *= 1609 #converts miles to meters

    #searchType = 'restaurant' #configure this from one here: https://developers.google.com/places/supported_types
    encodedType = urllib.parse.quote(p_searchType)

    #searchKeyWord = 'burger' #Use this to search for a keyword. I.e Burger
    encodedKeyWord = urllib.parse.quote(p_searchKeyWord)


    rawData = urllib.request.urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(p_locationLat) + ',' + str(p_locationLong) + '&radius=' + str(p_radius) + '&type=' + encodedType + '&keyword=' + encodedKeyWord + '&key=' + API_key)
    #log.error("Raw data: " + rawData)
    #rawData = urllib.urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=41.745161,-111.8119312&radius=8000&type=bar&keyword=&key=AIzaSyBueezSv1I_p8lywu8vm88YevVptloCcjo

    reader = codecs.getreader("utf-8")
    jsonData = json.load(reader(rawData))


    searchResults = jsonData['results']
    return searchResults


#test_results = retrieve_results(41.745161,-111.8119312,5,'restaurant','mexican',5)
#print(test_results)

#populate_database(41.745161,-111.8119312)
