import csv
import re
from statistics import median, mean
from matplotlib import pyplot as plt, ticker
import pandas as pd
import numpy as np
import seaborn as sns

# ["ALL", "Novice", "Moderate", "Brutal", "Insane", "Dummy", "DDmaX", "Oldschool", "Solo", "Race"]
OPTION = "Brutal"
# OPTION = "ALL"

general_dict = {}
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader)
    for row in reader:
        if OPTION == "ALL":
            general_dict[row[0]] = [int(row[2]), int(row[3]), [], []]
        else:
            if row[1] == OPTION:
                general_dict[row[0]] = [int(row[2]), int(row[3]), [], []]

with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        time = float(other_info[-3])
        read_nick = ''.join(other_info[1:-3])[1:-1]
        if map_name in general_dict.keys():
            general_dict[map_name][2].append(read_nick)
            general_dict[map_name][3].append(time / 60)

for map_key in general_dict.keys():
    pts, stars, finishers, times = general_dict[map_key]
    general_dict[map_key] = [pts, stars, len(set(finishers)), len(finishers), mean(times), median(times)]

names = list(general_dict.keys())
y_stars = [x[1][1] for x in list(general_dict.items())]  # stars
y_pts = [x[1][0] for x in list(general_dict.items())]  # points
x_uniq = [x[1][2] for x in list(general_dict.items())]  # unique finishers
# x_fin = [x[1][3] for x in list(general_dict.items())]                     # all finishes
# x_mean = [round(float(x[1][4]), 2) for x in list(general_dict.items())]   # mean time
x_med = [round(float(x[1][5]), 2) for x in list(general_dict.items())]  # median time

if 1:
    fig = plt.figure()


    def onpick3(event):
        ind = event.ind
        print('onpick3:', "Map:", np.take(names, ind), "Stars:", np.take(y_stars, ind), "Points:", np.take(y_pts, ind),
              "Coords:", np.take(x_uniq, ind), np.take(x_med, ind))


    # ax_1 = fig.add_subplot(2, 1, 1)
    ax_1 = fig.add_subplot()
    if OPTION == "ALL":
        sc2 = ax_1.scatter(x_uniq, x_med, c=y_pts, picker=True)  # colors = points (y_pts) or stars (y_stars)
        legend1 = ax_1.legend(*sc2.legend_elements(), title="Points")
    else:
        sc2 = ax_1.scatter(x_uniq, x_med, c=y_stars, picker=True)
        legend1 = ax_1.legend(*sc2.legend_elements(), title="Stars")

    ax_1.add_artist(legend1)
    ax_1.set_xlabel('Count of unique finishers')
    ax_1.set_ylabel('Median time (min)')
    ax_1.set_title(OPTION + " maps (click on a point to get info)")

    ax_1.set_xscale('log')
    ax_1.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, numticks=12))
    ax_1.grid()

    # ax_2 = fig.add_subplot(2, 1, 2)
    # ax_2.scatter(x_fin, x_mean, c=y_stars, picker=True)
    # ax_2.set_title("All finishes x Mean time")
    # ax_2.set_xlabel('Count of finishes')
    # ax_2.set_ylabel('Mean time (min)')

    fig.canvas.mpl_connect('pick_event', onpick3)

df = pd.DataFrame(list(general_dict.values()), index=list(general_dict.keys()),
                  columns=["Points", "Stars", "Unique finishers", "All finishes", "Mean time", "Median time"])
corr = df.corr()
plt.figure(figsize=(11, 7))
ax_hm = sns.heatmap(corr, annot=True, cmap='BrBG')
ax_hm.set_xticklabels(ax_hm.get_xticklabels(), rotation=15)
ax_hm.set_title(OPTION + "maps")
plt.show()
