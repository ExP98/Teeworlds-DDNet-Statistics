import re
# from datetime import datetime

with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        # server = re.split(',".*",', line)[1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        timestamp = (other_info[-2])[1:-1]
        time = float(other_info[-3])
        nick = ','.join(other_info[1:-3])[1:-1]  # nick with no quotes
        # nick = ','.join(other_info[1:-3]) # "nick"

        # print('map: ', map_name)
        # print('nick: ', nick)
        # print('time: ', time)
        # print('timestamp: ', timestamp)
        # print('server: ', server)

with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        # timestamp = datetime.strptime(re.split(',".*",', line)[1][1:-2], "%Y-%m-%d %H:%M:%S")
        info = re.findall(',".*",', line)[0].split(',')
        team_id = info[-2][1:-1]
        nick = ','.join(info[1:-3])[1:-1]
        # print(map_name, team_id, nick)
