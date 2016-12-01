import csv
import sys

import numpy as np

from kmeans.KMeans import k_means


def collect_data(factor_arr, lists):
    """
    from the list of factors and the json object lists,
    a numpy array is made full of data
    :param factor_arr: list of which factors to use
    :param lists: json object with data
    :return: a numpy array with selected data
    """

    factor_arr = check_factors(factor_arr, lists)
    data = None
    for index in range(1, len(lists)):
        row = []
        for factor in factor_arr:
            row.append(int(lists[index][factor]))
        if data is None:
            data = np.array([row])
        else:
            data = np.append(data, [row], axis=0)
    return data


def check_factors(factor_arr, lists):
    """
    looks through lists to make sure that all the desired
    factors are numerical
    :param factor_arr: array of which factors to use
    :param lists: json object with data
    :return: updated factor_array
    """

    # know that lists[0] is the header
    if len(lists) > 2:
        data_row = lists[1]
        for fact_num in factor_arr:
            try:
                converted_int = int(data_row[fact_num])
            except:
                print "Removed factor " + lists[0][fact_num]
                factor_arr.remove(fact_num)
                print factor_arr
    return factor_arr


def parse_csv(file_name):
    '''
    parses given file into json and runs our algorithm
    :param file_name: csv file name
    :return: numpy array of data
    '''

    lists = open_csv(file_name)

    # prompt for factors
    print("Select from the following factors:: ")
    print("Enter the factor number separated by commas with no space")
    count = 0
    for itr in range(1, len(lists[0])):
        print str(count) + ": " + str(lists[0][itr])
        count +=1
    '''for factor in lists[0]:
        print str(count) + ": " + str(factor)
        count += 1'''

    # get factors in integer form
    factor_arr = get_factors(count, "Factor")

    # get data
    data = collect_data(factor_arr, lists)
    return data


def open_csv(file_name):
    """
    parses a given .csv file and returns it
    in json form
    :param file_name: name of hte file
    :return: a json object
    """

    lists = None
    while lists is None:
        try:
            with open(file_name, 'r') as f:
                reader = csv.reader(f)
                lists = list(reader)
        except:
            print("Could not open your .csv file...")
            file_name = raw_input("Renter a .csv file name or type 'exit' to quit>  ")
            if file_name == 'exit':
                sys.exit(1)
    return lists


def print_centroids(centroids):
    '''
    given an array of centroids, print the coords
    :param centroids: PYTHON array of centroids to print
    :return:
    '''

    for centroid in centroids:
        print "Centroid center:" + str(centroid.id)
        print centroid.coords
        print "Centroid " + str(centroid.id) + " has " + str(len(centroid.points)) + " data points"
        print ""

def print_stats(centroids):
    """
    prints stats about centroids
    :param centroids: array of centroids
    :return: nothing
    """

    for centroid in centroids:
        print "Centroid" + str(centroid.id) + " has " + str(len(centroid.points)) + " data points"


def get_factors(biggest_factor, item_label):
    """
    makes sure that the factors are integer values; max of 10 factors
    :param item_label:
    :param biggest_factor: the largest numerical value for a factor number
    :return: a list of integer factors
    """

    factors = []
    factor_text = raw_input("Enter the " + item_label + " separated by commas with no space> ")
    factor_arr = factor_text.split(',')
    while len(factors) != len(factor_arr):
        for num in factor_arr:
            try:
                str_to_num = int(num)
            except:
                print item_label + " is not an integer"
                factor_text = raw_input("Enter the " + item_label + " separated by commas with no space> ")
                factor_arr = factor_text.split(',')
                factors = []
                break
            if str_to_num >= biggest_factor or str_to_num < 0:
                print item_label + " " + str(str_to_num) + " is out of range"
                factor_text = raw_input("Renter the " + item_label + " separated by commas with no space> ")
                factor_arr = factor_text.split(',')
                factors = []
                break
            else:
                factors.append(str_to_num)
    return factors


if __name__ == '__main__':
    while raw_input("Hit enter to begin or type 'exit' to quit ") != "exit":
        file_name = raw_input("Enter a .csv file name::  ")
        data = parse_csv(file_name)

        # run k_means
        num_centroids = raw_input("Enter the number of centroids:: ")
        if data.shape[1] == 2:
            path = raw_input("Enter the base name of the images (will be saved img0, img1, etc)> ")
            centroids = k_means(int(num_centroids), data, True, path)
        else:
            centroids = k_means(int(num_centroids), data, False, "")
        print_centroids(centroids)