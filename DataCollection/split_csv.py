# SPLIT THE CSV FILE

# import the necessary libraries
import csv
import pandas as pd

# a list for all the steam ids
steamids_list = []

# enter the name of the file with all the stema ids
steamids_csv = input('Enter the steamids file in the csv format: ')

# enter the per number
per_number = int(input('Enter the number of steam ids you want to have per one csv file: '))

# read the csv file
df = pd.read_csv(steamids_csv)

# append all steam ids to the list 
for steamid in df['steamid']:
    steamids_list.append(steamid)

# a function that splits a list into chunks
def chunks(lst, n):

    # yield successive n-sized chunks from lst
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# a list of split (divided) steam ids
split_csv = list(chunks(steamids_list, per_number))

# naming files
file_i = 0

# take each chunk and add each steam id from that chunk to a csv file
for steamids in split_csv: 
        file_i += 1
        filename = f'steamids_part_{file_i}.csv'
        with open(filename, 'w', newline='') as f:
            thewriter = csv.writer(f)

            thewriter.writerow(['steamid'])

            for steamid in steamids:
                thewriter.writerow([steamid])