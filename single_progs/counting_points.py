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
        if nick not in nick_dict.keys():
            nick_dict[nick] = set()
        else:
            nick_dict[nick].add(map)

for key in nick_dict.keys():
    total_points = 0
    for mp in nick_dict[key]:
        total_points += map_points[mp]
    nick_dict[key] = total_points
print('count of diff nicks: ', len(nick_dict.keys()))

sorted_list_of_tuple_points = sorted(nick_dict.items(), key=lambda x: x[1], reverse=True)

with open('../output_files/nicks-points.csv', 'w', encoding='utf-8') as f:
    f.write("Rank,Nickname,Points\n")
    for rank, (nick_name, points) in enumerate(sorted_list_of_tuple_points):
        f.write('%d,%s,%d\n' % (rank+1, nick_name, points))

print("PeX", nick_dict["PeX"])
print("Starkiller", nick_dict["Starkiller"])
print("ad", nick_dict["ad"])
print("not PeX", nick_dict["not PeX"])
