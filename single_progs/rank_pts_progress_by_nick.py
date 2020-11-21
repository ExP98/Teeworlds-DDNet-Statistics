import re
import csv
from matplotlib import pyplot as plt
from datetime import datetime

selected_nick = "ad"


def add_to_records(record_list, pts_dict_values, pts_num, tstamp):
    overall_rank = 1
    for points_number in pts_dict_values:
        if pts_num < points_number:
            overall_rank += 1
    record_list.append([overall_rank, pts_num, tstamp])


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

nick_pts_dict = dict()
nick_finished_maps = dict()
record_list_selected_nick = []

with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        dt = datetime.date(datetime.strptime((other_info[-2])[1:-1], "%Y-%m-%d %H:%M:%S"))
        nick = ','.join(other_info[1:-3])[1:-1]

        if nick not in nick_finished_maps.keys():
            nick_finished_maps[nick] = set(map_name)
            nick_pts_dict[nick] = map_points[map_name]
            if nick == selected_nick:
                add_to_records(record_list_selected_nick, list(nick_pts_dict.values()), nick_pts_dict[selected_nick], dt)
        else:
            if map_name not in nick_finished_maps[nick]:
                nick_finished_maps[nick].add(map_name)
                nick_pts_dict[nick] += map_points[map_name]
                if nick == selected_nick:
                    add_to_records(record_list_selected_nick, list(nick_pts_dict.values()), nick_pts_dict[selected_nick], dt)

### plot
rank_list = [item[0] for item in record_list_selected_nick]
points_list = [item[1] for item in record_list_selected_nick]
dates_list = [item[2] for item in record_list_selected_nick]

ranks_to_annotate = []
pts_to_annotate = []
borders_to_check = [1, 10, 100, 500]; borders_to_check.extend(list(range(1000, points_list[-1] // 1000 * 1000 + 1, 1000)))
# borders_to_check = [1, 100, 500, 1000, 2000, 3000, 5000, 7000, 10000, 15000, 18000, 19000, 20000, 24000, 25000, 26000] # special for Cor
for bor in borders_to_check:
    for i, pts in enumerate(points_list):
        if pts >= bor:
            pts_to_annotate.append((dates_list[i], pts))
            ranks_to_annotate.append((dates_list[i], rank_list[i]))
            break

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

ax1.plot_date(dates_list, points_list, fmt=".")
ax1.set_ylabel('Total points')
for (x_date, y_pts) in pts_to_annotate:
    ax1.annotate(y_pts, (x_date, y_pts), xytext=(x_date, y_pts+500), arrowprops=dict(arrowstyle="->", facecolor='black'))
ax1.plot_date([item[0] for item in pts_to_annotate], [item[1] for item in pts_to_annotate], fmt="r.")
ax1.set_ylim([0,(points_list[-1] // 1000 + 1) * 1000])
ax1.grid()

ax2.plot_date(dates_list, rank_list, fmt="-")
ax2.set_yscale('log')
ax2.set_ylabel('Overall rank')
for y_val in [1, 100, 10000]:
    ax2.axhline(y=y_val, color='gray', linewidth=0.5)
for item in ranks_to_annotate:
    ax2.annotate(item[1], item)
ax2.plot_date([item[0] for item in ranks_to_annotate], [item[1] for item in ranks_to_annotate], fmt="b.")
ax2.grid()

ax1.set_title(selected_nick + " stats")
# plt.show()
fig.set_size_inches((11.69, 8.27), forward=False)  # A4
fig.savefig('../output_files/rank_points_progress/r_pts_progress_' + selected_nick+ '.pdf', dpi=1000)
