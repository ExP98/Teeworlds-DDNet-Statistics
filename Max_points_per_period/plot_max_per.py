import re
import pylab as plt
import matplotlib.dates as mdates
from datetime import datetime


def get_data_to_plot(period_string, length_of_top=15):
    data_to_plot = []
    with open('output/single_results/max_per_' + period_string + '.csv', 'r', encoding='utf-8') as fr:
        next(fr)  # skipping header
        for line in fr:
            info = re.split(',".*",', line)[1].split(',')
            pts = int(info[0])
            dt = datetime.date(datetime.strptime(info[1][1:-2], "%Y-%m-%d"))
            nick = (re.findall(',".*",', line))[0].split(',')[1][1:-1]
            data_to_plot.append((pts, nick, dt))
    return sorted(data_to_plot, key=lambda tup: tup[0], reverse=True)[:length_of_top]


def set_axes_to_plot(data, ax, period_string):
    marker_list = ["o", "v", "^", "<", ">", "1", "2", "s", "p", "P", "*", "h", "H", "x", "X", "D", "d", ".", "+"]
    for idx, item in enumerate(data):
        ax.plot_date(item[2], item[0], marker=marker_list[idx % len(marker_list)],
                      label=item[1] + ' (' + str(item[0]) + ') ')
    ax.legend(prop={'size': 8})
    ax.set_title("Max points per 1 " + period_string)

    rule = mdates.rrulewrapper(mdates.MONTHLY, interval=2)
    ax.xaxis.set_major_locator(mdates.RRuleLocator(rule))
    ax.xaxis.set_major_formatter(formatter=mdates.DateFormatter('%d-%m-%y'))
    ax.xaxis.set_tick_params(rotation=30, labelsize=8)

    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='minor', axis='y', linestyle=':', linewidth='0.5', c='k', alpha=0.1)

    if period_string == "day":
        ax.set_xlabel("Date")
    else:
        ax.set_xlabel('Start date of the recording period')
    ax.set_ylabel('Points')
    ax.grid()

# period_str_list may include "day", "week", "month", "year"
# 1st arg is always list
def plot_max_per_period(period_str_list, row, col):
    if row + col - 1 != len(period_str_list):
        print("Error!")
    fig_to_plot, axes = plt.subplots(nrows=row, ncols=col)
    if row == col == 1:
        set_axes_to_plot(get_data_to_plot(period_str_list[0]), axes, period_str_list[0])
    else:
        for idx, ax in enumerate(axes.flat):
            set_axes_to_plot(get_data_to_plot(period_str_list[idx]), ax, period_str_list[idx])
    fig_to_plot.suptitle("Max for a certain period (with the rule \"1 player - 1 record\")")

    file_name_part = ""
    if len(period_str_list) == 1:
        file_name_part = period_str_list[0]
    else:
        for prd in period_str_list:
            file_name_part += prd + "_"
        file_name_part = file_name_part[:-1]
    fig_to_plot.set_size_inches((11.69, 8.27), forward=False)  # A4
    fig_to_plot.savefig('output/single_results/max_points_per_' + file_name_part + '.pdf', dpi=1000)


# plot_max_per_period(["month"], 1, 1)
plot_max_per_period(["day", "week"], 1, 2)
plot_max_per_period(["month", "year"], 1, 2)