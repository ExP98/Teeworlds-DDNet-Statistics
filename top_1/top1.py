import csv
import re
import time
import pylab as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


# making dict with key=date for every days till now
def get_date(file_line):
    o_i = (re.findall(',".*",', file_line))[0].split(',')
    t_s = (o_i[-2])[1:-1]
    return datetime.strptime(t_s, "%Y-%m-%d %H:%M:%S").replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)


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
        next(fp)
        for row in reader:
            if row[0] not in mp_pts.keys():
                mp_pts[row[0]] = 0
    return mp_pts


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
map_points = get_dict_map_points()

# deleting duplicates from race file to only reading and counting points during next reading
# (cuz every row will be unique)
no_duplicates_list = []
dict_nick_maps = {}
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as fr:
    next(fr)  # skipping header
    for line in fr:
        map_name = re.split(',".*",', line)[0][1:-1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        timestamp = (other_info[-2])[1:-1]
        nick = ''.join(other_info[1:-3])[1:-1]

        if nick not in dict_nick_maps.keys():
            dict_nick_maps[nick] = {map_name}
            no_duplicates_list.append((map_points[map_name], timestamp, nick))
        else:
            if map_name not in dict_nick_maps[nick]:
                dict_nick_maps[nick].add(map_name)
                no_duplicates_list.append((map_points[map_name], timestamp, nick))

top1 = list(dict_nick_maps)[0]
# print('first_finisher: ', top1)
dict_nick_maps.clear()
map_points.clear()
print("No duplicates is done")

# player_points_dict[nick] = current_count_of_points
top1_set = set()
player_points_dict = {top1: 0}

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

            date_dict[c_date] = [top1, player_points_dict[top1]]
            c_date += timedelta(days=1)

    if nick not in player_points_dict.keys():
        player_points_dict[nick] = points
    else:
        player_points_dict[nick] += points
# last iteration
top1 = max(player_points_dict, key=player_points_dict.get)
date_dict[c_date] = [top1, player_points_dict[top1]]
print("Top1-s were found")

with open('output_files/top1points.csv', 'w', encoding='utf-8') as f:
    f.write("Date,Top1,Points\n")
    for (dt, [top1nick, top1points]) in list(date_dict.items()):
        f.write('"%s","%s",%s\n' % (datetime.date(dt), top1nick, top1points))

print(len(top1_set), top1_set)
print("File was recorded")

# PLOT TOP 1 POINTS

players_dict = {}
with open('output_files/top1points.csv', 'r', encoding='utf-8') as fr:
    next(fr)  # skipping header
    for line in fr:
        dt = datetime.date(datetime.strptime(re.split(',".*",', line)[0][1:-1], "%Y-%m-%d"))
        points = int(re.split(',".*",', line)[1][:-1])
        nick = (re.findall(',".*",', line))[0].split(',')[1][1:-1]
        if nick not in players_dict.keys():
            players_dict[nick] = [[dt], [points]]
        else:
            players_dict[nick][0].append(dt)
            players_dict[nick][1].append(points)

fig, ax = plt.subplots()
for k in players_dict.keys():
    ax.plot_date(players_dict[k][0], players_dict[k][1], '.', label=k + ' (' + str(len(players_dict[k][0])) + ')')
ax.legend(title="Nicks (days on top)")
ax.set_title("Top 1 Points")

rule = mdates.rrulewrapper(mdates.MONTHLY, interval=2)
ax.xaxis.set_major_locator(mdates.RRuleLocator(rule))
ax.xaxis.set_major_formatter(formatter=mdates.DateFormatter('%d-%m-%y'))
ax.xaxis.set_tick_params(rotation=30, labelsize=8)

ax.set_axisbelow(True)
ax.minorticks_on()
ax.grid(which='minor', axis='y', linestyle=':', linewidth='0.5', c='k', alpha=0.1)
ax.grid()

ax.set_xlabel('Date')
ax.set_ylabel('Points')

fig.set_size_inches((11.69, 8.27), forward=False)  # A4
fig.savefig('output_files/top1points_plot.pdf', dpi=1000)
# *** PLOT TOP 1 POINTS ***

print("Figure was saved")
print(time.clock() - start_time, " seconds")

# in case of error "PermissionError: [Errno 13] Permission denied: 'output_files/top1points_plot.pdf'" just close the window with existing .pdf file
