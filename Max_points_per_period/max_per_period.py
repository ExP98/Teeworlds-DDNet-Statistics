import csv
import re
from datetime import datetime, timedelta
import time

# works with the assumption of 1 player - 1 record (check max_per_period_multiple_output.py to other way)
# otherwise the top will be very noisy by the records of the same
# players with the best results with a difference of several days
# avoiding this:
# Rank,Nickname,Points,DateOfPeriodStart
# 1,?#@,1518,2019-01-30
# 2,?#@,1465,2019-02-01
# 3,Ninjed,1319,2016-05-28
# 4,Ninjed,1298,2016-05-27
# 5,Brokecdx-,1224,2018-12-12
# 6,Brokecdx-,1217,2018-12-14


def get_dict_map_points():
    mp_pts = {}
    with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=',')
        next(fp)
        for row in reader:
            mp_pts[row[0]] = int(row[2])
    # for deleted maps
    with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=',')
        for row in reader:
            if row[0] not in mp_pts.keys():
                mp_pts[row[0]] = 0
    return mp_pts


def get_dict_points(dict_map_points):
    nck_pts_dict = {}
    with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f_get_pts:
        next(f_get_pts)  # skipping header
        for line_get_pts in f_get_pts:
            mp = re.split(',".*",', line_get_pts)[0][1:-1]
            pl_nick = ','.join((re.findall(',".*",', line_get_pts))[0].split(',')[1:-3])[1:-1]
            if pl_nick not in nck_pts_dict.keys():
                nck_pts_dict[pl_nick] = set()
            else:
                nck_pts_dict[pl_nick].add(mp)
    for key in nck_pts_dict.keys():
        t_pts = 0
        for mp in nck_pts_dict[key]:
            t_pts += dict_map_points[mp]
        nck_pts_dict[key] = t_pts
    return nck_pts_dict


def max_per_period(input_data, window_size):
    mpp = []
    if len(input_data) < window_size:
        mpp = [sum(input_data)]
    for ii in range(len(input_data) - window_size + 1):
        mpp.append(sum(input_data[ii:window_size + ii]))
    return mpp


def write_output_file(data, file_name):
    sort_arr = sorted(data, key=lambda x: x[1], reverse=True)[:100]
    with open('output/single_results/' + file_name + '.csv', 'w', encoding='utf-8') as fw:
        fw.write("Rank,Nickname,Points,DateOfPeriodStart\n")
        for rank, (nick_name, points, date) in enumerate(sort_arr):
            fw.write('%d,%s,%d,%s\n' % (rank + 1, nick_name, points, date))


def my_max(arr):
    _max, _idx = arr[0], 0
    for i in range(1, len(arr)):
        if arr[i] > _max:
            _max, _idx = arr[i], i
    return _max, _idx


print("Start", time.clock())
map_points = get_dict_map_points()
nick_points = get_dict_points(map_points)
for k in nick_points.copy().keys():
    if nick_points[k] < 300:    # even top25 daily_map more than 300, so players with <300 can't be in these tops
        del nick_points[k]      # this line reduces number of players_in_process from 169k to almost 7k

print("Map and nick_pts dict", time.clock())

# nick_maps_dict[nick] = set(finished_maps)
nick_maps_dict = dict()
# data_dict = {nick1: {day1: set(map1, map2, ..), day2: set(map3, map4, ..)}, nick2: {}}
data_dict = dict()
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map = re.split(',".*",', line)[0][1:-1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        nick = ','.join(other_info[1:-3])[1:-1]
        if nick in nick_points.keys():
            day_dict_key = datetime.date(datetime.strptime((other_info[-2])[1:-1], "%Y-%m-%d %H:%M:%S")).strftime("%Y-%m-%d")

            if nick not in nick_maps_dict.keys():
                nick_maps_dict[nick] = {map}
                data_dict[nick] = dict()
                data_dict[nick][day_dict_key] = {map}
            else:
                if map not in nick_maps_dict[nick]:
                    nick_maps_dict[nick].add(map)
                    if day_dict_key not in data_dict[nick].keys():
                        data_dict[nick][day_dict_key] = {map}
                    else:
                        data_dict[nick][day_dict_key].add(map)

nick_maps_dict.clear()

for nck_nm in data_dict.keys():
    for c_day in data_dict[nck_nm].keys():
        c_pts = 0
        for maps_this_day in data_dict[nck_nm][c_day]:
            c_pts += map_points[maps_this_day]
        data_dict[nck_nm][c_day] = c_pts

print("data_dict", time.clock())

max_per_day = []
max_per_week = []
max_per_month = []
max_per_year = []

for k in data_dict.keys():
    curr_date = datetime.strptime(list(data_dict[k].items())[0][0], "%Y-%m-%d")
    last_dt = datetime.strptime(list(data_dict[k].items())[-1][0], "%Y-%m-%d")
    date_list = []
    val_list = []

    while curr_date <= last_dt:
        c_date_str = curr_date.strftime("%Y-%m-%d")
        date_list.append(c_date_str)
        if c_date_str in data_dict[k].keys():
            val_list.append(data_dict[k][c_date_str])
        else:
            val_list.append(0)
        curr_date += timedelta(days=1)

    max_value, max_index = my_max(max_per_period(val_list, 1))
    max_per_day.append([k, max_value, date_list[max_index]])

    max_value, max_index = my_max(max_per_period(val_list, 7))
    max_per_week.append([k, max_value, date_list[max_index]])

    max_value, max_index = my_max(max_per_period(val_list, 30))
    max_per_month.append([k, max_value, date_list[max_index]])

    max_value, max_index = my_max(max_per_period(val_list, 365))
    max_per_year.append([k, max_value, date_list[max_index]])

print("Max-s per .. were found", time.clock())

write_output_file(max_per_day, "max_per_day")
write_output_file(max_per_week, "max_per_week")
write_output_file(max_per_month, "max_per_month")
write_output_file(max_per_year, "max_per_year")

print("End", time.clock())
