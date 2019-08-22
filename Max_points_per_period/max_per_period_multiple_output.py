import csv
import re
from datetime import datetime, timedelta
import time

# this is code with multiple output in meaning (check max_per_period.py to other way)
# the top could be very noisy by the records of the same
# players with the best results with a difference of several days
# like this:
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
    with open('output/multiple_results/' + file_name + '.csv', 'w', encoding='utf-8') as fw:
        fw.write("Rank,Nickname,Points,DateOfPeriodStart\n")
        for rank, (nick_name, points, date) in enumerate(data):
            fw.write('%d,%s,%d,%s\n' % (rank + 1, nick_name, points, date))


def own_max(arr):
    _max, _idx = arr[0], 0
    for i in range(1, len(arr)):
        if arr[i] > _max:
            _max, _idx = arr[i], i
    return _max, _idx


def paste_to_top(top_lst, nick_name_to_paste, max_value_to_paste, date_to_paste):
    len_top = len(top_lst)
    top_lst.append([nick_name_to_paste, max_value_to_paste, date_to_paste])
    top_lst = sorted(top_lst, key=lambda item: item[1], reverse=True)[:len_top]
    return top_lst, top_lst[-1][1]


def max_search_by_this_key(list_of_top_results, val_l, date_l, key_nick, min_of_top):
    max_res, max_idx = own_max(val_l)
    while max_res > min_of_top:
        list_of_top_results, min_of_top = paste_to_top(list_of_top_results, key_nick, max_res, date_l[max_idx])
        val_l.remove(max_res)
        del date_l[max_idx]
        if not val_l:
            break
        else:
            max_res, max_idx = own_max(val_l)
    return list_of_top_results, min_of_top


print("Start", time.clock())
map_points = get_dict_map_points()
nick_points = get_dict_points(map_points)
for k in nick_points.copy().keys():
    if nick_points[k] < 300:  # even top25 daily_map more than 300, so players with <300 can't be in these tops
        del nick_points[k]  # this line reduces number of players_in_process from 169k to almost 7k

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
            day_dict_key = datetime.date(datetime.strptime((other_info[-2])[1:-1], "%Y-%m-%d %H:%M:%S")).strftime(
                "%Y-%m-%d")

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

max_per_day = 25 * [["", 0, ""]]
# periods may overlap so next len of list is greater than max_per_day
max_per_week = 75 * [["", 0, ""]]
max_per_month = 75 * [["", 0, ""]]
max_per_year = 100 * [["", 0, ""]]

min_of_max_values_day = -1
min_of_max_values_week = -1
min_of_max_values_month = -1
min_of_max_values_year = -1

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

    max_per_day, min_of_max_values_day = max_search_by_this_key(max_per_day, max_per_period(val_list, 1), date_list, k,
                                                                min_of_max_values_day)
    max_per_week, min_of_max_values_week = max_search_by_this_key(max_per_week, max_per_period(val_list, 7), date_list,
                                                                  k, min_of_max_values_week)
    max_per_month, min_of_max_values_month = max_search_by_this_key(max_per_month, max_per_period(val_list, 30),
                                                                    date_list, k, min_of_max_values_month)
    max_per_year, min_of_max_values_year = max_search_by_this_key(max_per_year, max_per_period(val_list, 365),
                                                                  date_list, k, min_of_max_values_year)

print("Max-s per .. were found", time.clock())

write_output_file(max_per_day, "max_per_day")
write_output_file(max_per_week, "max_per_week")
write_output_file(max_per_month, "max_per_month")
write_output_file(max_per_year, "max_per_year")

print("End", time.clock())
