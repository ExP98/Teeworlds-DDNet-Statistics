import re

time_players_dict = dict()
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        other_info = (re.findall(',".*",', line))[0].split(',')
        time = float(other_info[-3])
        nick = ','.join(other_info[1:-3])
        if nick not in time_players_dict.keys():
            time_players_dict[nick] = time
        else:
            time_players_dict[nick] += time

sort_d = sorted(time_players_dict.items(), key=lambda x: x[1], reverse=True)

for rank, (player, time) in enumerate(sort_d[0:15]):
    print(rank + 1, player, round(time/3600, 2))  # in hours

with open('../output_files/sum_time_for_all.txt', 'w', encoding='utf-8') as f:
    f.write("Rank. Player: TotalTime(Hours)\n")
    for rank, (player, time) in enumerate(sort_d):
        f.write('%d. %s: %s\n' % (rank + 1, player, round(time/3600, 2)))
