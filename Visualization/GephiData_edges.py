# GET THE EDGES TABLE

# import the necessary libraries
import json
import itertools
from collections import Counter
import pandas as pd
import csv
import statistics

# enter the ids data file in the json format
ids_data = input('Enter the ids data file in the json format: ')

# enter the output (edges) file in the csv format
output_file_csv = input('Enter the output (edges) file in the csv format: ')

# counting the combinations
edges = {}

# a list with lengths of game_lists of each steam user
list_lengths = []

# a list with lists of average length
average_lists = []

# open the json file with all the data
with open(ids_data, 'r') as f_json:
    data = json.load(f_json)

    # counting total steam ids scanned
    i = 0

    # loading message
    print('Collecting the lengths of game_lists...')

    # collecting the lengths of game_lists of each steam user
    for game_list in list(data.values()):
        list_lengths.append(len(game_list))

    # completion message
    print('Lengths are collected successfully')

    # loading message
    print('Collecting the average game_lists...')

    # collecting the lists with the average length
    for game_list in list(data.values()):
        if len(game_list) <= statistics.mean(list_lengths):
            average_lists.append(game_list)

    # completion message
    print('Average game_lists are collected successfully')

    for game_list in average_lists:

        # getting all the possible combinations of the game_list
        combination_list = itertools.combinations(game_list, 2)

        # counting the occurences of the combinations
        for combination in combination_list:
            if frozenset(combination) in edges:
                edges[frozenset(combination)] += 1
            else:
                edges[frozenset(combination)] = 1

        # show the total steam ids scanned
        # so, i can track what's going on
        i += 1
        print(f'Steam ids scanned: {i}')

# sort the combinations in ascending order
edges_sorted = dict(sorted(edges.items(), key=lambda item: item[1], reverse=True))

combination_keys = list(edges_sorted.keys()) # for the combinations
count_values = list(edges_sorted.values()) # for the count numbers

# turn the frozensets into lists
list_combination_keys = []
for fset in combination_keys:
    list_combination_keys.append(list(fset))

# loading message
print('Writing the file...')

# add all the combinations and their values to the csv file (edges.csv)
with open(output_file_csv, 'w', encoding='utf-8', newline='') as f_out_csv:
    thewriter = csv.writer(f_out_csv)

    thewriter.writerow(['Source', 'Target', 'Weight'])

    for i in range(len(count_values)):
        source_target = list_combination_keys[i]
        weight = count_values[i]

        try:
            thewriter.writerow([source_target[0], source_target[1], weight])
        except Exception:
            continue

# save only 10000 combinations
df = pd.read_csv(output_file_csv)
df_top = df.head(10000)
df_top.to_csv(output_file_csv)
df_top.set_index('Source', inplace=True)
df_top.to_csv(output_file_csv)

# completion message
print('Done!')