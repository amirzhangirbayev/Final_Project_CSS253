# GET AS MUCH STEAM IDS AS POSSIBLE

# import the neccessary libraries
import json
import requests
import csv
import time
import stdiomask

# enter the API key
apikey = stdiomask.getpass(prompt='Enter the API key: ', mask='*')

# enter the root steam id
root_steamid = input('Enter the root steam id: ')

# enter the request limit
request_limit = int(input('Enter the request limit: '))

# enter the output file in the csv format
output_file = input('Enter the output file in the csv format: ')

# for the while loop
keep_running = True

# count the number of requests
request_count = 0

# a list of steam ids
steamids = []

# request the freind list of the Steam User in json format using GetFriendList method
data_1 = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={apikey}&steamid={root_steamid}&relationship=friend').json()
request_count += 1

# get the stats of each friend in the friend list
friends_steamids_1 = data_1['friendslist']['friends']

# run the while loop
while keep_running:

    # loop through each friend in the friend list
    for friend in friends_steamids_1:
        
        # get the steam id of the friend
        steamid_1 = friend['steamid']

        # append the steam id of the friend
        steamids.append(steamid_1) 

        # print the total number of unique steam ids
        # so i can track what's going on
        print(len(set(steamids)))

        # try to request the friend list of the friend
        # if too many requests is sent, wait for 60 seconds and try again
        while True:
            try:
                data_2 = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={apikey}&steamid={steamid_1}&relationship=friend').json()
                request_count += 1

                # print the number of sent requests
                # so i know how many is left
                print('Requests sent: '+str(request_count)+'')
                break
            except Exception:
                print('Connection refused by the server...')
                print('Trying again...')
                time.sleep(60)
            
        # if the request count is greater or equal to request_limit, break the while loop and the for loop
        # else, continue
        if request_count >= request_limit:
            keep_running = False
            break

        # if the friend list is public, get the friend list
        # else, continue the loop
        if 'friendslist' in data_2:
            
            friends_steamids_2 = data_2['friendslist']['friends']
            for friend in friends_steamids_2:
                steamid_2 = friend['steamid']
                steamids.append(steamid_2)

                print(len(set(steamids)))
            
                while True:
                    try:
                        data_3 = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={apikey}&steamid={steamid_2}&relationship=friend').json()
                        request_count += 1
                        print('Requests sent: '+str(request_count)+'')
                        break
                    except Exception:
                        print('Connection refused by the server...')
                        print('Trying again...')
                        time.sleep(60)

                if request_count >= request_limit:
                    keep_running = False
                    break

                if 'friendslist' in data_3:
                
                    friends_steamids_3 = data_3['friendslist']['friends']
                    for friend in friends_steamids_3:
                        steamid_3 = friend['steamid']
                        steamids.append(steamid_3)

                        print(len(set(steamids)))

                        while True:
                            try:
                                data_4 = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={apikey}&steamid={steamid_3}&relationship=friend').json()
                                request_count += 1
                                print('Requests sent: '+str(request_count)+'')
                                break
                            except Exception:
                                print('Connection refused by the server...')
                                print('Trying again...')
                                time.sleep(60)

                        if request_count >= request_limit:
                            keep_running = False
                            break

                        if 'friendslist' in data_4:
                        
                            friends_steamids_4 = data_4['friendslist']['friends']
                            for friend in friends_steamids_4:
                                steamid_4 = friend['steamid']
                                steamids.append(steamid_4)

                                print(len(set(steamids)))
                        
                        else:
                            continue

                else:
                    continue
                
        else:
            continue

    break

# remove all the dublicates
setlist_steamids = list(set(steamids))

# print the total number of unique steam ids
print(len(setlist_steamids))

# add all the steam ids to the csv file
with open(output_file, 'w', newline='') as f:
    thewriter = csv.writer(f)
    
    thewriter.writerow(['steamid'])

    for steamid in setlist_steamids:
        thewriter.writerow([steamid])