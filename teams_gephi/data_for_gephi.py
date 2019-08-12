import re
import csv

# open [OLD] writing_csv_to_gephi.py file to read more info

# dict "[Map] = points"
data_read_dict = {}
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as f_csv:
    reader = csv.reader(f_csv, delimiter=',')
    next(reader)
    for row in reader:
        data_read_dict[row[0]] = int(row[2])

set_maps = set()
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f_csv:
    reader = csv.reader(f_csv, delimiter=',')
    next(reader)
    for row in reader:
        set_maps.add(row[0])

for map in set_maps.difference(data_read_dict.keys()):
    data_read_dict[map] = 0

dict_nick = {}
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)
    for line in f:
        map = re.split(',".*",', line)[0][1:-1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        nick = ','.join(other_info[1:-3])[1:-1]
        if nick not in dict_nick.keys():
            dict_nick[nick] = set()
            dict_nick[nick].add(map)
        elif nick in dict_nick.keys():
            dict_nick[nick].add(map)
        else:
            print("ERROR!!!")

nick_to_del = []
pts = 0
barrier_to_entry = 600
for nickname in dict_nick.keys():
    for map in dict_nick[nickname]:
        pts += data_read_dict[map]
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
curr_id = ""
current_list = []
players_dict = {}
biggest_team_list = []
# players_dict[ID(nick)] = set(ID(nick1), ID(nick2), ...)
with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map = re.split(',".*",', line)[0][1:-1]
        info = re.findall(',".*",', line)[0].split(',')
        team_id = info[-2][1:-1]
        nick = ','.join(info[1:-3])[1:-1]
        if curr_id == team_id:
            current_list.append(nick)
        else:
            if len(current_list) > 15:
                biggest_team_list.append([len(current_list), curr_id, "", *current_list])
            for nck in current_list:
                if nck in dict_nick.keys():
                    if dict_nick[nck] not in players_dict.keys():
                        players_dict[dict_nick[nck]] = set()
                    for nn in current_list:
                        if nn in dict_nick.keys():
                            players_dict[dict_nick[nck]].add(dict_nick[nn])
            curr_id = team_id
            current_list = [nick]
# last iteration:
for nck in current_list:
    if nck in dict_nick.keys():
        if dict_nick[nck] not in players_dict.keys():
            players_dict[dict_nick[nck]] = set()
        for nn in current_list:
            if nn in dict_nick.keys():
                players_dict[dict_nick[nck]].add(dict_nick[nn])

# player has himself in his teammates list
for key in players_dict.keys():
    players_dict[key].remove(key)

# Adjacency List
with open('data_gephi/adj_list_edges_gephi.csv', 'w', encoding='utf-8') as f:
    for items in players_dict.keys():
        f.write(str(items))
        for ii in players_dict[items]:
            f.write(',' + str(ii))
        f.write('\n')

with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        team_id = re.findall(',".*",', line)[0].split(',')[-2][1:-1]
        for item in biggest_team_list:
            if item[1] == team_id:
                timestamp = re.split(',".*",', line)[1][1:-2]
                map = re.split(',".*",', line)[0][1:-1]
                item[1] = timestamp
                item[2] = map

biggest_team_list = sorted(biggest_team_list, key=lambda x: x[0], reverse=True)
with open('biggest_team.txt', 'w', encoding='utf-8') as f:
    f.write("Biggest teams: number of members, date, map, members\n")
    for rank, elem in enumerate(biggest_team_list):
        f.write('%d. %d players, %s, %s, %s\n' % (rank+1, elem[0], elem[1],  elem[2], ", ".join(str(i) for i in elem[3:])))
