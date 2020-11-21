import re
import csv
from matplotlib import pyplot as plt, dates as mdates, colors as mclrs, ticker
from datetime import datetime, timedelta
import numpy as np
import random

nick_name_list_to_compare = ["PeX", "ad", "AvapiX", "Patiga"]


def save_figure(fig, name):
    fig.set_size_inches((11.69, 8.27), forward=False)  # A4
    fig.savefig("output_data_comparative_stat/" + name + ".pdf", dpi=1000)


def set_bar_axes(axes_list, x_labels, bar_data_list, title_list):
    color_list = np.random.rand(len(nick_list), 3)  # RGB
    for rank, ax in enumerate(axes_list):
        ax.bar(x_labels, bar_data_list[rank], align='center', color=color_list)
        ax.set_title(title_list[rank])
        if len(x_labels) >= 4:
            ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    # for total points
    axes_list[1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.1f}'.format(x / 1000) + 'K'))


def set_ax_with_personal_stats(chosen_nick, ax, clr, clr2, mrkr):
    time_counter = 0
    date_points_map_dict = {}   # date_points_map_dict is main program structure
    # keys are every date (day) in race file
    # values are [0, set(finished maps on this day)]
    # later it will transform to [points_counted_by_finished_on_this_day_maps, set(...)]
    # and later to [points (only for this day), current_number_of_points (all points before + this day)]
    set_of_finished_maps = set()
    with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
        next(f)  # skipping header
        for line in f:
            other_info = (re.findall(',".*",', line))[0].split(',')
            nick = ','.join(other_info[1:-3])[1:-1]
            if nick == chosen_nick:
                finished_map = re.split(',".*",', line)[0][1:-1]
                time = float(other_info[-3])
                time_counter += time
                if finished_map not in set_of_finished_maps:
                    timestamp = datetime.date(datetime.strptime((other_info[-2])[1:-1], "%Y-%m-%d %H:%M:%S"))
                    if timestamp not in date_points_map_dict.keys():
                        date_points_map_dict[timestamp] = [0, []]
                    date_points_map_dict[timestamp][1].append(finished_map)  # making set of finished maps on this day
                    set_of_finished_maps.add(finished_map)  # only for map_counter

    map_counter = len(set_of_finished_maps)  # total count of different finished maps
    total_points = 0
    for key in date_points_map_dict.keys():
        for map in date_points_map_dict[key][1]:
            date_points_map_dict[key][0] += map_points[map]  # counting points for all maps on this day
        total_points += date_points_map_dict[key][0]    # counting points for all dates

    # list(el) because we need to transform tuple to list (to change, tuple is unchangeable)
    top5_days_max_points = [list(el) for el in
                            sorted(date_points_map_dict.items(), key=lambda x: x[1][0], reverse=True)[:5]]

    print("Stats for", chosen_nick, "\n\nTop 5 days with max points:")
    for item in top5_days_max_points:
        mp_list = []
        for mp in item[1][1]:
            mp_list.append(mp + " (" + str(map_points[mp]) + " p)")
        item[1][1] = mp_list
        print(item[0].strftime("%b %d %Y"), '-', item[1][0], 'points - maps: ', item[1][1])

    current_points = 0
    for k in date_points_map_dict.keys():
        current_points += date_points_map_dict[k][0]
        date_points_map_dict[k][1] = current_points  # writing count of points for less or equal this date

    first_date = list(date_points_map_dict.items())[0][0]
    last_date = list(date_points_map_dict.items())[-1][0]

    monthly_stat = {}
    # filling all months between 1st and last dates at least 0 (to make plot more precisely)
    curr_date = first_date
    while curr_date <= last_date:
        short_date = curr_date.strftime("%Y-%m")
        if short_date not in monthly_stat.keys():
            monthly_stat[short_date] = [0, 0]
        curr_date += timedelta(days=27)
    # curr date could be more than last date but last month 'd not be in dict
    short_date = last_date.strftime("%Y-%m")
    if short_date not in monthly_stat.keys():
        monthly_stat[short_date] = [0, 0]

    for k in date_points_map_dict.keys():
        monthly_stat[k.strftime("%Y-%m")][0] += date_points_map_dict[k][0]

    current_points = 0
    for month in monthly_stat.keys():
        current_points += monthly_stat[month][0]
        monthly_stat[month][1] = current_points

    annual_stat = {}
    for k in date_points_map_dict.keys():
        shortest_date = k.strftime("%Y")
        if shortest_date not in annual_stat.keys():
            annual_stat[shortest_date] = [date_points_map_dict[k][0], 0]
        else:
            annual_stat[shortest_date][0] += date_points_map_dict[k][0]
    current_points = 0
    for year in annual_stat.keys():
        current_points += annual_stat[year][0]
        annual_stat[year][1] = current_points

    print('\nPoints:', total_points)
    max_points_per_1_day = top5_days_max_points[0][1][0]
    print('Max points per day:', max_points_per_1_day)
    print('Count of different maps by', chosen_nick, ':', map_counter)
    total_time = round(time_counter / 60 / 60, 2)
    print('Total time of all finishes (in hours):', total_time, '\n')

    dates_max_points_list = [item[0] for item in top5_days_max_points]
    daily_max_points_list = [item[1][0] for item in top5_days_max_points]
    totally_max_points_list = [date_points_map_dict[dt][1] for dt in dates_max_points_list]

    ax[0].plot_date(date_points_map_dict.keys(), [date_points_map_dict[k][1] for k in date_points_map_dict.keys()],
                    fmt='.', c=clr, label=chosen_nick)
    ax[0].plot_date(dates_max_points_list, totally_max_points_list, c=clr2, fmt='x', label=chosen_nick)

    ax[1].plot_date(date_points_map_dict.keys(), [date_points_map_dict[k][0] for k in date_points_map_dict.keys()],
                    fmt='.', c=clr, label=chosen_nick)
    ax[1].plot_date(dates_max_points_list, daily_max_points_list, c=clr2, fmt='x', label=chosen_nick)

    months_list = [datetime.strptime(k, "%Y-%m") for k in monthly_stat.keys()]
    ax[2].plot(months_list, [monthly_stat[k][1] for k in monthly_stat.keys()], c=clr)
    ax[2].plot(months_list, [monthly_stat[k][1] for k in monthly_stat.keys()], c=clr, marker='.', markeredgecolor='k', label=chosen_nick)
    ax[3].plot_date(months_list, [monthly_stat[k][0] for k in monthly_stat.keys()], c=clr, marker=mrkr, markeredgecolor='k', label=chosen_nick)

    annual_list = [datetime.strptime(k, "%Y") for k in annual_stat.keys()]
    ax[4].plot(annual_list, [annual_stat[k][1] for k in annual_stat.keys()], c=clr)
    ax[4].plot(annual_list, [annual_stat[k][1] for k in annual_stat.keys()], c=clr, marker='^', markeredgecolor='k', label=chosen_nick)
    ax[5].scatter(annual_list, [annual_stat[k][0] for k in annual_stat.keys()], label=chosen_nick, c=clr, edgecolor='k', marker=mrkr)
    return [total_time, total_points, max_points_per_1_day, map_counter]


