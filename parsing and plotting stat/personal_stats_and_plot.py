import re
import csv
import pylab
from datetime import datetime

selected_nick_name = "PeX"

# dict {'map':points}
map_points = {}
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(fp)
    for row in reader:
        map_points[row[0]] = int(row[2])

# for deleted maps
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    for row in reader:
        if row[0] not in map_points.keys():
            map_points[row[0]] = 0

# date_points_map_dict[date] = [points_this_day, set(map1, map2, ...)]; where points this day are points for map1, .. , mapN which were done this day
time_counter = 0        # sum of time of all finishes
date_points_map_dict = {}
set_of_finished_maps = set()
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        other_info = (re.findall(',".*",', line))[0].split(',')
        nick = ','.join(other_info[1:-3])[1:-1]
        if nick == selected_nick_name:
            finished_map = re.split(',".*",', line)[0][1:-1]
            time = float(other_info[-3])
            time_counter += time
            if finished_map not in set_of_finished_maps:
                timestamp = datetime.date(datetime.strptime((other_info[-2])[1:-1], "%Y-%m-%d %H:%M:%S"))
                if timestamp not in date_points_map_dict.keys():
                    date_points_map_dict[timestamp] = [0, []]
                date_points_map_dict[timestamp][1].append(finished_map)
                set_of_finished_maps.add(finished_map)

map_counter = len(set_of_finished_maps)     # total count of different finished maps
total_points = 0
for key in date_points_map_dict.keys():
    for map in date_points_map_dict[key][1]:
        date_points_map_dict[key][0] += map_points[map]
    total_points += date_points_map_dict[key][0]

# list(el) because we need to transform tuple to list (to change, tuple is unchangeable)
top5_days_max_points = [list(el) for el in sorted(date_points_map_dict.items(), key=lambda x: x[1][0], reverse=True)[:5]]
print("Top 5 days with max points: ")
for item in top5_days_max_points:
    mp_list = []
    for mp in item[1][1]:
        mp_list.append(mp + " (" + str(map_points[mp]) + " p)")
    item[1][1] = mp_list
    print(item[0].strftime("%b %d %Y"), ',points:', item[1][0], ',maps:', item[1][1])

current_points = 0
for k in date_points_map_dict.keys():
    current_points += date_points_map_dict[k][0]
    date_points_map_dict[k][1] = current_points

# for key in date_points_map_dict.keys():
#     print(key, date_points_map_dict[key])

print('Points:', total_points)
print('Max points per day:', top5_days_max_points[0][1][0])
print('Count of different maps by', selected_nick_name, ':', map_counter)
print('Hours are sum of time of all finishes:', round(time_counter/60/60, 2))

# plot
fig = pylab.figure()

dates_max_points_list = [item[0] for item in top5_days_max_points]
daily_max_points_list = [item[1][0] for item in top5_days_max_points]
totally_max_points_list = [date_points_map_dict[dt][1] for dt in dates_max_points_list]

sp1 = pylab.subplot(2, 1, 1)
sp1.plot_date(date_points_map_dict.keys(), [date_points_map_dict[k][1] for k in date_points_map_dict.keys()], fmt=".")
sp1.plot_date(dates_max_points_list, totally_max_points_list, fmt='rx', label='max points per day')
sp1.legend()
sp1.set_title(selected_nick_name + " points")
pylab.ylabel('Total points')
pylab.grid()

sp2 = pylab.subplot(2, 1, 2)
sp2.plot_date(date_points_map_dict.keys(), [date_points_map_dict[k][0] for k in date_points_map_dict.keys()], fmt=".")
sp2.plot_date(dates_max_points_list, daily_max_points_list, fmt='rx')
pylab.ylabel('Points per day')
pylab.grid()

pylab.show()
