import numpy as np

from kmeans.Centroid import Centroid
from kmeans.ImageOutput import write_2D_picture, write_points


def init_centroids(k_centroids, data):
    '''
    initializes a group of new centroids based
    :param min_id: stating ID number
    :param max_id: ending ID number
    :param data: numpy.array of arrays holding data points
    :return:
    '''
    centroid_list = []
    min_arr = np.min(data, axis=0)
    max_arr = np.max(data, axis=0)
    med_arr = np.subtract(max_arr, min_arr)
    for ID in range(0, k_centroids, 1):
        rand_arr = np.multiply(np.random.rand(1, np.size(med_arr)), med_arr)
        centroid_list.append(Centroid(ID, np.add(rand_arr, min_arr).tolist()[0]))

    return centroid_list


def get_max_x_data(data):
    '''
    gets the maximum x value
    :param data: data set
    :return:
    '''
    max_arr = np.max(data, axis=0)
    print max_arr


def assign_centroid(centroids, data):
    '''
    loops through the data and the centroids to assign the data points to the
    closest centroid; must clear exisiting data first
    :param centroids: PYTHON ARRAY of centroids
    :param data: numpy.array of data points
    :return:
    '''

    for centroid in centroids:
        centroid.points = None
    for data_point in data:
        smallest_dist = 0
        smallest_dist_centroid = None
        for centroid in centroids:
            if smallest_dist_centroid is None:
                smallest_dist_centroid = centroid
                smallest_dist = np.sqrt(sum((centroid.coords - data_point) ** 2))
            elif np.sqrt(sum((centroid.coords - data_point) ** 2)) < smallest_dist:
                smallest_dist_centroid = centroid
                smallest_dist = np.sqrt(sum((centroid.coords - data_point) ** 2))
        smallest_dist_centroid.add_point(data_point)


def clear_centroid_points(centroids):
    '''
    loops through an array of centroids and clears the .points
    field so that assign_centroid doesn't continually place points
    into the field each iteration
    :param centroids: PYTHON ARRAY of centroids
    :return:
    '''

    for centroid in centroids:
        centroid.points = None


def use_all_centroids(centroids, data):
    '''
    it is mandatory that all centroids have at least one point; if they do not,
    they must be reinitialized and the data must be redistributed
    :param centroids: PYTHON ARRAY of centroids
    :param data: numpy.array of data points
    :return:
    '''

    min_arr = np.min(data, axis=0)
    max_arr = np.max(data, axis=0)
    med_arr = np.subtract(max_arr, min_arr)
    for centroid in centroids:
        while centroid.points is None:
            rand_arr = np.multiply(np.random.rand(1, np.size(med_arr)), med_arr)
            centroid.coords = np.array(np.add(rand_arr, min_arr).tolist()[0])
            assign_centroid(centroids, data)


def update_centroids(centroids):
    '''
    creates a new array of centroids which more closely fit the data
    centroids will be the mean of their current data points
    :param centroids: old PYTHON array of vectors
    :return: numpy.array of data points
    '''

    new_centroids = []
    for centroid in centroids:
        #print centroid.points
        mean_coords = np.mean(centroid.points, axis=0)
        new_centroid = Centroid(centroid.id, mean_coords)
        new_centroid.points = centroid.points
        new_centroids.append(new_centroid)
    return new_centroids


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


def k_means(k_centroids, data, write_picture, img_name):
    '''
    clustering algorithm that places k centroids about some data. the centroids continually
    move around, assuming the location of the mean of all the points in their cluster. The algorithm
    is complete when the no data points and no centroids move
    :param write_picture:
    :param img_name:
    :param k_centroids: number of centroids
    :param data: numpy.array of arrays holding data points
    :return: PYTHON array of centroids with associated points
    '''

    # set up optional image processing
    if data.shape[1] == 2 and write_picture is True:
        max_arr = np.max(data, axis=0)
        x_max = max_arr.item(0)
        y_max = max_arr.item(1)
        path = "../Images/" + img_name + str(0) + ".png"
        write_points(data, x_max, y_max, path)
        iterations = 1

    # initialize centroids
    curr_centroids = init_centroids(k_centroids, data)

    # create array of old centroids
    old_centroids = np.array([])

    # move centroids until old and new match
    while not check_centroid_array_eqality(old_centroids, curr_centroids):

        # assign points to centroids
        assign_centroid(curr_centroids, data)

        # make sure all centroids are in use
        use_all_centroids(curr_centroids, data)

        # assign old centroids to current
        old_centroids = curr_centroids

        # update centroids based on new grouping
        curr_centroids = update_centroids(curr_centroids)

        # write to image
        if data.shape[1] == 2 and write_picture is True:
            path = "../Images/" + img_name + str(iterations) + ".png"
            write_2D_picture(curr_centroids, x_max, y_max, path)
            iterations = iterations + 1

    # return final centroids; they will have the points nicely partitioned
    return curr_centroids

