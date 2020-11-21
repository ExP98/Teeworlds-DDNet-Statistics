import csv
import re
from datetime import datetime

# "YYYY-MM-DD"
requested_date = datetime.strptime("2020-05-01", "%Y-%m-%d")
print(requested_date)


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
            top10teams.append([rank, elem[0], elem[1], elem[2]])
            curr_time = elem[1]
        else:
            top10teams.append([rank, elem[0], elem[1], elem[2]])
            time_was_equal = True
    return top10teams


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
                map_dictionary_new[map_name][team_id] = [[nick], race_time, team_id]
            else:
                map_dictionary_new[map_name][team_id][0].append(nick)
                
            if timestamp < requested_date:
                if team_id not in map_dictionary[map_name].keys():
                    map_dictionary[map_name][team_id] = [[nick], race_time, team_id]
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

diff_keys_curr = map_dictionary_new.keys() - map_dictionary_new.keys() & map_dictionary.keys()

if diff_keys_curr:
    for dkey in diff_keys_curr:
        print("New map: ", dkey)
        print(map_dictionary_new[dkey])

for map_key in map_dictionary_new.keys() & map_dictionary.keys():
    new_team_ids = set([x[3] for x in map_dictionary_new[map_key]]) - set([x[3] for x in map_dictionary[map_key]])
    if new_team_ids:
        print(map_key)
        for record_row in map_dictionary_new[map_key]:
            if record_row[3] in new_team_ids:
                print(*record_row[:3])
        print("***")
