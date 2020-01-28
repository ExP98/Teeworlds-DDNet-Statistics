import csv
import re


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


def get_last_timestamp(file_link):
    with open(file_link, 'rb') as f_bin:
        f_bin.seek(-128, 2)
        last = f_bin.readlines()[-1].decode()
        return re.split(',".*",', last)[1][1:-2]


def get_all_top10teams(fold_link):
    map_dictionary = {}
    with open(fold_link + 'maps.csv', 'r', encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=',')
        next(reader)
        for row in reader:
            if row[1] == "Novice":
                map_dictionary[row[0]] = dict()

    print(get_last_timestamp(fold_link + 'teamrace.csv'))

    with open(fold_link + 'teamrace.csv', 'r', encoding='utf-8') as f:
        next(f)
        for line in f:
            map_name = re.split(',".*",', line)[0][1:-1]
            if map_name in map_dictionary.keys():
                info = re.findall(',".*",', line)[0].split(',')
                team_id = info[-2][1:-1]
                race_time = float(info[-3])
                nick = ','.join(info[1:-3])[1:-1]
                if team_id not in map_dictionary[map_name].keys():
                    map_dictionary[map_name][team_id] = [[nick], race_time]
                else:
                    map_dictionary[map_name][team_id][0].append(nick)

    for map_record in map_dictionary.keys():
        map_dictionary[map_record] = list(map_dictionary[map_record].values())
        map_dictionary[map_record] = get_marked_top10(sorted(map_dictionary[map_record], key=lambda x: x[1]))

    return map_dictionary


def print_records_only_in_one_file(diff_keys, map_dict):
    if diff_keys:
        for dkey in diff_keys:
            print("This map is only in one record list")
            print(dkey, map_dict[dkey])


def is_equal(list1, list2):
    return list1[0] == list2[0] and set(list1[1]) == set(list2[1]) and list1[2] == list2[2]


def print_difference(key, rec_list1, rec_list2):
    print(key)
    print("Old:", rec_list1)
    print("New:", rec_list2)
    print("***")


map_dict_current = get_all_top10teams('../ddnet-stats/')
map_dict_old = get_all_top10teams('../old_ddnet-stats/')

intersec_keys = map_dict_current.keys() & map_dict_old.keys()
diff_keys_curr = map_dict_current.keys() - intersec_keys
diff_keys_old = map_dict_old.keys() - intersec_keys

print_records_only_in_one_file(diff_keys_old, map_dict_old)
print_records_only_in_one_file(diff_keys_curr, map_dict_current)

for k in intersec_keys:
    if len(map_dict_current[k]) != len(map_dict_old[k]):
        print_difference(k, map_dict_old[k], map_dict_current[k])
    else:
        for i in range(len(map_dict_current[k])):
            if not is_equal(map_dict_current[k][i], map_dict_old[k][i]):
                print_difference(k, map_dict_old[k], map_dict_current[k])
                break
