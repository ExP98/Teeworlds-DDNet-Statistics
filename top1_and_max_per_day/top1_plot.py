import re
import pylab as plt
import matplotlib.dates as mdates
from datetime import datetime
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

fig1, ax1 = plt.subplots()
for k in players_dict.keys():
    plt.plot_date(players_dict[k][0], players_dict[k][1], '.', label=k + ' (' + str(len(players_dict[k][0])) + ')')
plt.legend(title="Nicks (days on top)")
plt.title("Top 1 Points")
rule = mdates.rrulewrapper(mdates.MONTHLY, interval=2)
ax1.xaxis.set_major_locator(mdates.RRuleLocator(rule))
ax1.xaxis.set_major_formatter(formatter=mdates.DateFormatter('%d-%m-%y'))
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

rule = mdates.rrulewrapper(mdates.MONTHLY, interval=2)
ax2.xaxis.set_major_locator(mdates.RRuleLocator(rule))
ax2.xaxis.set_major_formatter(formatter=mdates.DateFormatter('%d-%m-%y'))
ax2.xaxis.set_tick_params(rotation=30, labelsize=10)
ax2.set_yticks(list(range((min_point - 10) // 10 * 10, max_point + 30, 20)))

plt.xlabel('Date')
plt.ylabel('Points')
plt.grid()
fig2.set_size_inches((11.69, 8.27), forward=False)  # A4
fig2.savefig('output_files/max_points_per_day_plot.pdf', dpi=1000)

# *** PLOT MAX POINTS PER DAY ***
