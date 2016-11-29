import unittest
import requests
import urllib
import json
import simplejson
from transportation_module.Athlete import Athlete
from transportation_module.Driver import Driver
from transportation_module.KMeans import *
from transportation_module.Interface import *

class testDriver(unittest.TestCase):
    '''
    test all driver functions here
    '''

    def test_constructor(self):
        '''
        test basic constructor
        :return:
        '''

        address = "1401 W Green Street, Urbana IL"
        driver = Driver(0, address, 4, "Owen")

        self.assertEqual(driver.id, 0)
        self.assertAlmostEqual(driver.car_location[0], 40.109387, delta=0.001)
        self.assertAlmostEqual(driver.car_location[1], -88.2272456, delta=0.001)
        self.assertEqual(driver.driver_name, "Owen")
        self.assertEqual(len(driver.points), 0)
        self.assertEqual(driver.meeting_spot, [])

    def test_add_points(self):
        '''
        test adding of data to points array
        :return:
        '''

        athlete_address = "29 East John Street, Champaign IL"
        driver_address = "1401 W Green Street, Urbana IL"

        driver = Driver(0, driver_address, 4, "Owen")
        athlete = Athlete("Max", athlete_address, 0)
        driver.add_point(athlete, 0)

        self.assertEqual(len(driver.points), 1)
        self.assertEqual(driver.points[0].name, "Max")



class testAthlete(unittest.TestCase):
    '''
    test all athlete functions here
    '''

    def test_constructor(self):
        '''
        test basic constructor
        :return:
        '''

        address = "29 East John Street, Champaign IL"
        athlete = Athlete("Max", address, 0)

        self.assertEqual(athlete.name, "Max")
        self.assertEqual(athlete.address, address)
        self.assertEqual(len(athlete.position), 2)
        self.assertAlmostEqual(athlete.position[0], 40.1091848, delta=0.001)
        self.assertAlmostEqual(athlete.position[1], -88.24092639999998, delta=0.001)
        self.assertEqual(athlete.id, 0)



