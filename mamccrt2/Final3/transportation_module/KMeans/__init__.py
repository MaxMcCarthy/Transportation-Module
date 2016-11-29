import numpy as np
import csv
import sys
from kmeans.ImageOutput import write_2D_picture, write_points
from transportation_module.Driver import Driver
import simplejson, urllib
from transportation_module.Athlete import Athlete


def init_centroids(path):
    '''
    initializes a group of new Drivers based on the
    .csv file found at path
    :param path: path of the driver .csv file
    :return:
    '''

    try:
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            driver_list = list(reader)
            print(driver_list)
    except:
        print("CANNOT OPEN DRIVER FILE")
        sys.exit(1)

    driver_arr = []
    id = 0
    for driver in driver_list:
        driver_arr.append(Driver(id, driver['Address'], int(driver['Size']), driver['Name']))
        id += 1

    return driver_arr


def init_distance_matrix(drivers, athletes):
    """
    will create an array of arrays... each inner array represents the
    athlete's distance from the driver with that ID
    :param drivers: array of driver Objects
    :param athletes: array of athlete Objects
    :return: 2D array of distances
    """

    distance_matrix = []
    url_stub = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"
    key = "&key=AIzaSyBfb5NKTnSfrLGqSqWsIbvDzxloiC2DRnU"
    for athlete in athletes:
        origins = "&origins=" + athlete.address.replace(" ", "+")
        destinations = "&destinations="
        for driver in drivers:
            #destinations += str(driver.car_location[0]) + "," + str(driver.car_location[1]) + "|"
            destinations += driver.meeting_address.replace(" ", "+") + "|"
        url = url_stub + origins + destinations + key
        distances = simplejson.load(urllib.urlopen(url))['rows'][0]['elements']
        dist_arr = []
        for distance in distances:
            dist_arr.append(distance['distance']['value'])
        distance_matrix.append(dist_arr)
    return distance_matrix


def add_row_to_data(drivers, athlete, data):
    """
    adds a line to the data array
    :param drivers: list of drivers
    :param athlete: athlete to create array for
    :param data: data matrix to append to
    :return: new matrix
    """

    url_stub = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"
    key = "&key=AIzaSyBfb5NKTnSfrLGqSqWsIbvDzxloiC2DRnU"
    origins = "&origins=" + athlete.address.replace(" ", "+")
    destinations = "&destinations="
    for driver in drivers:
        destinations += driver.meeting_address.replace(" ", "+") + "|"
    url = url_stub + origins + destinations + key
    distances = simplejson.load(urllib.urlopen(url))['rows'][0]['elements']
    dist_arr = []
    for distance in distances:
        dist_arr.append(distance['distance']['value'])
    data.append(dist_arr)
    return data


def assign_to_cars(drivers, athletes, data):
    """
    assigns athletes to cars given route data
    :param drivers: an array of drivers
    :param athletes: an array of athletes
    :param data: an array for each athlete giving the distance between
    each driver and the given athlete
    :return:
    """


    while len(athletes) > 0:
        athlete = athletes.pop()
        if athlete.id <= len(data):
            distance = data[athlete.id]
        info = get_car_assignments(drivers, distance)
        if info is not None:
            smallest_dist = info.keys()[0]
            smallest_driver = info.values()[0]
            make_assignments(athlete, smallest_dist, smallest_driver, athletes)

    '''for driver in drivers:
        print driver.driver_name
        print len(driver.points)
        for athlete in driver.points:
            print athlete.name

        print ""'''

    return drivers


def make_assignments(athlete, smallest_dist, smallest_driver, athlete_queue):
    """
    takes an athlete and adds it to the appropriate car; will remove another athlete
    and put it back on the queue if necessary
    :param athlete:
    :param smallest_dist:
    :param smallest_driver:
    :param athlete_queue:
    :return: nothin
    """

    if len(smallest_driver.points) >= smallest_driver.car_size:
        if should_replace_point(smallest_driver, smallest_dist):
            smallest_driver.points.sort(key=lambda x: x.distance)
            athlete_queue.append(smallest_driver.points[smallest_driver.car_size-1])
            removed_item = smallest_driver.points[smallest_driver.car_size-1]
            smallest_driver.points.remove(removed_item)
            smallest_driver.add_point(athlete, smallest_dist)

    if len(smallest_driver.points) < smallest_driver.car_size:
        smallest_driver.add_point(athlete, smallest_dist)


def get_car_assignments(drivers, distances):
    """
    takes an array of distances representing one athlete's distance from
    every driver and selects an appropriate driver
    :param drivers: an array of drivers
    :param distances: an array of distances for the given athlete
    :return: a dictionary with the key as the smallest distance and the
    value the driver
    """

    smallest_driver = None
    smallest_dist = 0
    for itr in range(0, len(distances)):
        distance = distances[itr]
        if (len(drivers[itr].points) < drivers[itr].car_size) or (should_replace_point(drivers[itr], distance) is True):
            if smallest_driver is None:
                smallest_driver = drivers[itr]
                smallest_dist = distance
            elif distance < smallest_dist:
                smallest_dist = distance
                smallest_driver = drivers[itr]

    if smallest_driver is not None:
        return {smallest_dist: smallest_driver}
    else:
        return None


