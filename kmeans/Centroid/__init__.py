import numpy as np

class Centroid(object):
    '''
    class defines the centroid object
    each object will have coordinates stored in a vector
    to support multiple dimensions
    each object will also have an ID to later be used in coloring
    '''

    coords = None
    points = None
    id = 0

    def __init__(self, id, coord_arr):
        '''
        create new Driver object
        :param id: id of the new centroid
        :param coord_arr: array of integers
        '''

        self.coords = np.array(coord_arr)
        self.id = id
        self.points = None

    def add_point(self, coordinates):
        '''
        adds given coordinates to the points array
        :param coordinates: a point to add to the coord array
        :return:
        '''
        if self.points is None:
            self.points = np.array([coordinates])
        else:
            self.points = np.append(self.points, [coordinates], axis=0)
