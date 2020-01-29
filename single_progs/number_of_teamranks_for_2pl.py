import re

team_id_dict = dict()
player1 = "PeX"
player2 = "ad"

with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)
    for line in f:
        info = re.findall(',".*",', line)[0].split(',')
        team_id = info[-2][1:-1]
        nick = ','.join(info[1:-3])[1:-1]

        if nick == player1 or nick == player2:
            if team_id not in team_id_dict.keys():
                team_id_dict[team_id] = [nick]
            else:
                team_id_dict[team_id].append(nick)

counter = 0
for id_key in team_id_dict.keys():
    if player1 in team_id_dict[id_key] and player2 in team_id_dict[id_key]:
        counter += 1

print("Number of teamranks for 2 players:", counter)
