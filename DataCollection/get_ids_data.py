# GET THE STEAM IDS DATA

# import the neccessary libraries
import json
import requests
import operator
import pandas as pd
import time
import stdiomask

# enter the steamid file in the csv format
steamids_file = input('Enter the steamids file in the csv format: ')

# enter the output file in the json format
output_file = input('Enter the output file in the json format: ')

# enter the API key
apikey = stdiomask.getpass(prompt='Enter the API key: ', mask='*')

# enter the request limit
request_limit = int(input('Enter the request limit: '))

# for the while loop
keep_running = True

# count the number of requests
request_count = 0

# request the dictionary where each key is the app id, each value is the name of the game (app id)
data_1 = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/').json()

# list of the numbers of scanned steam ids
steamids_scanned = []

# create a list for storing all of the app ids and their names respectively
game_appid = []
game_name = []

games = data_1['applist']['apps']

for game in games:
    g_appid = game['appid']
    g_name = game['name']
    game_appid.append(g_appid) # app ids
    game_name.append(g_name) # names of app ids

# create a dictionary where keys are app ids, values are names of the app ids
appid_name = dict(zip(game_appid, game_name))

# create a dictionary, where the keys are the steam ids, and the values are app ids of the steam ids
steamid_game_list = dict()
game_list = []

# read the csv file with all steam ids
df = pd.read_csv(steamids_file)

# run the while loop
while keep_running:

    # loop through each steam id
    for steamid in df['steamid']:
        
        # try to request the list of owned games
        # if too many requests is sent, wait for 60 seconds and try again
        while True:
            try:
                data_2 = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={apikey}&steamid={steamid}&format=json').json()
                request_count += 1

                # print the number of sent requests
                # so i know how many is left
                print('Requests sent: '+str(request_count)+'')
                break
            except Exception:
                print('Connection refused by the server...')
                print('Trying again...')
                time.sleep(60)
                print()

        # if the request count is greater or equal to request_limit, break the while loop and the for loop
        # else, continue
        if request_count >= request_limit:
            keep_running = False
            break

        # try to request the lists of games of the steam user; 
        # if the game list is private, continue the loop
        try:

            games = data_2['response']['games']

            # show whether the profile is public or not
            # so, i can know whether the script is working or not
            print('Public: '+str(steamid)+'')
        
            # convert each app id to the name of the game
            for game in games:
                appid = game['appid']

                # try to convert the app id
                # if the app id is inconvertible, continue the loop 
                try:
                    game_name = appid_name[appid]
                    game_list.append(game_name)
                except Exception:
                    continue

            # update the dictionary
            # key: steam id
            # value: the list of owned games of the steam id
            steamid_game_list.update({steamid: game_list})

            # empty the game_list for the next steam id
            b = game_list
            game_list = []
                    
        except Exception:

            # show whether the profile is public or not
            # so, i can know whether the script is working or not
            print('Private: '+str(steamid)+'')
            pass

        # print the number of scanned steam ids
        # so i can track what's going on
        print('Steam ids scanned: '+str(len(set(steamid_game_list.keys())))+'')
        print()

        steamids_scanned.append(len(set(steamid_game_list.keys())))

        # if 100 steam ids are 'private' consecutively
        # break everything and save the json file
        try:
            if steamids_scanned[-1] == steamids_scanned[-100]:
                keep_running = False
                break
        except Exception:
            pass 

    break

# save the dictionary in the json format
with open(output_file, 'w') as f:
    json.dump(steamid_game_list, f, indent=2)