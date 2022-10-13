import pandas as pd
import numpy as np
#import csv
from pathlib import Path
import os
import seaborn
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

plt.rcParams['figure.dpi'] = 800
plt.rcParams['savefig.dpi'] = 800

# 'cgtn' or 'chinadaily' or 'globaltimes' or 'xinhuanet'
news = "xinhuanet"
#news = "bbc"
paths = sorted(Path("./" + news).iterdir(), key=os.path.getmtime, reverse=True)

# Store processed data of China column and World column
data_china = pd.DataFrame()
data_world = pd.DataFrame()

columns = ['CHINA', 'WORLD']
#columns = ['UK', 'WORLD']

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
        
        df = df.drop(columns=['Time'])
    
        df = df.dropna().reset_index(drop=True)
            
        data = pd.concat([data, df], axis = 0)
    
    data = data.drop_duplicates()
    data = data.reset_index(drop=True)
    
    
    for i in range(0, len(data)):
        title = data['Title'][i]
        vs = analyzer.polarity_scores(title)
        data['Title'][i] = vs['compound']
    
    #print(len(data))
    data.columns = ['score']
    if c == 'CHINA':
    #if c == 'UK':
        data_china = data
        data_china = pd.concat([data_china, pd.Series("China", index=range(data_china.shape[0]))], axis=1)
    if c == 'WORLD':
        data_world = data
        data_world = pd.concat([data_world, pd.Series("World", index=range(data_world.shape[0]))], axis=1)


data_total = pd.concat([data_china, data_world], axis=0)
data_total = data_total.reset_index(drop=True)
data_total.columns = [*data_total.columns[:-1], 'L']

# remove sentiment score = 0
data_total.replace(0.0, np.nan, inplace=True)

#data_total = data_total[data_total.score != 0.0]
#data_total = data_total.reset_index(drop=True)

# draw graph
seaborn.set(style = 'darkgrid')

seaborn.swarmplot(x = 'L', y = 'score', data = data_total, size = 0.15, linewidth=0.3,edgecolor='white')

seaborn.violinplot(x = "L", y = 'score', data = data_total, inner = None, scale='count')

plt.xlabel("News Column")

plt.ylabel("Sentiment Score")

plt.show()
