import re
import csv

# dict {'map':points}
map_points = {}
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(fp)
    for row in reader:
        map_points[row[0]] = int(row[2])

# for deleted maps
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    for row in reader:
        if row[0] not in map_points.keys():
            map_points[row[0]] = 0

nick_dict = {}

with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map = re.split(',".*",', line)[0][1:-1]
        nick = ','.join((re.findall(',".*",', line))[0].split(',')[1:-3])[1:-1]
        if re.findall(r'[P]e[X]', nick):
            if nick not in nick_dict.keys():
                nick_dict[nick] = {map}
            else:
                nick_dict[nick].add(map)

for key in nick_dict.keys():
    total_points = 0
    for mp in nick_dict[key]:
        total_points += map_points[mp]
    nick_dict[key] = total_points

sorted_nick_list = sorted(nick_dict.items(), key=lambda x: x[1], reverse=True)

with open('../output_files/pex_nicks.txt', 'w', encoding='utf-8') as f:
    f.write("Nick names that contain \"PeX\" and their points\n")
    for rnk, (nck, pts) in enumerate(sorted_nick_list):
        f.write('%d. %s: %d\n' % (rnk+1, nck, pts))
