from flask import Flask, render_template, request, flash, redirect, url_for
from mongoalchemy.fields import *
from flask_mongoalchemy import *
from mongoalchemy.session import Session
from flask_pymongo import PyMongo
import csv
from transportation_module.Interface import parse_csv_helper
from transportation_module.Athlete import Athlete
from transportation_module.KMeans import k_means

app = Flask(__name__)
session = Session.connect('mydb')


class Team(Document):
    name = StringField()
    user_name = StringField()
    password = StringField()


class Student(Document):
    name = StringField()
    has_car = IntField()
    num_seats = IntField()
    address = StringField()
    team = DocumentField(Team)


athletes = None
drivers = None


@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template('log_in.html')


# new user HTML
@app.route('/new_user', methods=['POST', 'GET'])
def new_user():
    return render_template('new_user.html')


# creates new user in DB
@app.route('/create_new_user', methods=['POST'])
def create_new_user():
    global session
    user_name = request.form['username']
    password = request.form['new-pass']
    team_name = request.form['team']

    user = Team(user_name=user_name, password=password, name=team_name)

    session.save(user)

    return redirect(url_for('manage_team', team_name=team_name))


# new student HTML
@app.route('/<team_name>/add_student', methods=['POST','GET'])
def add_student(team_name):
    print('here')
    return render_template('create_student.html', team_name=team_name)


# manages the students on a team
@app.route('/<team_name>/manage', methods=['POST', 'GET'])
def manage_team(team_name):
    global session
    print("team name")
    print(team_name)
    athletes = session.query(Student).filter(Student.team.name == team_name)
    return render_template('manage_athletes.html', athletes=athletes, team_name=team_name)


# creates new student in DB
@app.route('/<team_name>/submit_student', methods=['POST', 'GET'])
def submit_student(team_name):
    global session
    student_name = request.form['name']
    student_address = str(request.form['address'])
    student_seats = int(request.form['num_seats'])
    if request.form['has_car'] == 'on':
        student_has_car = 1
    else:
        student_has_car = 0
    team = session.query(Team).filter(Team.name == team_name).first()
    print(team)
    new_student = Student(name=student_name, address=student_address, has_car=student_has_car, num_seats=student_seats, team=team)
    session.save(new_student)
    print("start")
    print(session.query(Student).filter(Student.mongo_id == new_student.mongo_id).one().name)
    print("end")
    return redirect(url_for('manage_team', team_name=team_name))


# updates a student
@app.route('/<team_name>/update_student/<doc_id>', methods=['POST'])
def update_student(team_name, doc_id):
    global session
    student = session.query(Student).filter(Student.mongo_id == doc_id).one()


# deletes a student
@app.route('/<team_name>/delete_student/<doc_id>', methods=['POST', 'GET'])
def delete_student(team_name, doc_id):
    global session
    session.remove_query(Student).filter(Student.mongo_id == doc_id).execute()
    return redirect(url_for('manage_team', team_name=team_name))


@app.route('/', methods=["POST", "GET"])
def home_page():
    print "begin"
    # session = Session.connect('library')
    return render_template('log_in.html')
    # return render_template('home_page.html', drivers=None)


# @app.route('/csv', methods=['POST'])
# def print_csv():
#     """
#     used to parse the CSV File; if the CSV File is bad,
#     user is prompted to enter another one; else the csv
#     file turns into a link that can be clicked?
#     :return:
#     """
#
#     roster_path = request.form['file_name']
#     roster = None
#     try:
#         with open(roster_path, 'r') as fil_des:
#             reader = csv.DictReader(fil_des)
#             roster = list(reader)
#             arr = parse_csv_helper(roster)
#             global athletes, drivers
#             athletes = arr[0]
#             drivers = arr[1]
#             return render_template('csv.html', name=request.form['file_name'],
#                                    drivers=drivers)
#     except Exception as e:
#         print e
#         return render_template('bad_csv_file.html')
#
#
# @app.route('/select_drivers', methods=['POST', 'GET'])
# def select_drivers():
#     global athletes, drivers
#     print "was here, not now"
#     if request.method == 'POST':
#         print "is post"
#         form = request.form['data']
#         form = form[:-1]
#         arr = form.split(',')
#         adjust_drivers(arr)
#         for thing in drivers:
#             print thing.driver_name
#     return render_template('home_page.html', drivers=drivers)
#
#
# @app.route('/write_drivers')
# def write_drivers():
#     global athletes, drivers
#     if drivers is not None:
#         k_means(drivers, athletes)
#         for athlete in athletes:
#             print athlete.name
#         print "drivers written"
#         return render_template('drivers.html', drivers=drivers, athletes=athletes)
#     else:
#         return ""
#
#
# @app.route('/message', methods=['POST'])
# def display_message():
#     message1 = request.form['msg1']
#     message2 = request.form['msg2']
#     return render_template('message.html', msg1=message1, msg2=message2)
#
#
# @app.route('/<driver_name>')
# def display_driver(driver_name):
#     """
#     given a driver name, display some information
#     :param driver_name:
#     :return:
#     """
#
#     global drivers
#     driver_obj = None
#     for driver in drivers:
#         if driver.driver_name == driver_name:
#             driver_obj = driver
#             print driver_obj.driver_name
#             break
#     return render_template('driver_page.html', driver=driver_obj)
#
#
# def adjust_drivers(selected_drivers):
#     """
#
#     :param selected_drivers: array of drivers to be used
#     :return:
#     """
#     global athletes, drivers
#     new_driver_list = []
#     for person in drivers:
#         driver_needed = False
#         for name in selected_drivers:
#             if name == person.driver_name:
#                 driver_needed = True
#         if driver_needed is False:
#             athletes.append(Athlete(person.driver_name, person.driver_address, len(athletes), person.dorm_code))
#         else:
#             new_driver_list.append(person)
#     drivers = new_driver_list


if __name__ == '__main__':
    app.run()
