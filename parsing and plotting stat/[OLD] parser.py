import requests
from lxml import html


def reading_data(tr, mode):
    maps_list_lxml = tr.xpath('//div[@id = "' + mode + '"]')[0]

    count_maps = len(maps_list_lxml.xpath('./div/table[@class = "spacey"]/tbody/tr'))
    parsed_data = []

    for i in range(count_maps):
        map_lxml = maps_list_lxml.xpath('./div/table[@class = "spacey"]/tbody/tr')[i]
        name_maps = map_lxml.xpath('./td')
        map_info = []
        for map in name_maps:
            map_info.append(map.text_content())
        parsed_data.append(map_info)
    return parsed_data


url = 'https://ddnet.tw/players/PeX/'
r = requests.get(url)

with open('test_data/test.html', 'w', encoding='utf-8') as handle:
    for block in r.iter_content(1024):
        handle.write(block.decode('utf-8'))

with open("test_data/test.html", 'r', encoding='utf-8') as fobj:
    xml = fobj.read()
tree = html.fromstring(xml)

data_read_novice = reading_data(tree, 'Novice')
data_read_moderate = reading_data(tree, 'Moderate')
data_read_brutal = reading_data(tree, 'Brutal')
data_read_insane = reading_data(tree, 'Insane')
data_read_dummy = reading_data(tree, 'Dummy')
data_read_ddmax = reading_data(tree, 'DDmaX')
data_read_oldschool = reading_data(tree, 'Oldschool')
data_read_solo = reading_data(tree, 'Solo')
data_read_race = reading_data(tree, 'Race')

data_read = data_read_novice + data_read_moderate + data_read_brutal + data_read_insane + data_read_dummy + \
            data_read_ddmax + data_read_oldschool + data_read_solo + data_read_race
