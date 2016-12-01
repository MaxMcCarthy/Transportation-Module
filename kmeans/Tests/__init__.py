import unittest

from kmeans.Centroid import Centroid
import numpy as np

from kmeans.ImageOutput import *
from kmeans.Interface import *
from kmeans.KMeans import *


class testCentroid(unittest.TestCase):
    '''
    test all centroid functions here
    '''

    def test_constructor(self):
        '''
        test basic constructor
        :return:
        '''
        point_arr = [2, 3]
        centroid = Centroid(1, point_arr)

        # coordinates in 2D
        self.assertEqual(len(centroid.coords), 2)
        self.assertEqual(centroid.coords[0], 2)
        self.assertEqual(centroid.coords[1], 3)
        self.assertEqual(centroid.id, 1)

    def test_add_points(self):
        '''
        test adding of data to points array
        :return:
        '''
        point_arr = [2, 3]
        centroid = Centroid(1, point_arr)

        # add one point
        centroid.add_point([2,1])
        self.assertEqual(len(centroid.points), 1)
        self.assertEqual(centroid.points.item(0,0), 2)
        self.assertEqual(centroid.points.item(0,1), 1)

        # add a second point
        centroid.add_point([3,2])
        self.assertEqual(len(centroid.points), 2)
        self.assertEqual(centroid.points.item(1,0), 3)
        self.assertEqual(centroid.points.item(1,1), 2)

class testKMeans(unittest.TestCase):
    '''
    test all KMeans fucntions here
    '''

    def test_init_centroid(self):
        '''
        randomly initializes centroids
        :return:
        '''
        data = np.array([[1, 2], [3, 4], [2, 5]])
        centroid_list = init_centroids(4, data)
        for centroid in centroid_list:
            #print centroid
            self.assertAlmostEqual(centroid.coords.item(0), 2, delta=1)
            self.assertAlmostEqual(centroid.coords.item(1), 3.5, delta=1.5)

    def test_assign_centroid(self):
        '''
        test assigning of centroids
        :return:
        '''
        # centroid at 2,2
        centroid_a = Centroid(0, [2,2])
        # centroid at 5,5
        centroid_b = Centroid(1, [5,5])
        # data points in numpy.array
        # want to see that (1,1), (0,1), (0,0), (2,3), (3,3) belong to 2,2
        # rest go to 5,5
        data = np.array([[1,1], [0,1], [0,0], [2,3], [3,3], [4,5], [7,1], [20,20]])

        # assign centroids
        assign_centroid([centroid_a, centroid_b], data)

        # check centroid a
        self.assertEqual(len(centroid_a.points), 5)
        self.assertEqual(len(centroid_b.points), 3)
        self.assertEqual(centroid_a.points.item(0,0), 1)
        self.assertEqual(centroid_a.points.item(0,1), 1)
        self.assertEqual(centroid_a.points.item(1,0), 0)
        self.assertEqual(centroid_a.points.item(1,1), 1)
        self.assertEqual(centroid_a.points.item(2,0), 0)
        self.assertEqual(centroid_a.points.item(2,1), 0)
        self.assertEqual(centroid_a.points.item(3,0), 2)
        self.assertEqual(centroid_a.points.item(3,1), 3)
        self.assertEqual(centroid_a.points.item(4,0), 3)
        self.assertEqual(centroid_a.points.item(4,1), 3)

        # check centroid b
        self.assertEqual(centroid_b.points.item(0,0), 4)
        self.assertEqual(centroid_b.points.item(0,1), 5)
        self.assertEqual(centroid_b.points.item(1,0), 7)
        self.assertEqual(centroid_b.points.item(1,1), 1)
        self.assertEqual(centroid_b.points.item(2,0), 20)
        self.assertEqual(centroid_b.points.item(2,1), 20)

    def test_use_all_centroids(self):
        '''
        makes sure that if there is an unused centroid, that it gets moved
        and assigned to data
        :return:
        '''

        # centroid at 2,2
        centroid_a = Centroid(0, [2,2])
        # centroid at 100,100 - should be unused
        centroid_b = Centroid(1, [100,100])
        # data points in numpy.array
        # want to see that (1,1), (0,1), (0,0), (2,3), (3,3) belong to 2,2
        # rest go to 5,5
        data = np.array([[1,1], [0,1], [0,0], [2,3], [3,3], [4,5], [7,1], [20,20]])

        # assign centroids
        assign_centroid([centroid_a, centroid_b], data)

        # centroid_b has no points
        self.assertEqual(centroid_b.points, None)

        # reassign
        use_all_centroids([centroid_a, centroid_b], data)

        # impossible to know how the random generator assigned the centroid, so it will
        # be sufficient to test that it has MOVED and now has points associated with it
        #print centroid_b.coords
        self.assertFalse(centroid_b.coords.item(0) == 100)
        self.assertFalse(centroid_b.coords.item(1) == 100)
        self.assertFalse(len(centroid_b.points) == 0)

    def test_update_centroids(self):
        '''
        test to see that centroids update themsleves to match the mean of their data
        :return:
        '''

        # centroid at 2,2
        centroid_a = Centroid(0, [2,2])
        # data
        data = np.array([[1,1], [0,1], [0,0], [2,3]])
        # assign data to centroid
        assign_centroid([centroid_a], data)
        # update the centroid location
        new_centroid = update_centroids([centroid_a])[0]
        self.assertEqual(new_centroid.coords.item(0), .75)
        self.assertEqual(new_centroid.coords.item(1), 1.25)
        self.assertTrue(len(new_centroid.points) > 0)

    def test_check_centroid_array_equality(self):
        '''
        test to see if 2 centroid arrays are equal
        :return:
        '''

        centroid_a = Centroid(0, [2,1])
        centroid_b = Centroid(1, [2,1])
        centroid_c = Centroid(2, [3,0])

        # check for equality
        self.assertTrue(check_centroid_array_eqality([centroid_a], [centroid_b]))
        self.assertFalse(check_centroid_array_eqality([centroid_b], [centroid_c]))
        self.assertFalse(check_centroid_array_eqality([centroid_c], []))

    def test_k_means(self):
        '''
        test k_means algorithm
        hard to test because of randomly generated centroids
        will be content here to just run it and test it in images
        :return:
        '''

        data = np.array([[1,1], [0,1], [0,0], [2,3], [3,3], [4,5], [7,1], [2,2]])
        centroid_arr = k_means(2, data, False, "")
        self.assertTrue(len(centroid_arr) == 2)
        for center in centroid_arr:
            self.assertFalse(center.points is None)

    def test_get_max_x(self):
        '''
        test get maximum x value from data
        :return:
        '''
        data = np.array([[1,1], [0,1], [0,0], [2,3], [3,3], [4,5], [7,1], [2,2]])
        get_max_x_data(data)

