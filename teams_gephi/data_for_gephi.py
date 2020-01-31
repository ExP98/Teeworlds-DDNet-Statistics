import re
import csv

# open [OLD] writing_csv_to_gephi.py file to read more info

# dict "[Map] = points"
map_points = {}
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader)
    for row in reader:
        map_points[row[0]] = int(row[2])
# for deleted maps
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader)
    for row in reader:
        if row[0] not in map_points.keys():
            map_points[row[0]] = 0

dict_nick = {}
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        nick = ','.join(other_info[1:-3])[1:-1]
        if nick not in dict_nick.keys():
            dict_nick[nick] = {map_name}
        elif nick in dict_nick.keys():
            dict_nick[nick].add(map_name)
        else:
            print("ERROR!!!")

nick_to_del = []
pts = 0
barrier_to_entry = 600
for nickname in dict_nick.keys():
    for map_name in dict_nick[nickname]:
        pts += map_points[map_name]
    dict_nick[nickname] = pts
    if pts < barrier_to_entry:
        nick_to_del.append(nickname)
    pts = 0

# deleting players with pts < barrier_to_entry
for pl in nick_to_del:
    del dict_nick[pl]

print("PeX", dict_nick["PeX"])

with open('data_gephi/nodes_gephi.csv', 'w', encoding='utf-8') as f:
    f.write("ID,Points,Label\n")
    for rank, elem in enumerate(dict_nick):
        f.write('%i,%i,"%s"\n' % (rank, dict_nick[elem], elem))
        dict_nick[elem] = rank
# dict_nick[nick] = ID

# search teammates
ids_dict = dict()
with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        info = re.findall(',".*",', line)[0].split(',')
        team_id = info[-2][1:-1]
        pl_nick = ','.join(info[1:-3])[1:-1]
        if pl_nick in dict_nick.keys():
            if team_id not in ids_dict.keys():
                ids_dict[team_id] = [dict_nick[pl_nick]]
            else:
                ids_dict[team_id].append(dict_nick[pl_nick])

# players_dict[ID(nick)] = set(ID(nick1), ID(nick2), ...)
players_dict = dict()
for id_key in ids_dict.keys():
    for player_nick_id in ids_dict[id_key]:
        if player_nick_id not in players_dict.keys():
            players_dict[player_nick_id] = {*ids_dict[id_key]}
        else:
            players_dict[player_nick_id].update(ids_dict[id_key])

# player has himself in his teammates list
for player_key in players_dict.keys():
    players_dict[player_key].remove(player_key)

# Adjacency List
with open('data_gephi/adj_list_edges_gephi.csv', 'w', encoding='utf-8') as f:
    for items in players_dict.keys():
        f.write(str(items))
        for ii in players_dict[items]:
            f.write(',' + str(ii))
        f.write('\n')
