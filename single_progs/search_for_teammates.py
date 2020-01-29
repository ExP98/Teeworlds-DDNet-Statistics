import re

ids_dict = dict()
with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        info = re.findall(',".*",', line)[0].split(',')
        team_id = info[-2][1:-1]
        pl_nick = ','.join(info[1:-3])[1:-1]

        if team_id not in ids_dict.keys():
            ids_dict[team_id] = [pl_nick]
        else:
            ids_dict[team_id].append(pl_nick)

players_dict = dict()
for id_key in ids_dict.keys():
    for player_nick in ids_dict[id_key]:
        if player_nick not in players_dict.keys():
            players_dict[player_nick] = {*ids_dict[id_key]}
        else:
            players_dict[player_nick].update(ids_dict[id_key])

len_dict = {}
for key in players_dict.keys():
    players_dict[key].remove(key)
    len_dict[key] = len(players_dict[key])

sorted_list_len_dict = sorted(len_dict.items(), key=lambda x: x[1], reverse=True)[:1000]

with open('../output_files/players_with_most_mates.txt', 'w', encoding='utf-8') as f:
    f.write("Players with the most number of teammates (top-1000)\n")
    for rnk, (nck_nm, num_of_tmmts) in enumerate(sorted_list_len_dict, 1):
        f.write('%d. %s: %d\n' % (rnk, nck_nm, num_of_tmmts))

with open('../output_files/nick-teammates.txt', 'w', encoding='utf-8') as f:
    for player, teammates in players_dict.items():
        f.write('%s: %s\n' % (player, str(teammates)[1:-1]))
