import re
import csv
from matplotlib import pyplot as plt, dates as mdates
from datetime import datetime, timedelta


def rolling_avg(input_data, window_size):
    ra = []
    for i in range(len(input_data) - window_size + 1):
        ra.append(sum(input_data[i:window_size + i]) / window_size)
    return ra


def setting_avg_axes_for_plotting(ax_list, window_list, values_list, date_list_to_plot):
    for rank, wndw in enumerate(window_list):
        rol = rolling_avg(values_list, wndw)
        ax_list[rank].plot_date(date_list_to_plot[wndw // 2: len(date_list_to_plot) - (wndw - wndw // 2) + 1], rol, fmt=".")
        ax_list[rank].set_ylabel('Avg values')
        ax_list[rank].set_title("Average points per day for " + str(wndw) + " days")
        ax_list[rank].grid()


def save_figure(fig, name):
    fig.set_size_inches((11.69, 8.27), forward=False)  # A4
    fig.savefig("output_data/" + name + ".pdf", dpi=1000)


selected_nick_name = "Starkiller"

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
top5_text = ""
top5_text += "Top 5 days with max points:\n"
for item in top5_days_max_points:
    mp_list = []
    for mp in item[1][1]:
        mp_list.append(mp + " (" + str(map_points[mp]) + " p)")
    item[1][1] = mp_list
    top5_text += str(item[0].strftime("%b %d %Y")) + ' - ' + str(item[1][0]) + ' points -' + ' maps: ' + str(item[1][1]) + '\n'
print(top5_text)

current_points = 0
for k in date_points_map_dict.keys():
    current_points += date_points_map_dict[k][0]
    date_points_map_dict[k][1] = current_points

first_date = list(date_points_map_dict.items())[0][0]
curr_date = first_date
last_date = list(date_points_map_dict.items())[-1][0]
date_list = []
val_list = []

while curr_date <= last_date:
    date_list.append(curr_date)
    if curr_date in date_points_map_dict.keys():
        val_list.append(date_points_map_dict[curr_date][0])
    else:
        val_list.append(0)
    curr_date += timedelta(days=1)

monthly_stat = {}
# filling all months between 1st and last dates at least 0 (to make plot more precisely)
curr_date = first_date
while curr_date <= last_date:
    short_date = curr_date.strftime("%Y-%m")
    if short_date not in monthly_stat.keys():
        monthly_stat[short_date] = [0, 0]
    curr_date += timedelta(days=27)

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

print('Points:', total_points)
print('Max points per day:', top5_days_max_points[0][1][0])
print('Count of different maps by', selected_nick_name, ':', map_counter)
print('Total time of all finishes (in hours):', round(time_counter/60/60, 2))

# plot

dates_max_points_list = [item[0] for item in top5_days_max_points]
daily_max_points_list = [item[1][0] for item in top5_days_max_points]
totally_max_points_list = [date_points_map_dict[dt][1] for dt in dates_max_points_list]

fig1, (ax11, ax12) = plt.subplots(nrows=2, ncols=1)

ax11.plot_date(date_points_map_dict.keys(), [date_points_map_dict[k][1] for k in date_points_map_dict.keys()], fmt=".")
ax11.plot_date(dates_max_points_list, totally_max_points_list, fmt='rx', label='max points per day')
ax11.legend()
ax11.set_title(selected_nick_name + " points")
ax11.set_ylabel('Total points')
ax11.grid()

ax12.plot_date(date_points_map_dict.keys(), [date_points_map_dict[k][0] for k in date_points_map_dict.keys()], fmt=".")
ax12.plot_date(dates_max_points_list, daily_max_points_list, fmt='rx')
ax12.set_ylabel('Points per day')
ax12.grid()
fig1.tight_layout()
save_figure(fig1, "daily_stats")

fig2, (ax21, ax22, ax23, ax24) = plt.subplots(nrows=4, ncols=1)

ax21.plot_date(date_points_map_dict.keys(), [date_points_map_dict[k][0] for k in date_points_map_dict.keys()], fmt=".")
ax21.plot_date(dates_max_points_list, daily_max_points_list, fmt='rx')
ax21.set_title(selected_nick_name + " points per day")
ax21.set_ylabel('Points per day')
ax21.grid()

setting_avg_axes_for_plotting([ax22, ax23, ax24], [3, 5, 10], val_list, date_list)
fig2.tight_layout()
save_figure(fig2, "avg_for_3_5_10_days")

fig3, (ax31, ax32, ax33, ax34) = plt.subplots(nrows=4, ncols=1)

ax31.plot_date(date_points_map_dict.keys(), [date_points_map_dict[k][0] for k in date_points_map_dict.keys()], fmt=".")
ax31.plot_date(dates_max_points_list, daily_max_points_list, fmt='rx')
ax31.set_title(selected_nick_name + " points per day")
ax31.set_ylabel('Points per day')
ax31.grid()

setting_avg_axes_for_plotting([ax32, ax33, ax34], [30, 60, 120], val_list, date_list)
fig3.tight_layout()
save_figure(fig3, "avg_for_30_60_120_days")

fig4, (ax41, ax42) = plt.subplots(nrows=2, ncols=1)
months_list = [datetime.strptime(k, "%Y-%m") for k in monthly_stat.keys()]
ax41.plot(months_list, [monthly_stat[k][1] for k in monthly_stat.keys()])

rule = mdates.rrulewrapper(mdates.MONTHLY, interval=1)
ax41.xaxis.set_major_locator(mdates.RRuleLocator(rule))
ax41.xaxis.set_major_formatter(formatter=mdates.DateFormatter('%Y-%m'))
ax41.xaxis.set_tick_params(rotation=75, labelsize=9)

ax41.set_title("Monthly " + selected_nick_name + " points")
ax41.set_ylabel('Total points')
ax41.grid()

ax42.plot_date(months_list, [monthly_stat[k][0] for k in monthly_stat.keys()], fmt=".")
ax42.xaxis.set_major_locator(mdates.RRuleLocator(rule))
ax41.xaxis.set_major_formatter(formatter=mdates.DateFormatter('%Y-%m'))
ax42.xaxis.set_tick_params(rotation=75, labelsize=9)
ax42.set_ylabel('Points per month')
ax42.grid()
fig4.tight_layout()
save_figure(fig4, "monthly_stats")

fig5, (ax51, ax52) = plt.subplots(nrows=2, ncols=1)
annual_list = list(annual_stat.keys())
ax51.plot(annual_list, [annual_stat[k][1] for k in annual_stat.keys()])
ax51.set_title("Annual " + selected_nick_name + " points")
ax51.set_ylabel('Total points')
ax51.grid()

ax52.plot_date(annual_list, [annual_stat[k][0] for k in annual_stat.keys()])
ax52.set_ylabel('Points per year')
ax52.grid()
fig5.tight_layout()
save_figure(fig5, "annual_stats")

# plt.show()

# team stats

tid = set()
teammates = {}
with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        info = re.findall(',".*",', line)[0].split(',')
        nick = ','.join(info[1:-3])[1:-1]
        if nick == selected_nick_name:
            team_id = info[-2][1:-1]
            tid.add(team_id)

with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        info = re.findall(',".*",', line)[0].split(',')
        team_id = info[-2][1:-1]
        if team_id in tid:
            nick = ','.join(info[1:-3])[1:-1]
            if nick not in teammates.keys():
                teammates[nick] = 1
            else:
                teammates[nick] += 1

n_fin = teammates[selected_nick_name]
del teammates[selected_nick_name]

teammates = sorted(teammates.items(), key=lambda x: x[1], reverse=True)
best_teammates = teammates[:15]

with open('output_data/teammates_stat.txt', 'w', encoding='utf-8') as f_write:
    f_write.write("Team Statistics for " + selected_nick_name + "\n\n")
    f_write.write("Number of different teammates: " + str(len(teammates)-1) + '\n')
    f_write.write("Number of finishes in team: " + str(n_fin) + '\n')
    f_write.write("\nList of teammates:\n")
    for rate, (nick, count) in enumerate(teammates):
        f_write.write('%d. %s: %d\n' % (rate + 1, nick, count))
# ***   team stats  ***

with open('output_data/personal_stats.txt', 'w', encoding='utf-8') as f_stat:
    f_stat.write("Personal Statistics for " + selected_nick_name + "\n\n")
    f_stat.write("Points: " + str(total_points) + '\n\n')
    f_stat.write(top5_text + '\n')
    f_stat.write('Max points per day: ' + str(top5_days_max_points[0][1][0]) + '\n')
    f_stat.write('Count of different maps by ' + selected_nick_name + ': ' + str(map_counter) + '\n')
    f_stat.write('Total time of all finishes (in hours): ' + str(round(time_counter/60/60, 2)) + '\n')
    f_stat.write("Number of different teammates: " + str(len(teammates)-1) + '\n')
    f_stat.write("Number of finishes in team: " + str(n_fin) + '\n')
    f_stat.write("\nList of best teammates:\n")
    for rate, (nick, count) in enumerate(best_teammates):
        f_stat.write('%d. %s: %d\n' % (rate + 1, nick, count))
