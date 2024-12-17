import json

from src.data import read_data


def format_event(file, texts, event_dp, event):
    event_key = event.keys()
    with open(file, 'w', encoding='utf-8') as f:
        for i in range(len(texts)):
            f.writelines(texts[i])
            for e_dp in event_dp[i]:
                for e_key in event_key:
                    if e_dp in event[e_key]:
                        event_text = '<EVENT class="' + e_key + '">' + e_dp + '</EVENT>'
                        texts[i] = texts[i].strip().replace(e_dp, event_text)
            f.writelines('<TIMEML>' + '\n')
            f.writelines(texts[i] + '\n')
            f.writelines('</TIMEML>' + '\n\n')
            # print('.....')


def main():
    word_sentence = read_data('../event/event_dp.txt')
    text = read_data('../data/event_22_raw.txt')
    # print(read_data('../event/event_dp_cluster.txt'))
    cluster = eval(read_data('../event/event_dp_cluster.txt')[0])
    print(cluster)
    word_line = []
    for word in word_sentence:
        line = list(set(word.strip().split(',')))
        word_line.append(line)

    print(word_line)
    format_event('../data/event/event_dp_verb_timeml.txt', text, word_line, cluster)


main()
