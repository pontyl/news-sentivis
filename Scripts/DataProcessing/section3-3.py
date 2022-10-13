import pandas as pd
#from sys import exit
#import numpy as np
#import csv
from pathlib import Path
import os
#import time
from datetime import datetime
#import matplotlib.ticker as ticker
import seaborn
#import math
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# 'cgtn' or 'chinadaily' or 'globaltimes' or 'xinhuanet'
news = "xinhuanet"
#news = "bbc"

plt.rcParams['figure.dpi'] = 800
plt.rcParams['savefig.dpi'] = 800

seaborn.set(style = 'darkgrid')

paths = sorted(Path("./" + news).iterdir(), key=os.path.getmtime, reverse=True)

data_china = pd.DataFrame()
data_world = pd.DataFrame()

#columns = ['UK', 'WORLD']
columns = ['CHINA', 'WORLD']

for c in columns:
    data = pd.DataFrame()
    print(c)

    fileList = []
    
    for p in paths:
        temp_str = str(p)
        if temp_str.find(c) != -1:
            fileList.append(str(p))
    
    fileList.reverse()
    for filename in fileList:
        df = pd.read_csv(filename, header = None)
    
        df.columns = ['Time', 'Title']
    
        df = df.dropna().reset_index(drop=True)
        
        # formatting date
        if news == "xinhuanet":
            for i in range(0, len(df)):
                df['Time'][i] = df['Time'][i][0:10]
                df['Time'][i] = datetime.strptime(df['Time'][i], '%Y-%m-%d')

        if news == "globaltimes":
            for i in range(0, len(df)):
                df['Time'][i] = df['Time'][i][11:23]
                df['Time'][i] = datetime.strptime(df['Time'][i], '%b %d, %Y')
    
        if news == "chinadaily":
            for i in range(0, len(df)):
                df['Time'][i] = df['Time'][i][9:19]
                df['Time'][i] = datetime.strptime(df['Time'][i], '%Y-%m-%d')
    
        if news == "cgtn":
            for i in range(0, len(df)):
                df['Time'][i] = df['Time'][i][7:]
                df['Time'][i] = datetime.strptime(df['Time'][i], '%d-%b-%Y')
            
        if news == "bbc":
            for i in range(0, len(df)):
                df['Time'][i] = df['Time'][i][0:10]
                df['Time'][i] = datetime.strptime(df['Time'][i], '%Y-%m-%d')
                
        data = pd.concat([data, df], axis = 0)
    
    data = data.drop_duplicates()
    data = data.reset_index(drop=True)
    
    
    for i in range(0, len(data)):
        title = data['Title'][i]
        vs = analyzer.polarity_scores(title)
        data['Title'][i] = vs['compound']
    
    polarity = []
    for i in range(0, len(data)):
        if data['Title'][i] > 0:
            polarity.append(1)
        elif data['Title'][i] < 0:
            polarity.append(-1)
        else:
            polarity.append(0)
    
    data = pd.concat([data, pd.Series(polarity)], axis = 1)
    data['Time'] = data['Time'].astype("string")
    data.columns = [*data.columns[:-1], 'P']
    
    #if c == 'UK':
    if c == 'CHINA':
        data_china = data
    if c == 'WORLD':
        data_world = data

# plot World or China column
g1 = seaborn.histplot(x=data_china['Time'], hue=data_china['P'], kde=True, multiple="fill", palette=seaborn.color_palette("ch:s=-.2,r=.4", as_cmap=True))
g1.set(xticklabels=[])

#g2 = seaborn.histplot(x=data_world['Time'], hue=data_world['P'], kde=True, multiple="fill", palette=seaborn.color_palette("ch:s=-.2,r=.4", as_cmap=True))
#g2.set(xticklabels=[])

plt.legend(title='Polarity', labels=['Positive', 'Neutral', 'Negative'])

plt.xlabel("Publish Day")
plt.ylabel("Percentage")
plt.show()
