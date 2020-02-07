import csv
import re
from statistics import median, mean
from matplotlib import pyplot as plt, ticker
import pandas as pd
import numpy as np
import seaborn as sns


def onpick3(event):
    ind = event.ind
    print('onpick3:', "Map:", np.take(names, ind), "Stars:", np.take(y_stars, ind), "Points:", np.take(y_pts, ind),
          "Coords:", np.take(x_uniq, ind), np.take(x_med, ind))


def set_axis(axis_list):
    for axis in axis_list:
        axis.yaxis.set_tick_params(labelbottom=True)
        axis.set_ylabel('')
        axis.tick_params(axis='y', labelsize=10)
        axis.yaxis.grid(alpha=0.5, ls=':', c='k')
        axis.set_axisbelow(True)


general_dict = {}
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader)
    for row in reader:
        general_dict[row[0]] = [int(row[2]), int(row[3]), [], [], row[1]]

with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        race_time = float(other_info[-3])
        read_nick = ''.join(other_info[1:-3])[1:-1]
        if map_name in general_dict.keys():
            general_dict[map_name][2].append(read_nick)
            general_dict[map_name][3].append(race_time / 60)

for map_key in general_dict.keys():
    pts, stars, finishers, times, mode = general_dict[map_key]
    general_dict[map_key] = [pts, stars, len(set(finishers)), len(finishers), mean(times), median(times), mode]

possible_options = ["Novice", "Moderate", "Brutal", "Insane", "Dummy", "DDmaX", "Oldschool", "Solo", "Race", "ALL"]
for opt in possible_options:
    # *** --- PLOT 1 --- ***
    if opt != "ALL":
        names = [x[0] for x in list(general_dict.items()) if x[1][6] == opt]
        y_stars = [x[1][1] for x in list(general_dict.items()) if x[1][6] == opt]                   # stars
        y_pts = [x[1][0] for x in list(general_dict.items()) if x[1][6] == opt]                     # points
        x_uniq = [x[1][2] for x in list(general_dict.items()) if x[1][6] == opt]                    # unique finishers
        # x_fin = [x[1][3] for x in list(general_dict.items()) if x[1][6] == opt]                   # all finishes
        # x_mean = [round(float(x[1][4]), 2) for x in list(general_dict.items()) if x[1][6] == opt] # mean time
        x_med = [round(float(x[1][5]), 2) for x in list(general_dict.items()) if x[1][6] == opt]    # median time
    else:
        names = [x[0] for x in list(general_dict.items())]
        y_stars = [x[1][1] for x in list(general_dict.items())]
        y_pts = [x[1][0] for x in list(general_dict.items())]
        x_uniq = [x[1][2] for x in list(general_dict.items())]
        x_med = [round(float(x[1][5]), 2) for x in list(general_dict.items())]

    fig = plt.figure()
    ax_1 = fig.add_subplot()
    if opt == "ALL":
        sc2 = ax_1.scatter(x_uniq, x_med, c=y_pts, picker=True)  # colors = points (y_pts) or stars (y_stars)
        legend1 = ax_1.legend(*sc2.legend_elements(), title="Points")
    else:
        sc2 = ax_1.scatter(x_uniq, x_med, c=y_stars, picker=True)
        legend1 = ax_1.legend(*sc2.legend_elements(), title="Stars")

    ax_1.add_artist(legend1)
    ax_1.set_xlabel('Count of unique finishers')
    ax_1.set_ylabel('Median time (min)')
    ax_1.set_title(opt + " maps")

    ax_1.set_xscale('log')
    ax_1.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, numticks=12))
    ax_1.grid()
    fig.set_size_inches((11.69, 8.27), forward=False)  # A4
    fig.canvas.mpl_connect('pick_event', onpick3)  # (click on points to get info)

    # use one of next three options: savefig() or show() or both
    fig.savefig('output_plots/Scatter/' + opt + '.pdf', dpi=1000)
    # plt.show()        # commented because of show() after 2nd plot
    # *** --- PLOT 1 --- ***

    df = pd.DataFrame(list(general_dict.values()), index=list(general_dict.keys()),
                      columns=["Points", "Stars", "Unique finishers", "All finishes", "Mean time", "Median time", "Mode"])
    if opt != "ALL":
        df = df[df["Mode"] == opt]
    df = df.drop(columns="Mode")

    # *** --- PLOT 2 --- ***
    fig2, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(11, 6), sharey='row')
    fig2.suptitle(opt + " maps")

    sns.violinplot(x="Stars", y="Median time", data=df, inner="box", saturation=0.5, palette="BrBG", scale="width", ax=ax1)
    sns.violinplot(x="Stars", y="Median time", data=df, inner="box", saturation=0.5, palette="BrBG", scale="count", ax=ax2)
    sns.boxplot(x="Stars", y="Median time", data=df, ax=ax3,
                boxprops={'edgecolor': '0.4'}, whiskerprops={'color': '0.4'}, capprops={'color': '0.4'})
    sns.swarmplot(x="Stars", y="Median time", data=df, color="black", size=2.5, ax=ax3)

    set_axis([ax1, ax2, ax3])
    ax1.set_ylabel('Median time')
    ax1.set_title("Viloin plots (same width)")
    ax2.set_title("Viloin plots (counts)")
    ax3.set_title("Box plots (and swarm plots)")

    fig2.savefig('output_plots/Violin_box_plots/' + opt + '.pdf', dpi=1000)
    plt.show()
    # *** --- PLOT 2 --- ***

    # *** --- PLOT 3 --- ***
    corr = df.corr()

    fig3 = plt.figure()
    ax_hm = sns.heatmap(corr, annot=True, cmap='BrBG')
    ax_hm.set_xticklabels(ax_hm.get_xticklabels(), rotation=15)
    ax_hm.set_title(opt + " maps")
    fig3.set_size_inches((11.69, 8.27), forward=False)  # A4
    fig3.savefig('output_plots/Correlations/' + opt + '_correlation.pdf', dpi=1000)
    plt.close()
    # *** --- PLOT 3 --- ***
