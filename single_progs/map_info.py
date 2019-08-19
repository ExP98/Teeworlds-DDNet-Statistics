import csv
import re
import numpy as np

# dict "[Map] = [points, finishes, set of fin-ed players, total mins by finishers]"
data_read_dict = {}
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader)
    for row in reader:
        data_read_dict[row[0]] = [int(row[2]), 0, set(), 0]

# cuz some maps were deleted but still exist in race file, these maps will have points -1
set_maps = set()
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    for row in reader:
        if row[0] not in data_read_dict.keys():
            data_read_dict[row[0]] = [-1, 0, set(), 0]

with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map = re.split(',".*",', line)[0][1:-1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        time = float(other_info[-3])
        nick = ''.join(other_info[1:-3])

        data_read_dict[map][1] += 1
        data_read_dict[map][2].add(nick)
        data_read_dict[map][3] += time

map_to_del = []
for keys in data_read_dict.keys():
    data_read_dict[keys][2] = len(data_read_dict[keys][2])
    if data_read_dict[keys][0] == -1:
        map_to_del.append(keys)
for mapp in map_to_del:
    del data_read_dict[mapp]

# sort by data_read_dict[dict_val][0] - points; [1] - fin-s; [2] - fin-ed players; [3] - total time
indeces = [data_read_dict[dict_val][3] for dict_val in data_read_dict]
ind = np.argsort(indeces)[::-1]
sorted_d = [list(data_read_dict.items())[i] for i in ind]

with open('../output_files/map_info.csv', 'w', encoding='utf-8') as f:
    f.write('Map,Points,CountOfFinishes,CountOfFinishers,TotalTimeInMap(Sec)\n')
    for items in sorted_d:
        f.write(str(items[0]) + ',' + str(items[1][0]) + ',' + str(items[1][1])
                + ',' + str(items[1][2]) + ',' + str(round(items[1][3], 2)) + '\n')
