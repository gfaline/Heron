import json
import datetime
from scipy.spatial import distance
from difflib import SequenceMatcher


def string_similarity(str_1, str_2):
    str_1 = list(str_1)
    str_2 = list(str_2)

    return 1 - distance.hamming(str_1, str_2)


def find_common_name(str_1, str_2):
    match = SequenceMatcher(None, str_1, str_2).find_longest_match(0, len(str_1), 0, len(str_2))
    return str_1[match.a:match.a + match.size]


def periodicity(transactions, names):
    times = {}
    groups = {}

    for name in names:
        for transaction in transactions:
            if name in transaction["description"]:
                # date = datetime.datetime(transaction["date"])
                date = datetime.datetime(int(transaction["date"].split("-")[0]), int(transaction["date"].split("-")[1]), int(transaction["date"].split("-")[2]))
                if name in times:
                    times[name].append(date)
                    groups[name].append(transaction)
                else:
                    times[name] = [date]
                    groups[name] = [transaction]
    recurring = []
    for name in times:
        time_differences = []
        if len(times[name]) > 2:
            for i in range(len(times[name]) - 1):
                time_differences.append((times[name][i + 1] - times[name][i]).days)

            daily = all(difference >= 1 and difference < 2 for difference in time_differences)
            weekly = all(difference >= 5 and difference < 9 for difference in time_differences)
            monthly = all(difference >= 21 and difference < 39 for difference in time_differences)

            if daily or weekly or monthly:
                recurring.append(groups[name])
    print(recurring)
    print(len(recurring))
    return recurring


def identify_recurring_transactions(transactions):
    # Identify Names
    identify_descriptors = {}
    for item in transactions:
        # print("Current Transaction Name: ", item['description'])
        identifiers = list(identify_descriptors.keys())
        added = False
        for attempt in identifiers:
            common_name = find_common_name(item['description'], attempt)
            if common_name == attempt:
                # print("Common name is already a key: " + common_name)
                identify_descriptors[common_name].append(item)
                added = True
                break
            elif len(common_name)/len(item['description']) >= .6:
                # print("Good Common Name Found: " + common_name)
                # print(identify_descriptors[attempt])
                temp = identify_descriptors[attempt]
                temp.append(item)
                identify_descriptors[common_name] = temp
                added = True
                identify_descriptors.pop(attempt)
                break
        if not added:
            # print("Adding new key " + item['description'])
            identify_descriptors[item['description']] = [item]
    # print(identify_descriptors)
    # print(len(list(identify_descriptors.keys())))
    events = periodicity(transactions, list(identify_descriptors.keys()))
    return events


def main():
    with open('example.json') as f:
        data = json.load(f)

    events = identify_recurring_transactions(data['transactions'])


if __name__ == '__main__':
  main()

