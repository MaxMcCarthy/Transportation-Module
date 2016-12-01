from PIL import Image, ImageDraw


def write_2D_picture(centroids, max_x, max_y, img_name):
    '''
    takes list of centroids and writes them out to PNG
    :param centroids: PYTHON array of centroids
    :param max_x: maximum x value to include
    :param max_y: maximum y value to include
    :param img_name: location to write the image file
    :return:
    '''

    cols = [
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (0, 255, 255),
        (255, 0, 255),
        (255, 255, 0),
        (155, 155, 155),
        (255, 155, 255),
        (155, 0, 255),
        (105, 255, 255),
        (0, 0, 0)
    ]

    scale_factor = max(max_x, max_y)
    img_size = 502
    image = Image.new("RGB", (img_size, img_size), 'white')

    for centroid in centroids:
        if centroid.points is not None:
            for point in centroid.points:
                write_pixel(cols[centroid.id], img_size, point, image, scale_factor)
        draw_centroid(scale(centroid.coords.item(0), scale_factor), scale(centroid.coords.item(1), scale_factor), image, img_size)
        draw_perimeter(centroid, image, cols[centroid.id], scale_factor)

    image.save(img_name)


def write_pixel(color, img_size, location, image, scale_factor):
    """
    writes a pixel of varying size depending on the size
    of the overall image
    :param color: color of the pixel
    :param img_size: size of the image
    :param location: point to be made into a pixel
    :param image: the image to color on
    :param scale_factor: the number to pass to the scaling function
    :return:
    """
    x_location = scale(location.item(0), scale_factor)
    y_location = scale(location.item(1), scale_factor)

    img_cont = int(img_size/100)
    if img_cont == 0:
        image.putpixel((x_location, y_location), color)
    else:
        write_to_range(x_location-img_cont, x_location+img_cont, y_location-img_cont, y_location+img_cont, color, image, img_size)


def write_to_range(start_x, end_x, start_y, end_y, color, image, img_size):
    """
    loops through the given range coloring the pixels
    :param start_x: start x location
    :param end_x: end x location
    :param start_y: start y location
    :param end_y: end y locaiton
    :param color: color of the image
    :param image: image to color
    :param img_size: the size of the image
    :return:
    """

    for curr_x in range(start_x, end_x, 1):
        for curr_y in range(start_y, end_y, 1):
            if curr_x > 0 and curr_y > 0:
                if curr_x < img_size and curr_y < img_size:
                    image.putpixel((curr_x, curr_y), color)


def draw_centroid(start_x, start_y, image, img_size):
    """
    draws an X over the center of the centroid
    :param start_x: x location of the center of the x
    :param start_y: y location of the center of the x
    :param image: image to draw on
    :param img_size: dimension of the image
    :return:
    """

    range_value = int(img_size/100)
    if range_value == 0:
        range_value = 1

    image.putpixel((start_x, start_y), (0,0,0))

    for inc in range(0, range_value, 1):
        if (start_x + inc) < img_size and (start_y + inc) < img_size:
            image.putpixel((start_x+inc, start_y+inc), (0,0,0))
        if start_x + inc < img_size and start_y - inc >= 0:
            image.putpixel((start_x+inc, start_y-inc), (0,0,0))
        if start_x - inc >= 0 and start_y + inc < img_size:
            image.putpixel((start_x-inc, start_y+inc), (0,0,0))
        if start_x- inc >= 0 and start_y - inc >= 0:
            image.putpixel((start_x-inc, start_y-inc), (0,0,0))

    draw = ImageDraw.Draw(image)
    draw.line(((start_x + range_value, start_y + range_value), (start_x - range_value, start_y + range_value)), fill=(0,0,0))
    draw.line(((start_x + range_value, start_y + range_value), (start_x + range_value, start_y - range_value)), fill=(0,0,0))
    draw.line(((start_x - range_value, start_y + range_value), (start_x - range_value, start_y - range_value)), fill=(0,0,0))
    draw.line(((start_x - range_value, start_y - range_value), (start_x + range_value, start_y - range_value)), fill=(0,0,0))


def write_points(data, max_x, max_y, img_name):
    '''
    takes a set of data and plots all of the points
    :param data: data to plot
    :param max_x: maximum x value to include
    :param max_y: maximum y value to include
    :param img_name: location to write the image file
    :return:
    '''

    cols = [
        (25, 25, 25)
    ]
    scale_factor = max(max_x, max_y)
    img_size = 502
    image = Image.new("RGB", (img_size, img_size), 'white')

    for data_points in data:
        img_cont = int(img_size/100)
        x_location = scale(data_points.item(0), scale_factor)
        y_location = scale(data_points.item(1), scale_factor)
        if img_cont == 0:
            image.putpixel((x_location, y_location), cols[0])
        else:
            write_to_range(x_location-img_cont, x_location+img_cont, y_location-img_cont, y_location+img_cont, cols[0], image, img_size)

    image.save(img_name)


def draw_perimeter(centroid, image, color, scale_factor):
    """
    draws an ellipse around the center of the points
    :param centroid: centroid that is the center
    :param image: image to draw on
    :param color: color of the ellipse
    :param scale_factor: scale the point
    :return:
    """

    center_x = scale(centroid.coords.item(0), scale_factor)
    center_y = scale(centroid.coords.item(1), scale_factor)

    max_x = 0
    max_y = 0
    for point in centroid.points:
        scaled_x = scale(point.item(0), scale_factor)
        scaled_y = scale(point.item(1), scale_factor)
        if abs(scaled_x - center_x) > max_x:
            max_x = abs(scaled_x - center_x)
        if abs(scale(point.item(1), scale_factor) - center_y) > max_y:
            max_y = abs(scaled_y - center_y)

    bbox = (center_x - max_x, center_y - max_y, center_x + max_x, center_y + max_y)
    draw = ImageDraw.Draw(image)
    draw.ellipse(bbox, outline=color)
    del draw


def scale(point, max_size):
    """

    :param point:
    :param max_size:
    :return:
    """

    scale_factor = 500/float(max_size)
    return int(point*float(scale_factor))


