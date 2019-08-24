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
