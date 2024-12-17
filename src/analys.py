from bs4 import BeautifulSoup
from collections import Counter


def count_time(file_name, type_time='timex3'):
    result = []
    count = 0
    if type_time == 'timex3':
        attr = 'type'
    else:
        attr = 'class'
    with open(file_name, encoding='utf8') as f:
        # data = f.readlines()
        soup = BeautifulSoup(f.read(), 'html.parser')
        for tag in soup.find_all('timeml'):
            for t in tag.find_all(type_time):
                attrs = t.attrs
                if attr not in attrs.keys():
                    count += 1
                else:
                    # print(attrs[attr])
                    result.append(attrs[attr][0])

                # if attrs['type'] == 'DATE':
                #     print(t)

        # print(len(data))
        # for i in range(len(data)):
        #
        #     if i % 7 == 4:
        #         # print(i, '====', data[i].strip())
        #         print(i, data[i].count("<TIMEX3") == data[i].count("</TIMEX3>"))
    print(len(result))
    # print(result)
    dict_result = dict(Counter(result))
    dict_result['none_type'] = count
    return dict_result


def main():
    file = '../data/event/event_dp_verb_timeml.txt'
    print(count_time(file, 'event'))


main()
