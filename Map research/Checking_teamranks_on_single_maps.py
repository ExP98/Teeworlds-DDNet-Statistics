import csv
import re

single_maps = dict()
no_team_servers = {"Dummy", "Solo", "Race"}
with open('../ddnet-stats/maps.csv', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader)
    for row in reader:
        if row[1] in no_team_servers:
            single_maps[row[0]] = set()

with open('../ddnet-stats/teamrace.csv', 'r', encoding='utf-8') as f:
    next(f)
    for line in f:
        map_name = re.split(',".*",', line)[0][1:-1]
        team_id = re.findall(',".*",', line)[0].split(',')[-2][1:-1]
        if map_name in single_maps.keys():
            single_maps[map_name].add(team_id)

for map_key in single_maps.keys():
    if single_maps[map_key]:
        print(map_key, len(single_maps[map_key]))
