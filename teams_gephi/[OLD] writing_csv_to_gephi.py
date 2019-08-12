# counting points for all
# making dict[name] = ID
# choose players only with  points >= 300
# writing nodes file (ID,Points,Label) where label is nickname; WARNING: " -> "" in labels
# counting teamranks as dict with val as list of teammates
# writing edges ADJ file where nickname -> id (dict[name] = ID)

# all code for reading and extracting data can be rewritten using correct_reading.py, which was written later
# rewritten code is in data_for_gephi.py file

import csv


def clear_reading(nick_name):
    spl = nick_name.split(',')
    _id = spl[-1].replace(chr(34), '')
    spl.remove(spl[-1])
    spl.remove(spl[-1])
    _nick = ""
    for it in spl:
        _nick = _nick + it
    return deleting_slash(_nick), _id


def deleting_slash(_nick):
    if chr(92) in set(_nick):
        shit_counter = 0
        nick_str = ""
        for c in _nick:
            if ord(c) == 92:
                shit_counter = shit_counter + 1
                if shit_counter == 2:
                    shit_counter = 0
                else:
                    nick_str = nick_str + c
            else:
                nick_str = nick_str + c
    else:
        nick_str = _nick
    return nick_str


def add_double_quotes(nick_name):
    if chr(34) in nick_name:
        nick_name = nick_name.replace(chr(34), chr(34) + chr(34))
    return nick_name


# dict "[Map] = points"
data_read_dict = {}
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    for row in reader:
        data_read_dict[row[0]] = row[2]
del data_read_dict['Map']

set_maps = set()
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    for row in reader:
        set_maps.add(row[0])
set_maps.remove("Map")

for map in set_maps.difference(data_read_dict.keys()):
    data_read_dict[map] = 0

# count points
dict_nick = {}
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    for row in reader:
        if (chr(92) in row[1]) and (len(row) < 4):
            true_nick = clear_reading(row[1])[0]
        else:
            true_nick = row[1]
            if chr(92) in true_nick:
                true_nick = deleting_slash(true_nick)

        if true_nick not in dict_nick.keys():
            dict_nick[true_nick] = set()
            dict_nick[true_nick].add(row[0])
        elif true_nick in dict_nick.keys():
            dict_nick[true_nick].add(row[0])
        else:
            print("ERROR!!!")
del dict_nick['Name']

nick_to_del = []
points = 0
for nickname in dict_nick.keys():
    for map in dict_nick[nickname]:
        points = points + int(data_read_dict[map])
    dict_nick[nickname] = points
    if points < 600:
        nick_to_del.append(nickname)
    points = 0

# deleting players with points < 600
for pl in nick_to_del:
    del dict_nick[pl]

# sorted_list_of_tuple_points = sorted(dict_nick.items(), key=lambda x: x[1], reverse=True)
#
# with open('test-points.txt', 'w', encoding='utf-8') as f:
#     for items in sorted_list_of_tuple_points:
#         f.write('%s:%s\n' % (items[0], str(items[1])))

print("PeX", dict_nick["PeX"])

ID = 0
with open('data_gephi/[OLD]nodes_gephi.csv', 'w', encoding='utf-8') as f:
    f.write("ID,Points,Label\n")
    for elem in dict_nick:
        f.write('%i,%i,"%s"\n' % (ID, dict_nick[elem], add_double_quotes(elem)))
        dict_nick[elem] = ID
        ID = ID + 1
# dict_nick[nick] = ID

# search teammates
curr_id = ""
current_list = []
players_dict = {}
dict_nick['Name'] = 0
# players_dict[ID(nick)] = set(ID(nick1), ID(nick2), ...)
with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    for row in reader:
        if (chr(92) in row[1]) and (len(row) < 4):
            true_nick1, true_id = clear_reading(row[1])
            true_nick = deleting_slash(true_nick1)
        else:
            true_id = row[3]
            true_nick = row[1]
            if chr(92) in true_nick:
                true_nick = deleting_slash(true_nick)
        if curr_id == true_id:
            current_list.append(true_nick)
        else:
            for nick in current_list:
                if nick in dict_nick.keys():
                    if dict_nick[nick] not in players_dict.keys():
                        players_dict[dict_nick[nick]] = set()
                    for nn in current_list:
                        if nn in dict_nick.keys():
                            players_dict[dict_nick[nick]].add(dict_nick[nn])
            curr_id = true_id
            current_list = [true_nick]

for nick in current_list:
    if nick in dict_nick.keys():
        if dict_nick[nick] not in players_dict.keys():
            players_dict[dict_nick[nick]] = set()
        for nn in current_list:
            if nn in dict_nick.keys():
                players_dict[dict_nick[nick]].add(dict_nick[nn])
del players_dict[dict_nick['Name']]

for key in players_dict.keys():
    players_dict[key].remove(key)

with open('data_gephi/[OLD]adj_list_edges_gephi.csv', 'w', encoding='utf-8') as f:
    # f.write("Source,Target\n")
    for items in players_dict.keys():
        f.write(str(items))
        for ii in players_dict[items]:
            f.write(',' + str(ii))
        f.write('\n')
