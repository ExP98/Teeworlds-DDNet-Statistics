import csv
import re


def get_val_idx_min(mylist):
    my_min = mylist[0][2] + 1
    idx = 0
    for j, item in enumerate(mylist):
        if item[2] < my_min:
            my_min, idx = item[2], j
    return my_min, idx


nicks_to_ignore = {'brainless tee', 'nameless tee'}
race_maps_to_ignore = set()
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader)
    for row in reader:
        if row[1] == 'Race':
            race_maps_to_ignore.add(row[0])

general_dict = dict()
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        nick_name = ''.join((re.findall(',".*",', line))[0].split(',')[1:-3])[1:-1]
        if map_name in race_maps_to_ignore or nick_name in nicks_to_ignore:
            continue
        if nick_name not in general_dict.keys():
            general_dict[nick_name] = dict()
            general_dict[nick_name][map_name] = 1
        else:
            if map_name not in general_dict[nick_name].keys():
                general_dict[nick_name][map_name] = 1
            else:
                general_dict[nick_name][map_name] += 1

number_of_participants = 1000
most_finishes_list = number_of_participants*[["", "", 0]]
lower_bound = get_val_idx_min(most_finishes_list)[0]
for nn in general_dict.keys():
    for map_n in general_dict[nn].keys():
        if general_dict[nn][map_n] >= lower_bound:
            new_index = get_val_idx_min(most_finishes_list)[1]
            most_finishes_list[new_index] = [nn, map_n, general_dict[nn][map_n]]
            lower_bound = get_val_idx_min(most_finishes_list)[0]

most_finishes_list = sorted(most_finishes_list, key=lambda x: x[2], reverse=True)

print("Ignoring Race maps and \'nameless tee\' and \'brainless tee\'")
for i, it in enumerate(most_finishes_list):
    print(i+1, *it)
