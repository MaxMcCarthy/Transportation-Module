from flask import Flask, render_template, request, flash, redirect, url_for
import csv
from transportation_module.Interface import parse_csv_helper
from transportation_module.Athlete import Athlete
from transportation_module.KMeans import k_means

app = Flask(__name__)

athletes = None
drivers = None


@app.route('/', methods=["POST", "GET"])
def home_page():
    print "begin"
    return render_template('home_page.html', drivers=None)


@app.route('/csv', methods=['POST'])
def print_csv():
    """
    used to parse the CSV File; if the CSV File is bad,
    user is prompted to enter another one; else the csv
    file turns into a link that can be clicked?
    :return:
    """

    roster_path = request.form['file_name']
    roster = None
    try:
        with open(roster_path, 'r') as fil_des:
            reader = csv.DictReader(fil_des)
            roster = list(reader)
            arr = parse_csv_helper(roster)
            global athletes, drivers
            athletes = arr[0]
            drivers = arr[1]
            return render_template('csv.html', name=request.form['file_name'],
                                   drivers=drivers)
    except Exception as e:
        print e
        return render_template('bad_csv_file.html')


@app.route('/select_drivers', methods=['POST', 'GET'])
def select_drivers():
    global athletes, drivers
    print "was here, not now"
    if request.method == 'POST':
        print "is post"
        form = request.form['data']
        form = form[:-1]
        arr = form.split(',')
        adjust_drivers(arr)
        for thing in drivers:
            print thing.driver_name
    return render_template('home_page.html', drivers=drivers)


@app.route('/write_drivers')
def write_drivers():
    global athletes, drivers
    if drivers is not None:
        k_means(drivers, athletes)
        for athlete in athletes:
            print athlete.name
        print "drivers written"
        return render_template('drivers.html', drivers=drivers, athletes=athletes)
    else:
        return ""


@app.route('/message', methods=['POST'])
def display_message():
    message1 = request.form['msg1']
    message2 = request.form['msg2']
    return render_template('message.html', msg1=message1, msg2=message2)


@app.route('/<driver_name>')
def display_driver(driver_name):
    """
    given a driver name, display some information
    :param driver_name:
    :return:
    """

    global drivers
    driver_obj = None
    for driver in drivers:
        if driver.driver_name == driver_name:
            driver_obj = driver
            print driver_obj.driver_name
            break
    return render_template('driver_page.html', driver=driver_obj)


def adjust_drivers(selected_drivers):
    """

    :param selected_drivers: array of drivers to be used
    :return:
    """
    global athletes, drivers
    new_driver_list = []
    for person in drivers:
        driver_needed = False
        for name in selected_drivers:
            if name == person.driver_name:
                driver_needed = True
        if driver_needed is False:
            athletes.append(Athlete(person.driver_name, person.driver_address, len(athletes), person.dorm_code))
        else:
            new_driver_list.append(person)
    drivers = new_driver_list


if __name__ == '__main__':
    app.run()