def set_axes_for_comp_stats(nickname_list, axes_list):
    # to choose different random colors and marker for each player
    n = len(nickname_list)
    clr_list = list(mclrs.cnames.keys())
    marker_list = [".", "o", "v", "^", "<", ">", "1", "2", "s", "p", "P", "*", "h", "H", "+", "x", "X", "D", "d"]
    rand_color_list = []
    rand_marker_list = []
    for i in range(n):
        rand_color_list.append(clr_list[random.randint(0, len(clr_list) - 1)])
        rand_color_list.append(clr_list[random.randint(0, len(clr_list) - 1)])
        rand_marker_list.append(marker_list[random.randint(0, len(marker_list) - 1)])

    info = []
    for num, nickname in enumerate(nickname_list):
        info.append(set_ax_with_personal_stats(nickname, axes_list, rand_color_list[num],
                                               rand_color_list[num+n], rand_marker_list[num]))
    return info


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

fig1, (ax11, ax12) = plt.subplots(nrows=2, ncols=1)
fig2, (ax21, ax22) = plt.subplots(nrows=2, ncols=1)
fig3, (ax31, ax32) = plt.subplots(nrows=2, ncols=1)

rule = mdates.rrulewrapper(mdates.MONTHLY, interval=1)
ax21.xaxis.set_major_locator(mdates.RRuleLocator(rule))
ax21.xaxis.set_major_formatter(formatter=mdates.DateFormatter('%Y-%m'))
ax21.xaxis.set_tick_params(rotation=75, labelsize=9)

ax22.xaxis.set_major_locator(mdates.RRuleLocator(rule))
ax22.xaxis.set_major_formatter(formatter=mdates.DateFormatter('%Y-%m'))
ax22.xaxis.set_tick_params(rotation=75, labelsize=9)

nick_list = nick_name_list_to_compare

personal_info = set_axes_for_comp_stats(nick_list, [ax11, ax12, ax21, ax22, ax31, ax32])

ax11.set_title("Total points")
ax11.legend()
ax11.set_ylabel('Total points')
ax11.grid()

ax12.set_title("Points per day")
ax12.set_ylabel('Points per day')
ax12.grid()
ax12.legend()
fig1.tight_layout()

save_figure(fig1, "daily_stats")

ax21.set_title("Monthly total points")
ax21.set_ylabel('Total points')
ax21.legend()
ax21.grid()

ax22.set_title("Points per month")
ax22.set_ylabel('Points per month')
ax22.legend()
ax22.grid()
fig2.tight_layout()

save_figure(fig2, "monthly_stats")

ax31.set_title("Annual total points")
ax31.set_ylabel('Total points')
ax31.legend()
ax31.grid()

ax32.set_title("Annual points per year")
ax32.set_ylabel('Points per year')
ax32.legend()
ax32.grid()
fig3.tight_layout()

save_figure(fig3, "annual_stats")

fig_bar, ax_bar = plt.subplots(nrows=1, ncols=4)

titles = ['Total time of all finishes (in hours)', 'Total points', 'Max points per day', 'Count of finished maps']
bar_data = [
    [item[0] for item in personal_info],    # total_time
    [item[1] for item in personal_info],    # total_points
    [item[2] for item in personal_info],    # max_points_per_1_day
    [item[3] for item in personal_info]     # map_counter
]

set_bar_axes(ax_bar, nick_list, bar_data, titles)

save_figure(fig_bar, "personal_stat")
# plt.show()
