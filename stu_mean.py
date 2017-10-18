#! /usr/bin/env python

# Team NoPJs Shakil Rafi and Brian Leung
# HW10: Average
# SoftDev pd7
# 2017-10-16

import sqlite3
import csv
f = 'discobandit.db'
db = sqlite3.connect(f) 
c = db.cursor()

def make_courses():
    command = 'CREATE TABLE courses(code TEXT, mark INTEGER, id INTEGER)'
    c.execute(command) # create table
    courses = open('courses.csv', 'r')
    reader = csv.DictReader(courses)
    for row in reader:
        command = 'INSERT INTO courses VALUES ("%s", %s, %s)' % (row['code'], row['mark'], row['id'])
        c.execute(command) # add given row to table

def make_peeps():
    command = 'CREATE TABLE peeps(name TEXT, age INTEGER, id INTEGER PRIMARY KEY)'
    c.execute(command)
    peeps = open('peeps.csv', 'r')
    reader = csv.DictReader(peeps)
    for row in reader:
        command = 'INSERT INTO peeps VALUES ("%s", %s, %s)' % (row['name'], row['age'], row['id'])
        c.execute(command)

def make_peeps_avg():
    create_command = "CREATE TABLE peeps_avg(id INTEGER, avg INTEGER)"
    select_command = '''SELECT name, peeps.id, mark
    FROM peeps, courses
    WHERE peeps.id = courses.id;'''
    c.execute(create_command)
    db_result = c.execute(select_command)
    students = {} # to hold each student's average
    for student in db_result:
        name = student[0]
        if name in students:
            students[name]['total'] += student[2] # add to total for dividing later
            students[name]['num_classes'] += 1
        else:
            students[name] = {} # initialize sub-dict for student
            students[name]['total'] = student[2]
            students[name]['num_classes'] = 1
            students[name]['id'] = student[1]    
    for student in students.keys():
        total = students[student]['total']
        num_classes = students[student]['num_classes']
        gpa = total/num_classes
        stu_id = students[student]['id']
        command = "INSERT INTO peeps_avg VALUES(%d, %d)" % (stu_id, gpa)
        c.execute(command)
    return students

def update_peeps_avg():
    select_command = '''SELECT name, peeps.id, mark
    FROM peeps, courses
    WHERE peeps.id = courses.id;'''
    db_result = c.execute(select_command)
    students = {} # to hold each student's average
    for student in db_result:
        name = student[0]
        if name in students:
            students[name]['total'] += int(student[2]) # add to total for dividing later
            students[name]['num_classes'] += 1
        else:
            students[name] = {} # initialize sub-dict for student
            students[name]['total'] = int(student[2])
            students[name]['num_classes'] = 1
            students[name]['id'] = student[1]    
    for student in students.keys():
        total = students[student]['total']
        num_classes = students[student]['num_classes']
        gpa = total/num_classes
        stu_id = students[student]['id']
        command = "UPDATE peeps_avg SET avg = %d WHERE id = %d" % (gpa, stu_id)
        c.execute(command)
    return students
'''
def update_courses():
    f = open('courses.csv', 'r')
    reader = csv.DictReader(f)
    for row in reader:
        command = 'SELECT * FROM courses WHERE code = "%s" AND id = %s AND mark = %s' % (row['code'], row['id'], row['mark'])
        result = c.execute(command)
        if result.rowcount < 1:
            for r in result:
                print row, r
            command = 'INSERT INTO courses VALUES("%s", %s, %s)' % (row['code'], row['mark'], row['id'])
            c.execute(command)
'''
def update_courses():
	f = 'discobandit.db'
	csvfile = open("courses.csv","rb")
	reader = csv.DictReader(csvfile)
	command = 'DROP TABLE courses'
	c.execute(command)
	command = 'CREATE TABLE courses(code TEXT, mark INTEGER, id INTEGER)'
	c.execute(command)
	for row in reader:
		command = 'INSERT INTO courses VALUES("%s",%s,%s)' % (row['code'], row['mark'], row['id'])
		c.execute(command)
	return "Done"

def print_avgs():
    command = '''SELECT name, peeps.id, avg
    FROM peeps, peeps_avg
    WHERE peeps.id = peeps_avg.id'''
    students = c.execute(command)
    print 'Name, id, gpa'
    for student in students:
        name = student[0]
        stu_id = student[1]
        avg = student[2]
        print '%s, %s, %d' % (name, stu_id, avg)

try:
    make_courses()
    make_peeps()
    make_peeps_avg()
except:
    update_courses()
    update_peeps_avg()

print_avgs()

db.commit() #save changes
db.close()