def should_replace_point(driver, distance):
    '''
    determines whether an athlete should be removed from the
    car in favor of this new athlete
    :param driver:
    :param distance:
    :return:
    '''
    for itr in range(0, len(driver.points)):
        if driver.points[itr].distance > distance:
            return True
    return False


def update_drivers(driver_list):
    """
    update the address of all the drivers based on the athletes
    they are supposed to be picking up
    :param driver_list:
    :return:
    """

    for driver in driver_list:
        if len(driver.points) > 0:
            new_address = driver.driver_address
            athlete_lat = 0
            athlete_long = 0
            for athlete in driver.points:
                athlete_lat += athlete.position[0]
                athlete_long += athlete.position[1]
            athlete_lat /= long(len(driver.points))
            athlete_long /= long(len(driver.points))
            driver.car_location = [athlete_lat, athlete_long]
            coord_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
            key = "&key=AIzaSyBfb5NKTnSfrLGqSqWsIbvDzxloiC2DRnU"
            geo = simplejson.load(urllib.urlopen(coord_url + str(driver.car_location[0])
                                                 + "," + str(driver.car_location[1]) + key))
            driver.prev_address = driver.meeting_address
            driver.meeting_address = geo['results'][0]['formatted_address']
        else:
            driver.prev_address = driver.meeting_address


def check_centroid_array_eqality(old_centroids, new_centroids):
    '''
    takes in 2 arrays of centroids and checks equality determined by
    thier coordinates
    :param old_centroids: PYTHON array of centroids
    :param new_centroids: PYTHON array of centroids
    :return: true if the two are equal; false otherwise
    '''

    if len(old_centroids) != len(new_centroids):
        return False
    for centroid in range(0, len(old_centroids), 1):
        if not np.array_equal(old_centroids[centroid].coords, new_centroids[centroid].coords):
            return False
    return True


def check_drivers_are_set(drivers):
    """
    takes an array of driver and compares curr_address
    and meeting_address to see if they are the same
    :param drivers: an array of driver objects
    :return: true if the addresses are the same
    """

    for driver in drivers:
        if driver.prev_address != driver.meeting_address:
            return False
    return True


def check_efficiency(drivers, distances):
    """
    takes in the drivers after they have been assigned and see
    if a car can be reduced
    :param drivers: array of drivers
    :param distances: array of distances
    :return:
    """

    empty_seats = 0
    least_used_car = None
    len_athletes = 0
    for driver in drivers:
        if least_used_car is None:
            least_used_car = driver
        empty_seats += (driver.car_size - len(driver.points))
        if (driver.car_size - len(driver.points)) > (least_used_car.car_size - len(least_used_car.points)):
            least_used_car = driver
        driver.prev_address = ""
        len_athletes +=  len(driver.points)
    if (len(least_used_car.points) + 1) <= (empty_seats - (least_used_car.car_size - len(least_used_car.points))):
        print "Removing driver " + least_used_car.driver_name + " to improve efficiency..."
        remove_driver(drivers, least_used_car, distances)
        return True
    return False


def remove_driver(drivers, driver_to_remove, data):
    """
    takes in a list of drivers and a specific driver to convert
    into an athlete
    :param drivers: list of drivers
    :param driver_to_remove: driver being removed
    :param data: data array of distances
    :return:
    """

    athlete_arr = []
    for athlete in driver_to_remove.points:
        athlete_arr.append(athlete)
    new_athlete = Athlete(driver_to_remove.driver_name, driver_to_remove.driver_address, len(data))
    drivers.remove(driver_to_remove)
    athlete_arr.append(new_athlete)
    data = add_row_to_data(drivers, new_athlete, data)
    modified_k_means(drivers, athlete_arr, data)


def modified_k_means(drivers, athletes, distances):
    """

    :param drivers:
    :param athletes:
    :param distances:
    :return:
    """
    print "Running KMeans with added Athletes..."
    # assign athletes to cars
    assign_to_cars(drivers, athletes, distances)

    # update centroids based on new grouping
    update_drivers(drivers)

    # move centroids until old and new match
    while not check_drivers_are_set(drivers):

        # get distance matrix
        distances = init_distance_matrix(drivers, athletes)

        # assign athletes to cars
        assign_to_cars(drivers, athletes, distances)

        # update centroids based on new grouping
        update_drivers(drivers)


def k_means(drivers, athletes):
    '''
    clustering algorithm that places k centroids about some data. the centroids continually
    move around, assuming the location of the mean of all the points in their cluster. The algorithm
    is complete when the no data points and no centroids move
    :param drivers: array of drivers
    :param athletes: array of athletes
    '''

    print "Running KMeans..."

    distances = []
    # move centroids until old and new match
    while not check_drivers_are_set(drivers):

        #print "iteration number " + str(iterations)
        #iterations += 1

        # get distance matrix
        distances = init_distance_matrix(drivers, athletes)

        # assign athletes to cars
        assign_to_cars(drivers, athletes, distances)

        # update centroids based on new grouping
        update_drivers(drivers)

    while check_efficiency(drivers, init_distance_matrix(drivers, athletes)):
        print "Checking Efficiency of Cars..."
