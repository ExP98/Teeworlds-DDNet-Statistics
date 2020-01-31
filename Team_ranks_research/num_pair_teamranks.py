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
            players_dict[player_nick] = dict()
            for mate_nick in ids_dict[id_key]:
                players_dict[player_nick][mate_nick] = 1
        else:
            for mate_nick in ids_dict[id_key]:
                if mate_nick in players_dict[player_nick].keys():
                    players_dict[player_nick][mate_nick] += 1
                else:
                    players_dict[player_nick][mate_nick] = 1

barrier = 15
for key in players_dict.copy():
    del players_dict[key][key]
    for pl_nick in players_dict[key].copy():
        if players_dict[key][pl_nick] < barrier:
            del players_dict[key][pl_nick]
    if not players_dict[key]:
        del players_dict[key]

list_of_pairs = []
for key in players_dict.keys():
    for nick_key in players_dict[key]:
        list_of_pairs.append([players_dict[key][nick_key], key, nick_key])
        del players_dict[nick_key][key]

list_of_pairs = sorted(list_of_pairs, key=lambda x: x[0], reverse=True)[:1000]

with open('best_teammates_pairs.txt', 'w', encoding='utf-8') as f:
    f.write("Pairs of players with the most number of ranks together (top-1000)\n")
    for rank, (num, nick1, nick2) in enumerate(list_of_pairs, 1):
        f.write('%d. %d - %s, %s\n' % (rank, num, nick1, nick2))
