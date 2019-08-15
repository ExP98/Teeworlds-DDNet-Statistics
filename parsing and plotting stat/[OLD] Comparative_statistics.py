import requests
from lxml import html
from datetime import datetime, date
import matplotlib.dates
import numpy as np
import pylab

nickname1 = 'PeX'
nickname2 = 'ad'
nickname3 = 'Axaris'
nickname4 = 'Fexa'


def reading_data(tr, mode):
    maps_list_lxml = tr.xpath('//div[@id = "' + mode + '"]')[0]

    count_maps = len(maps_list_lxml.xpath('./div/table[@class = "spacey"]/tbody/tr'))
    data_read = []

    for i in range(count_maps):
        map_lxml = maps_list_lxml.xpath('./div/table[@class = "spacey"]/tbody/tr')[i]
        name_maps = map_lxml.xpath('./td')
        map_info = []
        for map in name_maps:
            map_info.append(map.text_content())
        data_read.append(map_info)
    return data_read


def player_stats_data(name):
    url = 'https://ddnet.tw/players/' + name + '/'
    r = requests.get(url)

    with open('output_data/test.html', 'w', encoding='utf-8') as handle:
        for block in r.iter_content(1024):
            handle.write(block.decode('utf-8'))

    with open("output_data/test.html", 'r', encoding='utf-8') as fobj:
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
    sorted_dates_for_plotting = [clear_date[i] for i in ind]

    # accumulation of points
    cumulative_points = sorted_points
    for i in range(1, len(cumulative_points)):
        cumulative_points[i] = cumulative_points[i - 1] + cumulative_points[i]

    # deleting elements with the same date
    ind_to_del = []
    for i in range(1, len(sorted_dates_for_plotting)):
        if sorted_dates_for_plotting[i] == sorted_dates_for_plotting[i - 1]:
            ind_to_del.append(i - 1)
    for i in range(len(ind_to_del))[::-1]:
        del sorted_dates_for_plotting[ind_to_del[i]]
        del cumulative_points[ind_to_del[i]]

    # some stats
    points_per_day_list = [cumulative_points[0]] + [cumulative_points[i] - cumulative_points[i - 1] for i in range(1, len(cumulative_points))]

    print('***' + name + '***')
    print("Total points: ", cumulative_points[-1])
    print("Max points per day: ", max(points_per_day_list))
    print("Max points per day: ")
    max_points_list = list(reversed(list(sorted(points_per_day_list))))[0:6]
    ind_days_max_points = [i for i, e in enumerate(points_per_day_list) if e in max_points_list]

    cumulatative_max_points_list = [cumulative_points[i] for i in ind_days_max_points]
    max_points_list = [points_per_day_list[i] for i in ind_days_max_points]
    days_with_max_points = [sorted_dates_for_plotting[i] for i in ind_days_max_points]

    list_of_days_with_max_points = []
    for i in range(len(days_with_max_points)):
        list_single_day = [days_with_max_points[i].strftime("%b %d %Y"), str(max_points_list[i]) + ' points total']
        for j in range(len(clear_date)):
            if clear_date[j] == days_with_max_points[i]:
                list_single_day.append(name_of_maps[j] + ' (' + str(points[j]) + ' points)')
        list_of_days_with_max_points.append(list_single_day)

    for i in range(len(list_of_days_with_max_points)):
        print(list_of_days_with_max_points[i])
    print("***")

    return sorted_dates_for_plotting, cumulative_points, days_with_max_points, cumulatative_max_points_list, points_per_day_list, max_points_list, name


sorted_dates, cumul_points, days_max_points, list_cumul_max_points, points_per_day, list_max_points, PLAYER_NAME = player_stats_data(
    nickname1)
sorted_dates2, cumul_points2, days_max_points2, list_cumul_max_points2, points_per_day2, list_max_points2, PLAYER_NAME2 = player_stats_data(
    nickname2)
s_d3, c_p3, d_m_p3, l_c_m_p3, ppd3, lmp3, pl_name3 = player_stats_data(nickname3)
s_d4, c_p4, d_m_p4, l_c_m_p4, ppd4, lmp4, pl_name4 = player_stats_data(nickname4)
# plot
fig = pylab.figure()

sp1 = pylab.subplot(2, 1, 1)
sp1.plot_date(sorted_dates, cumul_points, fmt="g.", label=PLAYER_NAME)
sp1.plot_date(days_max_points, list_cumul_max_points, fmt='rx', label=PLAYER_NAME + ' max points per day')

sp1.plot_date(sorted_dates2, cumul_points2, fmt="y.", label=PLAYER_NAME2)
sp1.plot_date(days_max_points2, list_cumul_max_points2, fmt='bx', label=PLAYER_NAME2 + ' max points per day')

sp1.plot_date(s_d3, c_p3, fmt="c.", label=pl_name3)
sp1.plot_date(d_m_p3, l_c_m_p3, fmt='gx', label=pl_name3 + ' max points per day')

sp1.plot_date(s_d4, c_p4, fmt="m.", label=pl_name4)
sp1.plot_date(d_m_p4, l_c_m_p4, fmt='kx', label=pl_name4 + ' max points per day')

sp1.legend()
sp1.set_title(PLAYER_NAME + "," + PLAYER_NAME2 + "," + pl_name3 + "," + pl_name4 + " points")
pylab.ylabel('Total points')
pylab.grid()

sp2 = pylab.subplot(2, 1, 2)
sp2.plot_date(sorted_dates, points_per_day, fmt="g.")
sp2.plot_date(days_max_points, list_max_points, fmt='rx')

sp2.plot_date(sorted_dates2, points_per_day2, fmt="y.")
sp2.plot_date(days_max_points2, list_max_points2, fmt='bx')

sp2.plot_date(s_d3, ppd3, fmt="c.")
sp2.plot_date(d_m_p3, lmp3, fmt='gx')

sp2.plot_date(s_d4, ppd4, fmt="m.")
sp2.plot_date(d_m_p4, lmp4, fmt='kx')

pylab.ylabel('Points per day')
pylab.grid()

pylab.show()
