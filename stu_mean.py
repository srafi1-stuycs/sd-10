#! /usr/bin/env python

# Team NoPJs Shakil Rafi and Brian Leung
# HW10: Average
# SoftDev pd7
# 2017-10-16

import sqlite3

f = 'discobandit.db'
db = sqlite3.connect(f) # open db
c = db.cursor()
q = '''SELECT name, peeps.id, mark
FROM peeps, courses
WHERE peeps.id = courses.id;'''
db_result  = c.execute(q) # retrieve all names, ids, and grades

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

print 'Name, id, gpa'
for student in students.keys():
    total = students[student]['total']
    num_classes = students[student]['num_classes']
    gpa = total/num_classes
    stu_id = students[student]['id']
    print '%s, %s, %d' % (student, stu_id, gpa)
