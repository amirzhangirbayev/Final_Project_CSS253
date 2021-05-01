# GET THE NODES TABLE

# import the necessary libraries
import json
from collections import Counter
import csv
import pandas as pd

# enter the ids data file in the json format
ids_data = input('Enter the ids data file in the json format: ')

# enter the edges file in the csv format
edges_file = input('Enter the edges file in the csv format: ')

# enter the output (nodes) file in the csv format
output_file = input('Enter the output (nodes) file in the csv format: ')

# list for all games from steam users
all_games = []

# open and load the json file 
with open(ids_data, 'r') as f:
    data = json.load(f)

    # add all games of steam users
    for game_list in list(data.values()):
        for games in game_list:
            all_games.append(games)

# count the games
nodes = dict(Counter(all_games))

# load the edges table
df_edges = pd.read_csv(edges_file)

# a list for all the games from the edges table
sources_targets = []

# append all the games from the edegs table to the list
for source in df_edges['Source']:
    sources_targets.append(source)
for target in df_edges['Target']:
    sources_targets.append(target)

# loop through each game in the nodes dict
for game in list(nodes.keys()):

    # if the game from the nodes dict is in the list from the edges table, pass
    # else, delete the game from the nodes dict
    if game in set(sources_targets):
        pass
    else:
        del nodes[game] 

# sort the dictionary in ascending order
nodes_sorted = dict(sorted(nodes.items(), key=lambda item: item[1], reverse=True))

# save the dictionary to a csv file
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(['ID', 'Label', 'Count'])

    for key, value in list(nodes_sorted.items()):
        writer.writerow([key, key, value])