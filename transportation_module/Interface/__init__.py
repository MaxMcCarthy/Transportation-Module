# build URL https://www.google.com/maps/dir/40.1096994,-88.2272659/40.1091848,-88.2409264/ end goes last

import csv
import sys
import simplejson
from transportation_module.Athlete import Athlete
from transportation_module.Driver import Driver
from transportation_module.KMeans import *
from kmeans.Interface import get_factors


def init_athletes(athlete_path):
    """
    given a path, create a an array of rowers
    :param athlete_path: path to .csv file
    :return: an array of athlete objects
    """
    try:
        with open(athlete_path, 'r') as fil_des:
            reader = csv.DictReader(fil_des)
            rower_list = list(reader)

        athletes = []
        count = 0
        for rower in rower_list:
            athletes.append(Athlete(rower['Name'], rower['Address'], count))
            count += 1
    except:
        print "could not open file"
        sys.exit(1)
    return athletes


def parse_csv():
    """
    give a file name of a roster in a csv file, parse it into athletes and drivers
    :return: a 2 element array, the first is the athletes and the second is the drivers
    """

    roster = None
    roster_path = raw_input("Please enter a .csv file: ")
    while roster is None:
        try:
            with open(roster_path, 'r') as fil_des:
                reader = csv.DictReader(fil_des)
                roster = list(reader)
        except:
            print "UNABLE TO OPEN FILE"
            roster_path = raw_input("Please enter a new .csv file: ")

    return parse_csv_helper(roster_path, roster)


def parse_csv_helper(roster):
    """
    give a known to be correct roster list object, this parses the athletes and drivers
    and returns an array
    :param roster: a list object parsed from csv
    :return: 2D array [athletes, drivers]
    """

    athletes = []
    drivers = []

    print "Parsing .csv ..."
    athlete_count = 0
    driver_count = 0
    for person in roster:
        if person['Is Driver'] == 'yes':
            drivers.append(Driver(driver_count, person['Address'], int(person['Num Seats']), person['Name']))
            driver_count += 1
        elif person['Is Driver'] == 'no':
            athletes.append(Athlete(person['Name'], person['Address'], athlete_count))
            athlete_count += 1

    return [athletes, drivers]


def pick_drivers(driver_arr, athletes):
    """
    takes in list of available drivers and prompts the user to pick
    which ones need to drive
    :param driver_arr: available drivers
    :param athletes: athlete array
    :return: a 2 element array, [athletes, drivers]
    """

    new_driver_list = []
    print "Select your drivers by Driver ID"
    for person in driver_arr:
        print str(person.id) + ": " + str(person.driver_name)
    driver_ids = get_factors(len(driver_arr), "Driver ID")
    print "Creating Drivers..."
    for person in driver_arr:
        driver_needed = False
        for curr_id in driver_ids:
            if curr_id == person.id:
                driver_needed = True
        if driver_needed is False:
            athletes.append(Athlete(person.driver_name, person.driver_address, len(athletes)))
        else:
            new_driver_list.append(person)
    return [athletes, new_driver_list]


def print_stats(drivers):
    """
    print out distance and time to meeting spot for each driver
    and athlete
    :param drivers: array of driver Objects
    :return: nothing
    """

    url_stub = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"
    key = "&key=AIzaSyBOdzdXLqA_jUXMPiZ81HrCwv5cgTO_CbA"
    walking = "&mode=walking"
    for driver in drivers:
        print "DRIVER: " + driver.driver_name
        print "MEETING SPOT: " + str(driver.car_location[0]) + "," + str(driver.car_location[1])
        origin_driver = "&origins=" + driver.driver_address.replace(" ", "+")
        destination_driver = "&destinations=" + str(driver.car_location[0]) + "," + str(driver.car_location[1])
        url = url_stub + origin_driver + destination_driver + key
        distance = simplejson.load(urllib.urlopen(url))['rows'][0]['elements'][0]
        print "Distance to meeting spot: " + distance['distance']['text']
        print "Estimated time to meeting spot: " + distance['duration']['text']
        print ""

        for athlete in driver.points:
            origin_athlete = "&origins=" + athlete.address.replace(" ", "+")
            url = url_stub + origin_athlete + destination_driver + walking + key
            distance = simplejson.load(urllib.urlopen(url))['rows'][0]['elements'][0]
            print "ATHLETE: " + athlete.name
            print "Distance to meeting spot: " + distance['distance']['text']
            print "Estimated time to meeting spot: " + distance['duration']['text']
            print ""

        print ""


if __name__ == '__main__':
    """
    main
    """
    roster_arr = parse_csv()
    roster_arr = pick_drivers(roster_arr[1], roster_arr[0])
    #for driver in roster_arr[1]:
        #print driver.car_size
    #assign_to_cars(roster_arr[1], roster_arr[0], init_distance_matrix(roster_arr[1], roster_arr[0]))
    k_means(roster_arr[1], roster_arr[0])
    #print_stats(roster_arr[1], roster_arr[0])
    #while check_efficiency(roster_arr[1]):
        #print "Making Assignments more efficient... "
    '''for driver in roster_arr[1]:
        print driver.driver_name
        for point in driver.points:
            print point.name
        print ""'''
    print_stats(roster_arr[1])