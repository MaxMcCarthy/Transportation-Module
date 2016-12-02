import numpy as np
from geopy.geocoders import Nominatim
import simplejson, urllib

class Athlete(object):
    '''
    describes the point object;
    each point has an array of coords
    and will be assigned a a centroid id
    '''

    distance = 0
    position = []
    id = 0
    name = ""
    address = ""
    dorm_code = ""

    def __init__(self, name, address, id, dorm_code):
        '''
        sets up a point in space Rn
        centroid id is set to -1 initially since
        it currently does not belong to any set
        :param coord_arr: array of coordinates
        '''

        self.id = id
        self.distance = 0
        self.name = name
        self.address = address
        self.position = self.get_coordinates(address)
        self.dorm_code = dorm_code


    def create_position(self, address):
        '''
        uses geopy package to get the latitude
        and longitude of a given address
        :param address: the address to get coordinates from
        :return:
        '''

        geolocator = Nominatim()
        location = geolocator.geocode(address)
        if location is None:
            self.position = [0,0]
        else:
            self.position = [location.latitude, location.longitude]

    def get_coordinates(self, address):
        '''
        takes in a string and uses the google API to get
        the geographical coordinates
        :param address: string representing address
        :return: a 2 element array representing lat and lng
        '''

        key = "&key=AIzaSyBfb5NKTnSfrLGqSqWsIbvDzxloiC2DRnU"
        coord_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
        geo = simplejson.load(urllib.urlopen(coord_url + address.replace(" ", "+") + key))
        return [geo['results'][0]['geometry']['location']['lat'], geo['results'][0]['geometry']['location']['lng']]