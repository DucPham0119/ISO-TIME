import re

from bs4 import BeautifulSoup


def extract_time_texts(file_name, type_ml='timex3'):
    res_time = []
    res_time_text = []
    with open(file_name, encoding='utf8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        res_time_1 = []
        res_time_text_1 = []
        for tag in soup.find_all('timeml'):
            for t in tag.find_all(type_ml):
                attrs = t.attrs
                if 'tid' in list(attrs.keys()):
                    del attrs['tid']
                elif 'eid' in list(attrs.keys()):
                    del attrs['eid']

                text = t.text.strip()
                if type_ml == 'timex3':
                    for e in t.find_all('event'):
                        text = re.sub(r'\s+', ' ', text.replace(str(e), ' '))
                res_time_text_1.append(text)
                res_time_1.append(attrs)
            # print(res)
            res_time.append(res_time_1)
            res_time_text.append(res_time_text_1)

    return res_time, res_time_text


def count_max_matches(test_attr, gold_attr, test_text, gold_text):
    # print(len(test_attr), len(gold_attr), len(test_text), len(gold_text))
    assert len(test_attr) == len(gold_attr) == len(test_text) == len(gold_text)

    correct = 0
    for i in range(len(test_attr)):
        texts_test = test_text[i]
        texts_gold = gold_text[i]
        for j in range(len(texts_test)):
            if texts_test[j].strip() in texts_gold:
                # print(texts_test[j])
                idx = texts_gold.index(texts_test[j])
                attrs_key_test = test_attr[i][j].keys()
                attrs_key_gold = gold_attr[i][idx].keys()
                for attr in attrs_key_test:
                    if attr in attrs_key_gold and test_attr[i][j][attr] == gold_attr[i][idx][attr]:
                        correct += 1

    return correct


def get_num_attr(test_attri):
    sum_num = 0
    for i in range(len(test_attri)):
        for j in range(len(test_attri[i])):
            sum_num += len(test_attri[i][j])

    return sum_num


def evaluate(doc_gold, text_gold, doc_predict, text_predict):
    mention_gold = get_num_attr(doc_gold)
    correct_attr = count_max_matches(doc_predict, doc_gold, text_predict, text_gold)
    mention_predict = get_num_attr(doc_predict)
    precision = correct_attr / mention_predict
    recall = correct_attr / mention_gold
    # print(precision, recall)
    f1_score = 2 * precision * recall / (precision + recall)
    return {'Precision': precision, 'Recall': recall, 'F1_score': f1_score}


def test_event(gold, test):
    gold, gold_text = extract_time_texts(gold, 'event')
    predict, text = extract_time_texts(test, 'event')
    print(evaluate(gold, gold_text, predict, text))


def test_time(gold, test):
    gold, gold_text = extract_time_texts(gold)
    predict, text = extract_time_texts(test)
    print(evaluate(gold, gold_text, predict, text))


def main_event(file_true, file_gemini, file_gpt, file_rule):
    print("GEMINI")
    test_event(file_true, file_gemini)
    print("GPT")
    test_event(file_true, file_gpt)
    print("Our model")
    test_event(file_true, file_rule)


def main_time(file_true, file_gemini, file_gpt, file_heidel, file_rule):
    print("GEMINI")
    test_time(file_true, file_gemini)
    print("GPT")
    test_time(file_true, file_gpt)
    print("Heidel")
    test_time(file_true, file_heidel)
    print("Our model")
    test_time(file_true, file_rule)


if __name__ == '__main__':
    file_true = '../data/time_test.txt'
    file_time_gemini = '../data/time/gemini_1-5flash_newPrompt.txt'
    file_time_gpt = '../data/time/gpt_4o_mini_v2output.txt'
    file_time_heidel = '../data/time/heideltime_v2_output27Aug.txt'
    file_time_rule = '../data/time/heideltime_v2_output29Aug.txt'
    main_time(file_true, file_time_gemini, file_time_gpt, file_time_heidel, file_time_rule)

    file_true = '../data/gold_test.txt'
    file_event_gemini = '../data/event/event_gemini_test.txt'
    file_event_gpt = '../data/event/event_gpt_20.txt'
    file_event_rule = '../data/event/event_dp_verb_timeml.txt'
    main_event(file_true, file_event_gemini, file_event_gpt, file_event_rule)
