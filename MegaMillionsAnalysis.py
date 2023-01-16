# -*- coding: utf-8 -*-
"""
A brief analysis of Mega Millions Past Numbers as published by the Virginia 
Lottery (https://www.valottery.com/api/v1/downloadall?gameId=15).
"""

__license__ = 'cc-by-sa-4.0'
__author__ = 'Decaff42'
__date__ = '15 January 2023'


import os
import matplotlib.pyplot as plt
import pandas as pd

# Get the current location of the script and the location of the raw data
cwd = os.getcwd()
filename = 'MegaMillions_1_11_2023.txt'
source_data_file = os.path.join(cwd, filename)

# Import the raw data as a list of lists with no \n character at the end and 
# remove the comment/header lines at the beginning and end of the file
raw_data = list()
with open(source_data_file, mode='r') as txt_file:
    raw_data = [line.rstrip() for line in txt_file][2:-3]

# Split out the data for each line accounting for mulitple delimiters
data = list()
for line in raw_data:
    for delimiter in ['; ', ': ']:
        line = line.replace(delimiter, ',')
    line = line.split(',')
    del line[6]  # Remove the "Mega Ball" label in the line.
    data.append(line)

# Store data in a dataframe
headers = ['Date', '1', '2', '3', '4', '5', 'MegaBall']
df = pd.DataFrame(data, columns=headers, dtype=int)

# Convert date to datetime objects and set as index
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
df.set_index(keys='Date', inplace=True)

# Convert data from string to integers
for col in df.columns:
    df[col] = df[col].astype(int)

# Count occurances of values in the various columns
counts = list()
for col in ['1', '2', '3', '4', '5', 'MegaBall']:
    counts.append(df[col].value_counts())

# Arrange data by ball value 
plot_data = list()
for ballvalue in range(1, 71):
    line = [ballvalue]
    for group in counts:
        if ballvalue in group.index:
            line.append(group[ballvalue])
        else:
            line.append(0)
    
    line.append(sum(line[1:]))
    plot_data.append(line)

# Store ball-specific data into df
plot_df = pd.DataFrame(plot_data, columns=['Value', 'Ball1', 'Ball2', 'Ball3', 'Ball4', 'Ball5', 'MegaBall', 'All Time'])
plot_df.set_index('Value', inplace=True)

# Calculate the percentage of draws each ball has been a number
percent_df = plot_df.copy(deep=True)
for col in percent_df:
    if col != 'All Time':
        percent_df[col] = percent_df[col] / len(df.index) * 100
    else:
        percent_df[col] = percent_df[col] / (6 * len(df.index)) * 100
    
# Make the plot with all the data from plot_df
cols = plot_df.columns
labels = ['Ball 1', 'Ball 2', 'Ball 3', 'Ball 4', 'Ball 5', 'Mega Ball', 'All Positions']
for col, legend in zip(cols, labels):
    plt.plot(percent_df[col], label=legend)

# Handle Plot admin
plt.title('Mega Millions Historical Numbers')
plt.ylabel('Percent Chance')
plt.xlabel('Ball Number')
plt.legend(loc='best',ncol=3)
plt.grid(True)
plt.show()
