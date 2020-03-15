"""

TODOs:
    * Error handling: MP API not working, no routes near location
    * add weather forecast 
    * Write all doc strings
    * Write doc tests
    * Write a few tests
"""

__author__ = 'Daniel Rodas Bautista'

import requests
import json 
import ipinfo


class ProjFinder():
    """
    """

    def __init__(self):
        self.nearby_route =[]

    def get_best_routes(self, routes):
        """
        Returns a list of the best routes (based on the stars) given a list of routes)
        """
        #Sort the list of routes
        #split the list to give just the first 5
        best_routes = routes
        return best_routes
        pass

    def main(self):

        # TODO: optionally get the email/key from the user.
        email    = 'daniel.rodas.bautista@gmail.com'
        key      = '200222284-dae8be573771fdff71e7b535b47b600d'

        nearby_routes = []
        best_routes   = []
        MP            = MountainProjectAPI(email, key)
        location      = Location()


        # Testing
        #MP.get_user(email)
        
        ## User gives max red point grade (sport by default).
        ## Optionally the user can choose max distance, style, pitches, etc.
        #self.get_user_input()

        ## Getting the location based on the IP address.
        location.get_location()
        print('Your location is set to:')
        location.print_location()

        ## Based on that location ask MP for all the routes nearby (max default 50).
        print('\nGetting nearby routes:')
        nearby_routes = MP.get_nearby_routes(location)
        for route in nearby_routes:
            route.print_route_name()

        ## Parse the list of routes to get the best ones (top 5 by default).
        best_routes = self.get_best_routes(nearby_routes)

        ## Show in a pretty way these routes with route name, grade, location, link.
        #self.print_routes(best_routes)


class MountainProjectAPI():
    """
    A class to interact with the Mountain Project API https://www.mountainproject.com/data
    """

    def __init__(self, email, key):

        self.parameters = {
                'email' : email,
                'key'   : key,
                }

    def jprint(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def get_user(self, user):
        """
        Given a user ID or corresponding email it will retrieve the user's information from MP.
        """

        response = requests.get(self.MP_URL+'get-user', params = self.parameters)
        self.jprint(response.json())
        return response

    def get_nearby_routes(self, location, max_distance = 30, max_results = 50, min_diff = 5.6, max_diff = 5.13):
        """
        Given a location in the form of a tuple it will look for all the routes near that location and return them in a list of routes.
        """
        #Required Arguments:
        #key - Your private key
        #lat - Latitude for a given area
        #lon - Longitude for a given area
        #Optional Arguments:
        #maxDistance - Max distance, in miles, from lat, lon. Default: 30. Max: 200.
        #maxResults - Max number of routes to return. Default: 50. Max: 500.
        #minDiff - Min difficulty of routes to return, e.g. 5.6 or V0.
        #maxDiff - Max difficulty of routes to return, e.g. 5.10a or V2.

        params = self.parameters

        params['lat']         = location.latitude
        params['lon']         = location.longitude
        params['maxDistance'] = max_distance
        params['maxResults']  = max_results
        params['minDiff']     = min_diff
        params['maxDiff']     = max_diff

        #response = requests.get(self.MP_URL+'get-routes-for-lat-lon', params = self.parameters)
        response = self.get_response_from_api('get-routes-for-lat-lon', params)
        #self.jprint(response.json())
        nearby_routes = self.json2routes(response.json())
        return nearby_routes

    def get_response_from_api(self, api_method, parameters):
        """
        """
        MP_URL   = 'https://www.mountainproject.com/data/'
        #try:
        response = requests.get(''.join((MP_URL, api_method)), params = parameters)
        #response = requests.get(MP_URL+api_method, params = parameters)
        #except ConnectionError:
            #print('ERROR: Could not connect to Mountain Project')
        return response

    def json2routes(self, json_routes):
        """
        Returns a list of route objects given a json containing routes.
        """

        routes = []

        for json_route in json_routes['routes']:
            #print(route['name'])
            loc = Location()
            loc.latitude  = json_route['latitude'],
            loc.longitude = json_route['longitude'],
            loc.place     = json_route['location'],

            route  = Route(
                name     = json_route['name'], 
                style    = json_route['type'],
                grade    = json_route['rating'],
                stars    = json_route['stars'],
                pitches  = json_route['pitches'],
                url      = json_route['url'],
                location = loc
                )

            routes.append(route)

        return routes


class Location():
    """
    """
    longitude = ''
    latitude = ''
    place     = []

    def __init__(self):
        pass

    #def __str__(self):
        #return 

    def get_location(self, ip_address = None):
        """
        Returns a touple with lattitute and longitude according to the IP address. It uses the ipinfo library.
        """

        access_token   = 'eba1bfd8659873'
        handler        = ipinfo.getHandler(access_token)
        details        = handler.getDetails(ip_address)
        self.city      = details.city
        self.country   = details.country
        self.longitude = details.longitude
        self.latitude  = details.latitude
        return (self.latitude, self.longitude,)

    def print_location(self):
        """
        Detailed printing of location.
        """
        print(self.latitude + ', ' + self.longitude)
        print('Latitude  : ' + self.latitude)
        print('Longitude : ' + self.longitude)
        print('city      : ' + self.city)
        print('country   : ' + self.country)


class Route():
    """
    A class to encapsulate all the information of a route along with some helpful methods.
    """

    def __init__(self, name, style, grade, stars, pitches, url, location):
        self.name     = name
        self.style    = style
        self.grade    = grade
        self.stars    = stars
        self.pitches  = pitches
        self.location = location
        self.url      = url

    def __str__(self):
        return self.name

    def is_single_pitch(self):
        return self.pitches == 1

    def is_multi_pitch(self):
        return self.pitches > 1

    def is_five_stars(self):
        return self.stars == 5

    def is_good_route(self):
        return self.stars > 4

    def is_sport(self):
        return self.style == 'sport'

    def print_route_name(self):
        #print((self.name, self.grade))
        print(self)


if __name__ == '__main__':
    proj_finder = ProjFinder()
    try:
        proj_finder.main()
    except (ConnectionError):
        print('Could not connect to Mountain Project API')
