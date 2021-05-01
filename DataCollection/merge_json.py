# MERGE TWO JSON FILES INTO ONE

# import the necessary libraries
import json

# enter the names of the files
file1 = input('Enter the name of the first json file: ')
file2 = input('Enter the name of the second json file: ')

# enter the name of the output file
output_file = input('Enter the name of the output file: ')

# open the files
with open(file1, 'r') as f1:
    dict1 = json.load(f1)
with open(file2, 'r') as f2:
    dict2 = json.load(f2)

# merge the files
dict3 = {**dict1, **dict2}

# output the merged file in the json format
with open(output_file, 'w') as f:
    json.dump(dict3, f, indent=2)