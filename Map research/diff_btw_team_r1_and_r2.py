import re
import numpy as np

map_general = dict()
with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        info = re.findall(',".*",', line)[0].split(',')
        team_id = info[-2][1:-1]
        race_time = float(info[-3])

        if map_name not in map_general.keys():
            map_general[map_name] = dict()
        if team_id not in map_general[map_name].keys():
            map_general[map_name][team_id] = race_time

for map_key in map_general.keys():
    arr = np.array(list(map_general[map_key].values()))
    if len(arr) == 1:
        map_general[map_key] = [arr[0], -1, -1, 2.01]
        continue
    if len(arr) == 0:
        print("This map is still unfinished in teams")
    mean_val = np.mean(arr)
    std_val = np.std(arr)

    min_idx = np.argmin(arr)
    first_min = arr[min_idx]
    arr2 = np.delete(arr, min_idx)
    sec_min = arr2[np.argmin(arr2)]

    norm_min1 = (first_min - mean_val) / std_val
    norm_min2 = (sec_min - mean_val) / std_val

    map_general[map_key] = [first_min, sec_min, sec_min - first_min, norm_min2 - norm_min1]

sorted_abs = sorted(map_general.items(), key=lambda kv: kv[1][2])
sorted_rel = sorted(map_general.items(), key=lambda kv: kv[1][3])

lim = 150
with open('output/least_diff_btw_tr1_tr2_abs.txt', 'w', encoding='utf-8') as f:
    f.write("Maps with the least absolute difference between 1st and 2nd team ranks\n")
    f.write("No. map, 1st result - 2nd result, absolute difference, difference between normalized (z-score) 1st and 2nd results\n")
    for rank, (name_of_map, (time1, time2, time_diff, diff_norm)) in enumerate(sorted_abs[:lim], 1):
        f.write('%d. %s - %.2f, %.2f, %.2f, %f\n' % (rank, name_of_map, time1, time2, time_diff, diff_norm))

with open('output/largest_diff_btw_tr1_tr2_abs.txt', 'w', encoding='utf-8') as f:
    f.write("Maps with the largest absolute difference between 1st and 2nd team ranks\n")
    f.write("No. map, 1st result - 2nd result, absolute difference, difference between normalized (z-score) 1st and 2nd results\n")
    for rank, (name_of_map, (time1, time2, time_diff, diff_norm)) in enumerate(sorted_abs[:-lim-1:-1], 1):
        f.write('%d. %s - %.2f, %.2f, %.2f, %f\n' % (rank, name_of_map, time1, time2, time_diff, diff_norm))

with open('output/least_diff_btw_tr1_tr2_relative.txt', 'w', encoding='utf-8') as f:
    f.write("Maps with the least relative difference between 1st and 2nd team ranks (using z-score normalization)\n")
    f.write("No. map, 1st result - 2nd result, absolute difference, difference between normalized (z-score) 1st and 2nd results\n")
    f.write("[X, -1, -1, 2.01] shows maps with only 1 team finish; [.., .., .., 2.00] shows maps with 2 team finishes\n")
    for rank, (name_of_map, (time1, time2, time_diff, diff_norm)) in enumerate(sorted_rel[:lim], 1):
        f.write('%d. %s - %.2f, %.2f, %.2f, %f\n' % (rank, name_of_map, time1, time2, time_diff, diff_norm))

with open('output/largest_diff_btw_tr1_tr2_relative.txt', 'w', encoding='utf-8') as f:
    f.write("Maps with the largest relative difference between 1st and 2nd team ranks (using z-score normalization)\n")
    f.write("No. map, 1st result - 2nd result, absolute difference, difference between normalized (z-score) 1st and 2nd results\n")
    f.write("[X, -1, -1, 2.01] shows maps with only 1 team finish; [.., .., .., 2.00] shows maps with 2 team finishes\n")
    for rank, (name_of_map, (time1, time2, time_diff, diff_norm)) in enumerate(sorted_rel[:-lim-1:-1], 1):
        f.write('%d. %s - %.2f, %.2f, %.2f, %f\n' % (rank, name_of_map, time1, time2, time_diff, diff_norm))

# for item in sorted_abs[:-lim-1:-1]:   # last "lim" rows from last
#     print(item)
# print("***")
