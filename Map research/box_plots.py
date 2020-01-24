import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import csv
import re
from statistics import median, mean


def count_of_parts_by_window_size(some_int, window_size):
    return some_int // window_size if some_int % window_size == 0 else some_int // window_size + 1


def box_plot(data_to_plot, x_labels, title):
    fig_box, ax_box = plt.subplots()
    ax_box.set_title(title)
    ax_box.boxplot(data_to_plot, whis=[0, 95], labels=x_labels, medianprops={'color': 'indigo'}, showfliers=False,
                   meanline=True, showmeans=True, meanprops={'color': 'sienna'},
                   patch_artist=True, boxprops={'facecolor': 'lightgrey'})
    median_patch = mlines.Line2D([], [], color='indigo', label='Median line')
    mean_patch = mlines.Line2D([], [], color='sienna', label='Mean line', linestyle='--')
    upper_wh = mlines.Line2D([], [], color='black', label='Upper whisker is 95 percentile')
    ax_box.legend(handles=[median_patch, mean_patch, upper_wh])
    ax_box.set_ylabel("Minutes")
    ax_box.minorticks_on()
    ax_box.grid(which='major', axis='y', linestyle='-', linewidth='0.5', c='k', alpha=0.6)
    ax_box.grid(which='minor', axis='y', linestyle=':', linewidth='0.5', c='k', alpha=0.3)
    plt.show()


novice_maps_dict = dict(())
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader)
    for row in reader:
        if row[1] == "Novice":
            if row[2] not in novice_maps_dict.keys():
                novice_maps_dict[row[2]] = [row[0]]
            else:
                novice_maps_dict[row[2]].append(row[0])

times_dict = dict()
for maps_list in novice_maps_dict.values():
    for mp in maps_list:
        times_dict[mp] = []

with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map = re.split(',".*",', line)[0][1:-1]
        time = float((re.findall(',".*",', line))[0].split(',')[-3])
        if map in times_dict.keys():
            times_dict[map].append(time/60)

wndw = 15
for k in novice_maps_dict.keys():
    tmp_data = [times_dict[selected_map] for selected_map in novice_maps_dict[k]]
    mean_values_data = [median(item) for item in tmp_data]
    sorted_data = [[x, y] for _, x, y in sorted(zip(mean_values_data, tmp_data, list(novice_maps_dict[k])),
                                        key=lambda triple: triple[0])]

    data = [list(item[0]) for item in sorted_data]
    labels_list = [item[1] for item in sorted_data]

    for i in range(count_of_parts_by_window_size(len(data), wndw)):
        sliceObj = slice((wndw * i + 0), (wndw * i + wndw))
        box_plot(data[sliceObj], labels_list[sliceObj], str(k) + " points maps (" + str(i+1) + " part)")
