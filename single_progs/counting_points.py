import re
import csv
from collections import defaultdict

# dict {'map':points}
map_points = {}
with open('../ddnet-stats/maps.csv', 'r', encoding='latin-1') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(fp)
    for row in reader:
        map_points[row[0]] = int(row[2])

nick_dict = defaultdict(set)
with open('../ddnet-stats/race.csv', 'r', encoding='latin-1') as f:
    next(f)  # skipping header
    for line in f:
        map = re.split(',".*",', line)[0][1:-1]
        nick = ','.join((re.findall(',".*",', line))[0].split(',')[1:-3])[1:-1]
        nick_dict[nick].add(map)
print('count of diff nicks: ', len(nick_dict.keys()))

pts_dict = dict()
for key in nick_dict.keys():
    total_points = 0
    for mp in nick_dict[key]:
        total_points += map_points[mp]
    if total_points >= 1000:
        pts_dict[key] = total_points

print('count of selected nicks: ', len(pts_dict.keys()))

sorted_list_of_tuple_points = sorted(pts_dict.items(), key=lambda x: x[1], reverse=True)

with open('../output_files/nicks_points_1000pt.tsv', 'w', encoding='latin-1') as f:
    f.write("Rank\t\"Nickname\"\tPoints\n")
    for rank, (nick_name, points) in enumerate(sorted_list_of_tuple_points):
        f.write('%d\t\"%s\"\t%d\n' % (rank+1, nick_name, points))

print("PeX", pts_dict["PeX"])
print("Cor", pts_dict["Cor"])
print("not PeX", pts_dict["not PeX"])
