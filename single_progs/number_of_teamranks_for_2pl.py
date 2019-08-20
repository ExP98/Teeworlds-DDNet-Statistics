import re

counter = 0
tid = ""
team_players_set = set()
player1 = "PeX"
player2 = "ad"

with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        info = re.findall(',".*",', line)[0].split(',')
        team_id = info[-2][1:-1]
        nick = ','.join(info[1:-3])[1:-1]

        if tid != team_id and team_players_set:
            team_players_set.clear()
        if nick == player1 or nick == player2:
            team_players_set.add(nick)
            if (player1 in team_players_set) and (player2 in team_players_set) and (tid == team_id):
                counter = counter + 1
                team_players_set.clear()
            tid = team_id

print("Number of teamranks for 2 players:", counter)
