import re

pl_id = ""
current_list = []
players_dict = {}

with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        info = re.findall(',".*",', line)[0].split(',')
        team_id = info[-2][1:-1]
        pl_nick = ','.join(info[1:-3])[1:-1]

        if pl_id == team_id:
            current_list.append(pl_nick)
        else:
            for nck in current_list:
                if nck not in players_dict.keys():
                    players_dict[nck] = set()
                for nn in current_list:
                    players_dict[nck].add(nn)
            pl_id = team_id
            current_list = [pl_nick]
# last iteration
for nck in current_list:
    if nck not in players_dict.keys():
        players_dict[nck] = set()
    for nn in current_list:
        players_dict[nck].add(nn)

len_dict = {}
for key in players_dict.keys():
    players_dict[key].remove(key)
    len_dict[key] = len(players_dict[key])

sorted_list_len_dict = sorted(len_dict.items(), key=lambda x: x[1], reverse=True)[:1000]

with open('../output_files/players_with_most_mates.txt', 'w', encoding='utf-8') as f:
    f.write("Players with the most number of teammates (top-1000)\n")
    for rnk, (nck_nm, num_of_tmmts) in enumerate(sorted_list_len_dict):
        f.write('%d. %s: %d\n' % (rnk+1, nck_nm, num_of_tmmts))

with open('../output_files/nick-teammates.txt', 'w', encoding='utf-8') as f:
    for player, teammates in players_dict.items():
        f.write('%s: %s\n' % (player, str(teammates)[1:-1]))
