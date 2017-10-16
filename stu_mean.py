#! /usr/bin/env python

'''
Team NoPJs
Shakil Rafi
Brian Leung
HW 10: Average
PD 7 SoftDev
2017-10-16
'''

import sqlite3

f = 'discobandit.db'
db = sqlite3.connect(f)
c = db.cursor()
q = '''SELECT name, peeps.id, mark
FROM peeps, courses
WHERE peeps.id = courses.id;'''
foo  = c.execute(q)

students = {}
for bar in foo:
    name = bar[0]
    if name in students:
        students[name]['total'] += bar[2]
        students[name]['num_classes'] += 1
    else:
        students[name] = {}
        students[name]['total'] = bar[2]
        students[name]['num_classes'] = 1
        students[name]['id'] = bar[1]

print 'Name, id, gpa'
for student in students.keys():
    total = students[student]['total']
    num_classes = students[student]['num_classes']
    gpa = total/num_classes
    stu_id = students[student]['id']
    print '%s, %s, %d' % (student, stu_id, gpa)
