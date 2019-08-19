# import csv
# from datetime import datetime
#
# def clear_reading(nickname):
#     spl = nickname.split(',')
#     return spl[-1].replace('\"', '')
#
# # time_set = set()
# with open('ddnet-stats/race.csv', 'r', encoding='utf-8') as fp:
#     reader = csv.reader(fp, delimiter=',')
#     next(reader) # skip header
#     for row in reader:
#         if ((chr(92) in row[1]) and (len(row) < 4)):
#             timestamp = clear_reading(row[1])
#             # time_set.add(timestamp)
#         else:
#             timestamp = row[-2].split(',')[-1].replace('\"', '') # cuz of nicks contain ','
#         if (datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") > datetime.now()):
#             print("Future! ", timestamp)
#             print("Full row: ", row)
#
# # print(time_set)

# new version
# this prog was created after finding the finish date 2030 (gdin -> map Continuum), but most likely it's a joke ;)

import re
from datetime import datetime

with open('../ddnet-stats/race.csv', 'r', encoding='utf-8') as f:
    next(f)  # skipping header
    for line in f:
        other_info = (re.findall(',".*",', line))[0].split(',')
        timestamp = (other_info[-2])[1:-1]

        if datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") > datetime.now():
            print("Future! ", timestamp)
