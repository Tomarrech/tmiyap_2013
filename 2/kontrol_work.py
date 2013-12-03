__author__ = 'tomar_000'
from datetime import datetime, timedelta
import random
import os
#task1
date_list = []

dt = datetime.now()
for i in range(1000):
    date_list.append(dt + timedelta(random.randint(-500, 500)))

#task2
new_date_list = []
max_date_value = dt + timedelta(400)
min_date_value = dt + timedelta(-400)

for date in date_list:
    if (date > min_date_value) & (date < max_date_value):
        new_date_list.append(date)

#task3
list_even_months = []
for date in new_date_list:
    if not date.month % 2:
        list_even_months.append(date)

#task4
print os.getcwd()


def week_():
    w = dt.weekday()
    if w == 0: return 'Monday '
    elif w == 1: return 'Tuesday'
    elif w == 2: return 'Wednesday'
    elif w == 3: return 'Thursday'
    elif w == 4: return 'Friday'
    elif w == 5: return'Saturday'
    elif w == 6: return 'Sunday'

if not os.path.exists(os.getcwd()+'\\'+week_()):
    os.mkdir(week_())
else:
    pass

#task5
os.chdir(os.getcwd()+'\\'+week_())
print os.getcwd()

f = open('dates.txt', 'w')

for date in list_even_months:
    if date.year == 2012: f.write(str(date.day) + '.' + str(date.month) + '.' + str(date.year) + ' - last year; ')
    elif date.year == 2013: f.write(str(date.day) + '.' + str(date.month) + '.' + str(date.year) + ' - this year; ')
    elif date.year == 2014: f.write(str(date.day) + '.' + str(date.month) + '.' + str(date.year) + ' - next year; ')

f.close()

#task6
import re
dates_from_file = []
for d in re.findall(ur'(?:0[1-9]|[12][0-9]|3[01])[\.](?:0[1-9]|1[012])[\.]\d\d\d\d', open('dates.txt', 'r').read()):
    dates_from_file.append(d)

#task7
dt_date = []
for date in dates_from_file:
    dt_date.append(datetime.strptime(date, "%d.%m.%Y"))