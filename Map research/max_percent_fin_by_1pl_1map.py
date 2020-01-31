import re

count_of_finishes = dict()
general_dict = dict()
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        nick_name = ''.join((re.findall(',".*",', line))[0].split(',')[1:-3])[1:-1]
        if map_name not in count_of_finishes.keys():
            count_of_finishes[map_name] = 1
        else:
            count_of_finishes[map_name] += 1
        if map_name not in general_dict.keys():
            general_dict[map_name] = dict()
            general_dict[map_name][nick_name] = 1
        else:
            if nick_name not in general_dict[map_name].keys():
                general_dict[map_name][nick_name] = 1
            else:
                general_dict[map_name][nick_name] += 1

eps = 0.005             # reduce the length of the sorted list
barrier_to_entry = 15   # number of finishes to be in the list (to exclude overrated share in little-finished maps)

share_fin_list = []
short_share_fin_list = []
for map_key in general_dict.keys():
    for nick_key in general_dict[map_key].keys():
        share_of_finishes = general_dict[map_key][nick_key] / count_of_finishes[map_key]
        if share_of_finishes >= eps:
            share_fin_list.append([map_key, nick_key, share_of_finishes, general_dict[map_key][nick_key], count_of_finishes[map_key]])
            if count_of_finishes[map_key] >= barrier_to_entry:
                short_share_fin_list.append([map_key, nick_key, share_of_finishes, general_dict[map_key][nick_key], count_of_finishes[map_key]])

nick_map_share_fin_list = sorted(share_fin_list, key=lambda x: x[2], reverse=True)[:1000]
short_share_fin_list = sorted(short_share_fin_list, key=lambda x: x[2], reverse=True)[:1000]

with open('output/biggest_shares_of_finishes_1map_by_1pl.txt', 'w', encoding='utf-8') as f:
    f.write("Players with the largest share of finishes on maps\n")
    f.write("No., map, nick, share, finishes for player, overall number of finishes\n")
    for rank, (name_of_map, nick, share, fin, all_fin) in enumerate(nick_map_share_fin_list, 1):
        f.write('%d. %s - %s - %.4f, %d, %d\n' % (rank, name_of_map, nick, share, fin, all_fin))

with open('output/biggest_shares_of_finishes_1map_by_1pl_(15_and_more).txt', 'w', encoding='utf-8') as f:
    f.write("Players with the largest share of finishes on maps (only >= 15 finishes on the map)\n")
    f.write("No., map, nick, share, finishes for player, overall number of finishes\n")
    for rank, (name_of_map, nick, share, fin, all_fin) in enumerate(short_share_fin_list, 1):
        f.write('%d. %s - %s - %.4f, %d, %d\n' % (rank, name_of_map, nick, share, fin, all_fin))
