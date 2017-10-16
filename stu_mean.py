#!usr/bin/python
'''
Shakil Rafi
Brian Leung
HW 10: Average
PD 7 SoftDev
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
        students[
        
