import requests
from lxml import html
from datetime import datetime, date
import matplotlib.dates
import numpy as np
import pylab

PLAYER_NAME = ':Ram'


def reading_data(tr, mode):
    maps_list_lxml = tr.xpath('//div[@id = "' + mode + '"]')[0]

    count_maps = len(maps_list_lxml.xpath('./div/table[@class = "spacey"]/tbody/tr'))
    parsed_data = []

    for i in range(count_maps):
        map_lxml = maps_list_lxml.xpath('./div/table[@class = "spacey"]/tbody/tr')[i]
        name_maps = map_lxml.xpath('./td')
        map_info = []
        for map in name_maps:
            map_info.append(map.text_content())
        parsed_data.append(map_info)
    return parsed_data


url = 'https://ddnet.tw/players/' + PLAYER_NAME + '/'
r = requests.get(url)

with open('test_data/test.html', 'w', encoding='utf-8') as handle:
    for block in r.iter_content(1024):
        handle.write(block.decode('utf-8'))

with open("test_data/test.html", 'r', encoding='utf-8') as fobj:
    xml = fobj.read()
tree = html.fromstring(xml)

data_read_novice = reading_data(tree, 'Novice')
data_read_moderate = reading_data(tree, 'Moderate')
data_read_brutal = reading_data(tree, 'Brutal')
data_read_insane = reading_data(tree, 'Insane')
data_read_dummy = reading_data(tree, 'Dummy')
data_read_ddmax = reading_data(tree, 'DDmaX')
data_read_oldschool = reading_data(tree, 'Oldschool')
data_read_solo = reading_data(tree, 'Solo')
data_read_race = reading_data(tree, 'Race')

data_read = data_read_novice + data_read_moderate + data_read_brutal + data_read_insane + data_read_dummy + data_read_ddmax + data_read_oldschool + data_read_solo + data_read_race
# data_read = data_read_novice

# extracting points and dates from data
name_of_maps = [m[0] for m in data_read]
points = [int(p[1]) for p in data_read]
dates = [q[6] for q in data_read]

# transformation data to correct format
dt = [datetime.strptime(d, "%Y-%m-%d %H:%M") for d in dates]
clear_date = [date(d.year, d.month, d.day) for d in dt]
date_num = matplotlib.dates.date2num(clear_date)

# sorting all data
ind = np.argsort(date_num)
sorted_points = [points[i] for i in ind]
sorted_dates = [clear_date[i] for i in ind]

# cumulation points
cumul_points = sorted_points
for i in range(1, len(cumul_points)):
    cumul_points[i] = cumul_points[i - 1] + cumul_points[i]

# deleting elements with the same date
ind_to_del = []
for i in range(1, len(sorted_dates)):
    if sorted_dates[i] == sorted_dates[i - 1]:
        ind_to_del.append(i - 1)
for i in range(len(ind_to_del))[::-1]:
    del sorted_dates[ind_to_del[i]]
    del cumul_points[ind_to_del[i]]

# some stats
points_per_day = [cumul_points[0]] + [cumul_points[i] - cumul_points[i - 1] for i in range(1, len(cumul_points))]

print("Total points: ", cumul_points[-1])
print("Max points per day: ", max(points_per_day))
print("Max points per day: ")
max_points_list = list(reversed(list(sorted(points_per_day))))[0:6]
ind_days_max_points = [i for i, e in enumerate(points_per_day) if e in max_points_list]

list_cumul_max_points = [cumul_points[i] for i in ind_days_max_points]
list_max_points = [points_per_day[i] for i in ind_days_max_points]
days_max_points = [sorted_dates[i] for i in ind_days_max_points]

list_of_days_with_max_points = []
for i in range(len(days_max_points)):
    list_single_day = [days_max_points[i].strftime("%b %d %Y"), str(list_max_points[i]) + ' points total']
    for j in range(len(clear_date)):
        if clear_date[j] == days_max_points[i]:
            list_single_day.append(name_of_maps[j] + ' (' + str(points[j]) + ' points)')
    list_of_days_with_max_points.append(list_single_day)

for i in range(len(list_of_days_with_max_points)):
    print(list_of_days_with_max_points[i])

# plot
fig = pylab.figure()

sp1 = pylab.subplot(2, 1, 1)
sp1.plot_date(sorted_dates, cumul_points, fmt=".")
sp1.plot_date(days_max_points, list_cumul_max_points, fmt='rx', label='max points per day')
sp1.legend()
sp1.set_title(PLAYER_NAME + " points")
pylab.ylabel('Total points')
pylab.grid()

sp2 = pylab.subplot(2, 1, 2)
sp2.plot_date(sorted_dates, points_per_day, fmt=".")
sp2.plot_date(days_max_points, list_max_points, fmt='rx')
pylab.ylabel('Points per day')
pylab.grid()

pylab.show()
