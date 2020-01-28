import csv
import re
from datetime import datetime


def get_marked_top10(team_members_time_list):
    top10teams = []
    curr_time = -1
    rank = 0
    time_was_equal = False
    for itr, elem in enumerate(team_members_time_list):
        if curr_time != elem[1]:
            if time_was_equal:
                rank = itr + 1
                time_was_equal = False
            else:
                rank += 1
            if rank > 10:
                break
            top10teams.append([rank, elem[0], elem[1]])
            curr_time = elem[1]
        else:
            top10teams.append([rank, elem[0], elem[1]])
            time_was_equal = True
    return top10teams


# "YYYY-MM-DD"
requested_date = datetime.strptime("2019-01-25", "%Y-%m-%d")
print(requested_date)
print()

map_dictionary = {}
map_dictionary_new = {}
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader)
    for row in reader:
        if row[1] == "Novice":
            map_dictionary[row[0]] = dict()
            map_dictionary_new[row[0]] = dict()

with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        if map_name in map_dictionary.keys():
            info = re.findall(',".*",', line)[0].split(',')
            team_id = info[-2][1:-1]
            race_time = float(info[-3])
            nick = ','.join(info[1:-3])[1:-1]
            timestamp = datetime.strptime(re.split(',".*",', line)[1][1:-2], "%Y-%m-%d %H:%M:%S")
            
            if team_id not in map_dictionary_new[map_name].keys():
                map_dictionary_new[map_name][team_id] = [[nick], race_time]
            else:
                map_dictionary_new[map_name][team_id][0].append(nick)
                
            if timestamp < requested_date:
                if team_id not in map_dictionary[map_name].keys():
                    map_dictionary[map_name][team_id] = [[nick], race_time]
                else:
                    map_dictionary[map_name][team_id][0].append(nick)

for map_record in map_dictionary.copy():
    if not map_dictionary[map_record]:
        del map_dictionary[map_record]
        continue
    map_dictionary[map_record] = list(map_dictionary[map_record].values())
    map_dictionary[map_record] = get_marked_top10(sorted(map_dictionary[map_record], key=lambda x: x[1]))
    
for map_record in map_dictionary_new.keys():
    map_dictionary_new[map_record] = list(map_dictionary_new[map_record].values())
    map_dictionary_new[map_record] = get_marked_top10(sorted(map_dictionary_new[map_record], key=lambda x: x[1]))


def print_records_only_in_one_file(diff_keys, map_dict):
    if diff_keys:
        for dkey in diff_keys:
            print("This map is only in one record list")
            print(dkey, map_dict[dkey])


def get_times_by_nick(res_list):
    dct = dict()
    for list_item in res_list:
        for player_nick in list_item[1]:
            if player_nick not in dct.keys():
                dct[player_nick] = list_item[2]
    return dct


intersec_keys = map_dictionary_new.keys() & map_dictionary.keys()
diff_keys_curr = map_dictionary_new.keys() - intersec_keys
diff_keys_old = map_dictionary.keys() - intersec_keys

print_records_only_in_one_file(diff_keys_old, map_dictionary)
print_records_only_in_one_file(diff_keys_curr, map_dictionary_new)

for map_key in intersec_keys:
    old_dict = get_times_by_nick(map_dictionary[map_key])
    new_dict = get_times_by_nick(map_dictionary_new[map_key])
    copy_of_map_dict_new = map_dictionary_new[map_key]

    players_with_better_time = []

    for nick_key in new_dict.keys():
        if nick_key not in old_dict.keys():
            players_with_better_time.append(nick_key)
        elif new_dict[nick_key] < old_dict[nick_key]:
            players_with_better_time.append(nick_key)

    if players_with_better_time:
        print("MAP: ", map_key)
        print('Old: ', map_dictionary[map_key])
        print('New: ', map_dictionary_new[map_key])

        for nick_key in players_with_better_time:
            for i in range(len(copy_of_map_dict_new)):
                if nick_key in copy_of_map_dict_new[i][1]:
                    if new_dict[nick_key] == copy_of_map_dict_new[i][2]:
                        copy_of_map_dict_new[i] = [copy_of_map_dict_new[i][0], copy_of_map_dict_new[i][1], copy_of_map_dict_new[i][2], True]
        for itm in copy_of_map_dict_new:
            if len(itm) > 3:
                print(itm[:3])

        print("***")
