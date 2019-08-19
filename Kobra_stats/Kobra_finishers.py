import re
import seaborn as sns
from matplotlib import pyplot as plt


def save_figure(fig, name):
    fig.set_size_inches((11.69, 8.27), forward=False)  # A4
    fig.savefig("output/Kobra_" + name + ".pdf", dpi=1000)


def plot_bar_data(data, cum_rows, num_cols, n_lim, fig_title, is_kobra_in_title=True, y_labels=None):
    fig, ax_bar = plt.subplots(nrows=cum_rows, ncols=num_cols)
    color_scheme = sns.color_palette(n_colors=n_lim)

    for numb, axs in enumerate(ax_bar.flat):
        x_labels = [el[0] for el in data[numb]]
        bar_data = [el[1] for el in data[numb]]

        axs.bar(x_labels, bar_data, color=color_scheme)

        axs.set_axisbelow(True)
        axs.minorticks_on()
        axs.grid(which='major', axis='y', linestyle='-', linewidth='0.5', c='k', alpha=0.6)
        axs.grid(which='minor', axis='y', linestyle=':', linewidth='0.5', c='k', alpha=0.3)

        if is_kobra_in_title:
            axs.set_title("Kobra " + str(numb + 1))
        axs.xaxis.set_tick_params(rotation=30, labelsize=8)
        if y_labels is not None:
            axs.set_ylabel(y_labels[numb])

    fig.suptitle(fig_title)
    fig.tight_layout()
    save_figure(fig, fig_title)


dict_Kobra = {}
kobra_list = ["Kobra", "Kobra 2", "Kobra 3", "Kobra 4"]

with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map = re.split(',".*",', line)[0][1:-1]
        if map in kobra_list:
            other_info = (re.findall(',".*",', line))[0].split(',')
            nick = ','.join(other_info[1:-3])[1:-1]
            time = float(other_info[-3])
            if nick not in dict_Kobra:
                dict_Kobra[nick] = [[0, 0], [0, 0], [0, 0], [0, 0]]
            if map == kobra_list[0]:
                dict_Kobra[nick][0][0] += 1
                dict_Kobra[nick][0][1] += time
            if map == kobra_list[1]:
                dict_Kobra[nick][1][0] += 1
                dict_Kobra[nick][1][1] += time
            if map == kobra_list[2]:
                dict_Kobra[nick][2][0] += 1
                dict_Kobra[nick][2][1] += time
            if map == kobra_list[3]:
                dict_Kobra[nick][3][0] += 1
                dict_Kobra[nick][3][1] += time

top_limit = 10
sorted_players_max_finishes_count = []
for i in range(len(kobra_list)):
    top_items = sorted(dict_Kobra.items(), key=lambda x: x[1][i][0], reverse=True)[0:top_limit]
    sorted_players_max_finishes_count.append([[it[0], it[1][i][0]] for it in top_items])

sorted_players_max_time = []
for i in range(len(kobra_list)):
    top_items = sorted(dict_Kobra.items(), key=lambda x: x[1][i][1], reverse=True)[0:top_limit]
    sorted_players_max_time.append([[it[0], round(it[1][i][1]/60/60, 2)] for it in top_items])  # round(../60/60, 2) is hours

for itm in dict_Kobra.items():
    dict_Kobra[itm[0]] = [sum([el[0] for el in itm[1]]), round(sum([el[1] for el in itm[1]])/60/60, 2)]  # [1] is hours

sorted_overall_top_count = sorted(dict_Kobra.items(), key=lambda x: x[1][0], reverse=True)[0:top_limit]
sorted_overall_top_time = sorted(dict_Kobra.items(), key=lambda x: x[1][1], reverse=True)[0:top_limit]

with open('output/kobra_finishers.txt', 'w', encoding='utf-8') as f:
    f.write(" COUNT\n")
    for num, kobra_mp in enumerate(sorted_players_max_finishes_count):
        f.write(" *** Kobra " + str(num + 1) + " ***\n")
        for rank, [player, count] in enumerate(kobra_mp):
            f.write('%d. %s - %d\n' % (rank + 1, player, count))
        f.write(" *** \n")
    f.write("*** All Kobra maps ***\n")
    for rank, [player, [count, time]] in enumerate(sorted_overall_top_count):
        f.write('%d. %s - %d\n' % (rank + 1, player, count))
    f.write(" *** \n")

    f.write(" \nTIME (in hours)\n")
    for num, kobra_mp in enumerate(sorted_players_max_time):
        f.write(" *** Kobra " + str(num + 1) + " ***\n")
        for rank, [player, time] in enumerate(kobra_mp):
            f.write('%d. %s - %s\n' % (rank + 1, player, str(time)))
        f.write(" *** \n")
    f.write("*** All Kobra maps ***\n")
    for rank, [player, [count, time]] in enumerate(sorted_overall_top_time):
        f.write('%d. %s - %s\n' % (rank + 1, player, str(time)))
    f.write(" *** \n")

# plot

plot_bar_data(sorted_players_max_finishes_count, 2, 2, top_limit, "Count of finishes")
plot_bar_data(sorted_players_max_time, 2, 2, top_limit, "Total time of finishes (in hours)")

overall_data_for_plot = [[[el[0], el[1][0]] for el in sorted_overall_top_count], [[el[0], el[1][1]] for el in sorted_overall_top_time]]
y_lab = ['Count of finishes in all Kobra maps', 'Total time of all finishes in Kobra maps (in hours)']
plot_bar_data(overall_data_for_plot, 1, 2, top_limit, "Overall top", False, y_lab)
