import requests
from lxml import html
import numpy as np
import pylab as plt

nickname = "PeX"


def reading_data(tr, mode):
    maps_list_lxml = tr.xpath('//div[@id = "' + mode + '"]')[0]

    count_maps = len(maps_list_lxml.xpath('./div/table[@class = "spacey"]/tbody/tr'))
    data_read = []

    for i in range(count_maps):
        map_lxml = maps_list_lxml.xpath('./div/table[@class = "spacey"]/tbody/tr')[i]
        name_maps = map_lxml.xpath('./td')
        map_info = []
        for map in name_maps:
            map_info.append(map.text_content())
        data_read.append(map_info)
    return data_read


def get_player_data(nick_name):
    url = 'https://ddnet.tw/players/' + nick_name + '/'
    r = requests.get(url)

    with open('test_data/test.html', 'w', encoding='utf-8') as handle:
        for block in r.iter_content(1024):
            handle.write(block.decode('utf-8'))

    with open("test_data/test.html", 'r', encoding='utf-8') as fobj:
        xml = fobj.read()
    tree = html.fromstring(xml)

    data_read = reading_data(tree, 'Novice')

    # uncomment for show only ranks < 100
    # comment for show all team ranks
    name_of_maps = []
    teamrank = []
    for i in range(len(data_read)):
        if data_read[i][2] != '':
            # if (int(data_read[i][2].replace('.', '')) < 100):
            #     name_of_maps.append(data_read[i][0])
            #     teamrank.append(int(data_read[i][2].replace('.', '')))
            name_of_maps.append(data_read[i][0])
            teamrank.append(int(data_read[i][2].replace('.', '')))

    ind = np.argsort(teamrank)
    sorted_maps = [name_of_maps[i] for i in ind]
    sorted_ranks = [teamrank[i] for i in ind]

    return sorted_ranks, sorted_maps, nick_name


sorted_ranks_list, sorted_maps_list, name = get_player_data(nickname)
x_val1 = list(range(0, len(sorted_ranks_list)))

# plot
ax1 = plt.subplot()
t = x_val1
plt.scatter(x_val1, sorted_ranks_list, s=5, c=t, cmap='viridis')
plt.ylabel('Team ranks')
plt.title(name + " team ranks")
plt.grid()
plt.locator_params(axis='y', nbins=15)
plt.locator_params(axis='x', nbins=len(sorted_maps_list))
ax1.set_yticks([0, 5, 10], minor=True)
ax1.grid(which='minor', linestyle='--', linewidth='0.5', color='k')
ax1.set_xlim(0, len(sorted_maps_list))
ax1.set_xticklabels(sorted_maps_list, rotation=90, fontsize=8)
plt.show()