class testImageOutput(unittest.TestCase):
    '''
    test all imageoutput functions here
    '''

    def test_write_2D_picture(self):
        '''
        test writing of output picture
        :return:
        '''

        data = np.array([[145, 188],
                        [147, 187],
                        [150, 195],
                        [147, 211],
                        [136, 240],
                        [125, 262],
                        [110,  46],
                        [ 95,  29],
                        [ 94,  29],
                        [104,  21],
                        [115,  17],
                        [156,  10],
                        [181,  68],
                        [154, 305],
                        [137, 426],
                        [138, 381],
                        [137, 378],
                        [133, 366],
                        [131, 370],
                        [133, 380],
                        [137, 362],
                        [139, 355],
                        [156, 231],
                        [167, 181],
                        [156, 242],
                        [155, 236],
                        [162, 224],
                        [166, 248],
                        [174, 259],
                        [177, 203],
                        [155, 322],
                        [97, 552],
                        [66, 576],
                        [66, 572],
                        [66, 577],
                        [66, 574],
                        [66, 571],
                        [66, 572]])
        centroids = k_means(3, data, True, "image")
        for center in centroids:
            self.assertFalse(center.points is None)
        arr = np.max(data, axis=0)

    def test_scale(self):
        print scale(125, 300)

class testInterface(unittest.TestCase):
    '''
    test all interface functions here
    '''

    def test_parse_csv(self):
        '''
        test parsing of csv file
        :return:
        '''

        #parse_csv('/Users/Max/PycharmProjects/Final0/absentee.csv')