class testKMeans(unittest.TestCase):
    '''
    test all KMeans fucntions here
    '''

    def test_init_centroid(self):
        '''
        initializes centroids
        :return:
        '''

        path = "/Users/Max/PycharmProjects/Final1/transportation_module/drivers.csv"
        driver_list = init_centroids(path)
        self.assertEqual(len(driver_list), 3)
        self.assertEqual(driver_list[0].driver_name, "Driver 1")
        self.assertEqual(driver_list[0].driver_address, "1109 West Stougton, Urbana IL")
        self.assertEqual(driver_list[0].car_size, 4)
        self.assertEqual(driver_list[0].id, 0)


    def test_assign_centroid(self):
        '''
        test assigning of centroids
        :return:
        '''
        driver_path = "/Users/Max/PycharmProjects/Final1/transportation_module/drivers.csv"
        rower_path = "/Users/Max/PycharmProjects/Final1/transportation_module/rowers.csv"
        driver_list = init_centroids(driver_path)

        points = init_athletes(rower_path)

        data = [
            [2403, 2513, 0],
            [2403, 2513, 0],
            [2188, 2822, 198],
            [2188, 2822, 198],
            [2448, 318, 2472],
            [1862, 608, 2181],
            [1915, 662, 2128],
            [512, 2472, 1772],
            [807, 2767, 1879],
            [2210, 729, 3945],
            [714, 2083, 1502],
            [1299, 1678, 1020],
            [2337, 1084, 1999],
            [2458, 1205, 2120],
            [2336, 206, 2598],
            [2351, 221, 2618],
            [2457, 1205, 2119],
            [3360, 1500, 2420],
            [2159, 906, 1884]
        ]

        assign_to_cars(driver_list, points, data)

        self.assertEqual(len(driver_list[0].points), 4)
        self.assertEqual(len(driver_list[1].points), 4)
        self.assertEqual(len(driver_list[2].points), 6)

    def test_init_distance_matrix(self):
        '''
        test distance matrix
        :return:
        '''

        athlete_address = "29 East John Street, Champaign IL"
        driver_path = "/Users/Max/PycharmProjects/Final1/transportation_module/drivers.csv"
        driver_list = init_centroids(driver_path)
        athlete = Athlete("Max", athlete_address, 0)
        distance_matrix = init_distance_matrix(driver_list, [athlete])
        self.assertEqual(distance_matrix[0][0], 1982)
        self.assertEqual(distance_matrix[0][1], 548)
        self.assertEqual(distance_matrix[0][2], 3344)

        data = [
            [2403, 2513, 0],
            [2403, 2513, 0],
            [2188, 2822, 198],
            [2188, 2822, 198],
            [2448, 318, 2472],
            [1862, 608, 2181],
            [1915, 662, 2128],
            [512, 2472, 1772],
            [807, 2767, 1879],
            [2210, 729, 3945],
            [714, 2083, 1502],
            [1299, 1678, 1020],
            [2337, 1084, 1999],
            [2458, 1205, 2120],
            [2336, 206, 2598],
            [2351, 221, 2618],
            [2457, 1205, 2119],
            [3360, 1500, 2420],
            [2159, 906, 1884]
        ]

        rower_path = "/Users/Max/PycharmProjects/Final1/transportation_module/rowers.csv"
        #points = init_athletes(rower_path)
        #new_dist = init_distance_matrix(driver_list, points)
        #self.assertEqual(new_dist, data)

        #assign_to_cars(driver_list, points, new_dist)
        #update_drivers(driver_list)


    def test_update_centroids(self):
        '''
        test to see that centroids update themsleves to match the mean of their data
        :return:
        '''

        driver_path = "/Users/Max/PycharmProjects/Final1/transportation_module/drivers.csv"
        driver_list = init_centroids(driver_path)
        rower_path = "/Users/Max/PycharmProjects/Final1/transportation_module/rowers.csv"
        points = init_athletes(rower_path)
        new_dist = init_distance_matrix(driver_list, points)

        assign_to_cars(driver_list, points, new_dist)
        update_drivers(driver_list)

        self.assertAlmostEqual(driver_list[0].car_location[0], 40.1097408, delta=0.001)
        self.assertAlmostEqual(driver_list[0].car_location[1], -88.223517, delta=0.0015)

        #data = init_distance_matrix(driver_list, points)
        #assign_to_cars(driver_list, points, data)
        #update_drivers(driver_list)



    def test_kmeans(self):
        """
        test full kmeans alorithm
        :return:
        """

        driver_path = "/Users/Max/PycharmProjects/Final1/transportation_module/drivers.csv"
        driver_list = init_centroids(driver_path)
        rower_path = "/Users/Max/PycharmProjects/Final1/transportation_module/rowers.csv"
        points = init_athletes(rower_path)

        k_means(driver_list, points)


    def test_efficiency(self):
        """
        test efficiency here
        :return:
        """

        address0 = "806 W Springfield Ave, Urbana, IL"
        address1 = "1109 West Stoughton, Urbana IL"
        address2 = "1007 South First, Champaign IL"
        address3 = "906 W College Ct, Urbana, IL 61801"
        address4 = "207 East Gregory Drive, Champaign, IL 61820"
        address5 = "1107 S 4th St, Champaign, IL 61820"
        address6 = "1201 S 4th St, Champaign, IL 61820"

        #def __init__(self, id, address, car_size, driver_name):

        driver0 = Driver(0, address0, 3, "d0")
        driver1 = Driver(1, address1, 2, "d1")
        driver2 = Driver(2, address2, 3, "d2")

        #def __init__(self, name, address, id):

        athlete0 = Athlete("a0", address3, 0)
        athlete1 = Athlete("a1", address4, 1)
        athlete2 = Athlete("a2", address5, 2)
        athlete3 = Athlete("a3", address6, 3)

        drivers = [driver0, driver1, driver2]
        athletes = [athlete0, athlete1, athlete2, athlete3]

        k_means(drivers, athletes)

        #check_efficiency(drivers)

        self.assertEqual(len(drivers), 2)
        for driver in drivers:
            self.assertEqual(len(driver.points), driver.car_size)
