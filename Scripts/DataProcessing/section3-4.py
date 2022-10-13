import pandas as pd
#import numpy as np
#import csv
from pathlib import Path
#from sys import exit
import os
import seaborn as sns
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

plt.rcParams['figure.dpi'] = 800
plt.rcParams['savefig.dpi'] = 800

# 'cgtn' or 'chinadaily' or 'globaltimes' or 'xinhuanet'
news = "xinhuanet"
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
        
        df = df.drop(columns=['Time'])
    
        df = df.dropna().reset_index(drop=True)
            
        data = pd.concat([data, df], axis = 0)
    
    data = data.reset_index(drop=True)
    
    data = data['Title'].value_counts()
    data = data.reset_index(level=0)
    data = data[data.Title >= 2]
    
    data.columns = ['Title', 'Count']
    
    score = []
    for i in range(0, len(data)):
        title = data['Title'][i]
        vs = analyzer.polarity_scores(title)
        score.append(vs['compound'])
    data = pd.concat([data, pd.Series(score)], axis=1)
    
    data.columns = ['Title', 'Count', 'Score']
    
    polarity = []
    for i in range(0, len(data)):
        if data['Score'][i] > 0:
            polarity.append("Positive")
        elif data['Score'][i] < 0:
            polarity.append("Negative")
        else:
            polarity.append("Neutral")
    
    data = pd.concat([data, pd.Series(polarity)], axis = 1)
    
    data.columns = ['Title', 'Count', 'Score', 'P']
    
    data = data[data.P != "Neutral"]
    data = data.reset_index(drop=True)
    
    #if c == 'UK':
    if c == 'CHINA':
        data_china = data
        data_china = pd.concat([data_china, pd.Series(1, index=range(data_china.shape[0]))], axis=1)
        data_china.columns = ['Title', 'Count', 'Score', 'P', 'C']
        #exit()
    if c == 'WORLD':
        data_world = data
        data_world = pd.concat([data_world, pd.Series(1, index=range(data_world.shape[0]))], axis=1)
        data_world.columns = ['Title', 'Count', 'Score', 'P', 'C']


fig, axes = plt.subplots(1, 2, figsize=(14, 8))

colors = ["#69b3a2", "#b37b43"]
sns.set_palette(colors)


data_china = data_china.groupby(['Count','P']).sum()
data_china = data_china.reset_index()

data_world = data_world.groupby(['Count','P']).sum()
data_world = data_world.reset_index()

g1 = sns.barplot(
    ax=axes[0],
    x="C", 
    y="Count", 
    hue="P", 
    data=data_china, 
    ci=None,
    log=True,
    orient="h"
    )


g2 = sns.barplot(
    ax=axes[1],
    x="C", 
    y="Count", 
    hue="P", 
    data=data_world, 
    ci=None,
    log=True,
    orient="h"
    )

axes[0].set_title('China')
axes[1].set_title('World')

g1.legend(loc='lower right', title='Sentiment')
g2.legend(loc='lower right', title='Sentiment')

g1.set_ylabel("Day of Exposure")
g2.set_ylabel("Day of Exposure")

g1.set_xlabel("Number of News")
g2.set_xlabel("Number of News")
