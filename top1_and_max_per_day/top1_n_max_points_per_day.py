# import sys
import csv
import re
import time
import pylab as plt
from matplotlib.dates import MONTHLY, DateFormatter, rrulewrapper, RRuleLocator
from datetime import datetime, timedelta


# making dict with key=date for every days till now
def get_date(file_line):
    o_i = (re.findall(',".*",', file_line))[0].split(',')
    t_s = (o_i[-2])[1:-1]
    return datetime.strptime(t_s, "%Y-%m-%d %H:%M:%S") \
               .replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

start_time = time.clock()
with open('../ddnet-stats/race.csv', 'rb') as f_bin:
    next(f_bin)
    first = next(f_bin).decode()
    f_bin.seek(-128, 2)
    last = f_bin.readlines()[-1].decode()
curr_date = get_date(first)
last_date = get_date(last)
c_date = curr_date

date_dict = {}
while curr_date <= last_date:
    date_dict[curr_date] = ['', -1]
    curr_date += timedelta(days=1)
# date_dict[date] = ['nick of top1', his_points]; -1 is default amount of points

print("Dict with dates is done")

# preparing race file for reading: saving only 1st finish for each player-map, points for each map
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
print("Map dict is done")

# deleting duplicates from race file to only reading and counting points during next reading
# (cuz every row will be unique)
no_duplicates_list = []
dict_nick_maps = {}
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as fr:
    next(fr)  # skipping header
    for line in fr:
        map = re.split(',".*",', line)[0][1:-1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        timestamp = (other_info[-2])[1:-1]
        nick = ''.join(other_info[1:-3])[1:-1]

        if nick not in dict_nick_maps.keys():
            dict_nick_maps[nick] = {map}
            no_duplicates_list.append((map_points[map], timestamp, nick))
        else:
            if map not in dict_nick_maps[nick]:
                dict_nick_maps[nick].add(map)
                no_duplicates_list.append((map_points[map], timestamp, nick))
# print('len: ', len(no_duplicates_list), ', size: ', sys.getsizeof(no_duplicates_list)/1024/1024, ' MB')

top1 = list(dict_nick_maps)[0]
# print('first_finisher: ', top1)
dict_nick_maps.clear()
map_points.clear()
print("No duplicates is done")

# player_points_dict[nick] = current_count_of_points
top1_set = set()
player_points_dict = {top1: 0}

pl_dict = dict()
max_diff_list = []

for item in no_duplicates_list:
    points = item[0]
    date = datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S")
    nick = item[2]

    # c_date is 00:00 of next day for 1st date in race
    if date >= c_date:
        while c_date < date:
            # if some players have same max points (and ex-top1 is one of them) then ex-top1 still will be top1
            m = max(player_points_dict.values())
            if player_points_dict[top1] != m:
                top1 = max(player_points_dict, key=player_points_dict.get)
                top1_set.add(top1)

            for k in player_points_dict.keys():
                if k in pl_dict.keys():
                    if (player_points_dict[k] - pl_dict[k]) >= 300:
                        max_diff_list.append([player_points_dict[k] - pl_dict[k], k, c_date])

            pl_dict = player_points_dict.copy()

            date_dict[c_date] = [top1, player_points_dict[top1]]
            c_date += timedelta(days=1)

    if nick not in player_points_dict.keys():
        player_points_dict[nick] = points
    else:
        player_points_dict[nick] += points

top1 = max(player_points_dict, key=player_points_dict.get)
date_dict[c_date] = [top1, player_points_dict[top1]]
print("Top1-s were found")

with open('output_files/top1points.csv', 'w', encoding='utf-8') as f:
    f.write("Date,Top1,Points\n")
    for (dt, [top1nick, top1points]) in list(date_dict.items()):
        f.write('"%s","%s",%s\n' % (datetime.date(dt), top1nick, top1points))

print(len(top1_set), top1_set)
max_diff_list = sorted(max_diff_list, key=lambda tup: tup[0], reverse=True)
with open('output_files/max_count_points_per_day.csv', 'w', encoding='utf-8') as f:
    f.write("PointsPerDay,Nick,Date\n")
    for (points, nick, dt) in max_diff_list:
        f.write('%s,"%s","%s"\n' % (points, nick, datetime.date(dt)))
print("Files were recorded")

# PLOT TOP 1 POINTS

players_dict = {}
with open('output_files/top1points.csv', 'r', encoding='utf-8') as fr:
    next(fr)  # skipping header
    for line in fr:
        dt = datetime.date(datetime.strptime(re.split(',".*",', line)[0][1:-1], "%Y-%m-%d"))
        points = int(re.split(',".*",', line)[1][:-2])
        nick = (re.findall(',".*",', line))[0].split(',')[1][1:-1]
        if nick not in players_dict.keys():
            players_dict[nick] = [[dt], [points]]
        else:
            players_dict[nick][0].append(dt)
            players_dict[nick][1].append(points)

fig1, ax1 = plt.subplots()
for k in players_dict.keys():
    plt.plot_date(players_dict[k][0], players_dict[k][1], '.', label=k + ' (' + str(len(players_dict[k][0])) + ')')
plt.legend(title="Nicks (days on top)")
plt.title("Top 1 Points")
rule = rrulewrapper(MONTHLY, interval=2)
ax1.xaxis.set_major_locator(RRuleLocator(rule))
ax1.xaxis.set_major_formatter(formatter=DateFormatter('%d-%m-%y'))
ax1.xaxis.set_tick_params(rotation=30, labelsize=8)
plt.xlabel('Date')
plt.ylabel('Points')
plt.grid()
fig1.set_size_inches((11.69, 8.27), forward=False)  # A4
fig1.savefig('output_files/top1points_plot.pdf', dpi=1000)
# *** PLOT TOP 1 POINTS ***

# PLOT MAX POINTS PER DAY

max_pts_per_day = []
with open('output_files/max_count_points_per_day.csv', 'r', encoding='utf-8') as fr:
    next(fr)  # skipping header
    for line in fr:
        points = int(re.split(',".*",', line)[0])
        dt = datetime.date(datetime.strptime(re.split(',".*",', line)[1][1:-2], "%Y-%m-%d"))
        nick = (re.findall(',".*",', line))[0].split(',')[1][1:-1]
        max_pts_per_day.append((points, nick, dt))

max_pts_per_day = sorted(max_pts_per_day, key=lambda tup: tup[0], reverse=True)[:15]
# min and max for Y_ticks in plot
min_point = max_pts_per_day[-1][0]
max_point = max_pts_per_day[0][0]

fig2, ax2 = plt.subplots()
for item in max_pts_per_day:
    plt.plot_date(item[2], item[0], label=item[1] + ' (' + str(item[0]) + ') ')
leg = plt.legend(prop={'size': 10})
plt.title("Max points per 1 day")

rule = rrulewrapper(MONTHLY, interval=2)
ax2.xaxis.set_major_locator(RRuleLocator(rule))
ax2.xaxis.set_major_formatter(formatter=DateFormatter('%d-%m-%y'))
ax2.xaxis.set_tick_params(rotation=30, labelsize=10)
ax2.set_yticks(list(range((min_point - 10) // 10 * 10, max_point + 30, 20)))

plt.xlabel('Date')
plt.ylabel('Points')
plt.grid()
fig2.set_size_inches((11.69, 8.27), forward=False)  # A4
fig2.savefig('output_files/max_points_per_day_plot.pdf', dpi=1000)

print("Figures were saved")
print(time.clock() - start_time, " seconds")

# *** PLOT MAX POINTS PER DAY ***
