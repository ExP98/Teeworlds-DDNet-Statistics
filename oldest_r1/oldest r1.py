import csv
import numpy
import re
from datetime import datetime

map_dict = {}
with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        map = re.split(',".*",', line)[0][1:-1]
        other_info = (re.findall(',".*",', line))[0].split(',')
        timestamp = (other_info[-2])[1:-1]
        time = float(other_info[-3])
        if map not in map_dict.keys():
            map_dict[map] = [time, timestamp]
        else:
            if map_dict[map][0] > time:
                map_dict[map] = [time, timestamp]

indeces = [map_dict[dict_val][1] for dict_val in map_dict]
ind = numpy.argsort(indeces)
sorted_d = [list(map_dict.items())[i] for i in ind]

with open('oldest_r1.txt', 'w', encoding='utf-8') as f:
    f.write("Map: Time, Date\n")
    for mp, [tm, dt] in sorted_d:
        f.write('%s:\t%s,\t%s\n' % (mp, str(tm), str(dt)))

map_rls_dict = {}
with open('maps_rls_date_notnull.txt', 'r', encoding='utf-8') as fp:
    reader = csv.reader(fp, delimiter=',')
    next(reader)
    for row in reader:
        map_rls_dict[row[0]] = row[5]

wrong_rls = []
with open('early_r1.txt', 'w', encoding='utf-8') as f:
    f.write('All these maps were completed in less than 1.5 day for r1\n')
    for k in map_dict.keys():
        if k in map_rls_dict.keys():
            t1 = datetime.strptime(map_dict[k][1], "%Y-%m-%d %H:%M:%S")
            t2 = datetime.strptime(map_rls_dict[k], "%Y-%m-%d %H:%M:%S")
            if (t1 - t2).total_seconds() <= 1.5 * 24 * 60 * 60:
                f.write(k + ',\t\trls: ' + str(t2) + ',\tr1: ' + str(t1) + '\n')
            if t2 > t1:
                wrong_rls.append((k, str(t2), str(t1)))
    f.write("\nWrong! !!! r1 < rls date!!!\n")
    for item in wrong_rls:
        f.write(item[0] + ',\t\trls: ' + item[1] + ',\tr1: ' + item[2] + '\n')
