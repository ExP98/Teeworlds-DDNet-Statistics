import csv
import re

map_server = {}
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader)
    for row in reader:
        if row[1] == "Novice":
            map_server[row[0]] = dict()

with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        if map_name in map_server.keys():
            info = re.findall(',".*",', line)[0].split(',')
            team_id = info[-2][1:-1]
            race_time = float(info[-3])
            nick = ','.join(info[1:-3])[1:-1]
            # records with the same team_id could be not even close in teamrace file
            # so we can't just compare current and previous team_id-s
            if team_id not in map_server[map_name].keys():
                map_server[map_name][team_id] = [[nick], race_time]
            else:
                map_server[map_name][team_id][0].append(nick)

for map_n in map_server.keys():
    map_server[map_n] = list(map_server[map_n].values())

# max teams ever
max_teams = []
for mp in map_server.keys():
    for item in map_server[mp]:
        if len(item[0]) > 15:
            max_teams.append([mp, len(item[0]), item[1], item[0]])
print("Biggest teams:")
for mt in max_teams:
    print(mt)


def get_marked_top10(teammembers_time_list):
    top10teams = []
    curr_time = -1
    rank = 0
    time_was_equal = False
    for itr, elem in enumerate(teammembers_time_list):
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


for map_record in map_server:
    map_server[map_record] = get_marked_top10(sorted(map_server[map_record], key=lambda x: x[1]))
    # print(map_record, map_server[map_record])


def points_calculation(map_dict, calc_list, size_of_top=20):
    teamrank_points = dict()
    for m_name in map_dict:
        player_set = set()
        for itm in map_dict[m_name]:
            for mate_nick in itm[1]:
                if mate_nick not in player_set:
                    if mate_nick not in teamrank_points.keys():
                        teamrank_points[mate_nick] = calc_list[itm[0]]
                    else:
                        teamrank_points[mate_nick] += calc_list[itm[0]]
                    player_set.add(mate_nick)
    return sorted(teamrank_points.items(), key=lambda x: x[1], reverse=True)[:size_of_top]


def print_points_calc(pts_c):
    for i, (nickname, pts) in enumerate(pts_c):
        print('%d. %s %d' % (i + 1, nickname, pts))


pts_calc_list = dict(zip(list(range(1, 11)), [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]))
first_rank_calc = dict(zip(list(range(1, 11)), [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]))

print('\nTeam rank points (Novice):')
print_points_calc(points_calculation(map_server, pts_calc_list))
print('\nCount of 1st places (Novice):')
print_points_calc(points_calculation(map_server, first_rank_calc))
