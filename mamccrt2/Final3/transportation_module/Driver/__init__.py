from geopy import Nominatim
import simplejson, urllib

class Driver(object):
    '''
    class defines the centroid object
    each object will have coordinates stored in a vector
    to support multiple dimensions
    each object will also have an ID to later be used in coloring
    '''

    driver_address = ""
    prev_address = ""
    meeting_address = ""
    car_location = []
    meeting_spot = []
    points = []
    id = 0
    car_size = 0
    driver_name = ""
    dorm_code = ""

    def __init__(self, id, address, car_size, driver_name, dorm_code):
        '''
        create new Driver object
        :param id: id of the new driver
        :param address: a string address
        :param car_size: size of car not including driver
        '''

        self.car_size = car_size
        self.id = id
        self.points = []
        self.driver_name = driver_name
        self.meeting_spot = []
        self.driver_address = address
        self.meeting_address = address
        self.prev_address = ""
        self.car_location = self.get_coordinates(address)
        self.dorm_code = dorm_code

    def add_point(self, point, distance):
        '''
        adds given point to the points array
        :param point: a point to add to the coord array
        :return:
        '''

        self.points.append(point)
        point.distance = distance

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
