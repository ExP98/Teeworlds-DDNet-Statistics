### Descending list of players who finished Insane maps

import re
import csv

# dict {'map':points}
insane_maps = set()
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(fp)
    for row in reader:
        if (row[1] == "Insane"):
            insane_maps.add(row[0])

players_insane = dict()
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        nick = ','.join(other_info[1:-3])[1:-1]

        if map_name in insane_maps:
            if nick not in players_insane.keys():
                players_insane[nick] = {map_name}
            else:
                players_insane[nick].add(map_name)

###
# dict {'map':points}
map_points = dict()
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

nick_dict = dict()
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map = re.split(',".*",', line)[0][1:-1]
        nick = ','.join((re.findall(',".*",', line))[0].split(',')[1:-3])[1:-1]
        if nick in players_insane.keys():
            if nick not in nick_dict.keys():
                nick_dict[nick] = {map}
            else:
                nick_dict[nick].add(map)

for key in nick_dict.keys():
    total_points = 0
    for mp in nick_dict[key]:
        total_points += map_points[mp]
    nick_dict[key] = total_points

for player in players_insane.keys():
    player_insane_pts = 0
    insane_map_list = []
    for insane_map in players_insane[player]:
        player_insane_pts += map_points[insane_map]
        insane_map_list.append((insane_map, map_points[insane_map]))
    players_insane[player] = [nick_dict[player], player_insane_pts, insane_map_list]

sorted_players_list = sorted(players_insane.items(), key=lambda x: x[1][0], reverse=False)

with open('../output_files/player_insane_finishes.csv', 'w', encoding='utf-8') as f:
    f.write("Rank,Nickname,Points,Insane_pts,List_of_insane_maps\n")
    for rank, (nick_name, (points, ins_pts, ins_list)) in enumerate(sorted_players_list, 1):
        f.write('%d,%s,%d,%d,%s\n' % (rank, nick_name, points, ins_pts, ins_list))