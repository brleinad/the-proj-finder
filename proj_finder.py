"""

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

    def main():

        # TODO: optionally get the email/key from the user.
        email    = 'daniel.rodas.bautista@gmail.com'
        key      = '200222284-dae8be573771fdff71e7b535b47b600d'

        nearby_routes = []
        best_routes   = []
        MP            = MountainProjectAPI(email, key)
        location      = Location()


        # Testing
        MP.get_user(email)
        
        ## User gives max red point grade (sport by default).
        ## Optionally the user can choose max distance, style, pitches, etc.
        #self.get_user_input()

        ## Getting the location based on the IP address.
        #location.get_location()

        ## Based on that location ask MP for all the routes nearby (max default 50).
        #nearby_routes = MP.get_nearby_routes(location)

        ## Parse the list of routes to get the best ones (top 5 by default).
        #best_routes = self.get_best_routes(nearby_routes)

        ## Show in a pretty way these routes with route name, grade, location, link.
        #self.print_routes(best_routes)


class MountainProjectAPI():
    """
    """

    MP_URL = 'https://www.mountainproject.com/data/'
    parameters = {}

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


    def get_best_routes(self, routes):
        """
        Returns a list of the 10 best rated routes from a list of routes
        """
        pass

    def get_nearby_routes(location, max_distance = 30, max_results = 50, min_diff = 5.6, max_diff = 5.13):
        """
        Given a location in the form of a tuple it will look for all the routes near that location and return them in a list of routes.
        """
        pass


class Location():
    """
    """
    longitude = ''
    lattitude = ''
    place     = []

    def __init__(self):
        pass

    def get_location():
        """
        Returns a touple with lattitute and longitude according to the IP address.
        """
        pass


class Route():
    """
    A class to encapsulate all the information of a route along with some helpful methods.
    """

    def __init__(self, name, style, grade, stars, pitches, location, url):
        self.name     = name
        self.style    = style
        self.grade    = grade
        self.stars    = stars
        self.pitches  = pitches
        self.location = location
        self.url      = url

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


ProjFinder.main()
