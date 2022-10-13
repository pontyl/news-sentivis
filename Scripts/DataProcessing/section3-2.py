import pandas as pd
#from sys import exit
import numpy as np
#import csv
from pathlib import Path
import os
import seaborn
#import math
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

plt.rcParams['figure.dpi'] = 800
plt.rcParams['savefig.dpi'] = 800

plt.ylim(-1.0, 1.0)

seaborn.set(style = 'darkgrid')

# 'cgtn' or 'chinadaily' or 'globaltimes' or 'xinhuanet'
news = "xinhuanet"
#news = "bbc"
paths = sorted(Path("./" + news).iterdir(), key=os.path.getmtime, reverse=True)

fileList = []

for p in paths:
    temp_str = str(p)
    #if temp_str.find("UK") != -1:
    if temp_str.find("CHINA") != -1:
        fileList.append(str(p))

scores_china = pd.DataFrame()

scores_china2 = pd.DataFrame()

j = 0

fileList.reverse()
for filename in fileList:
    df = pd.read_csv(filename, header = None)

    df.columns = ['Time', 'Title']

    df = df.dropna().reset_index()
    
    score = []

    for i in range(0,len(df)):
        title = df['Title'][i]
        vs = analyzer.polarity_scores(title)
        score.append(vs['compound'])
        
    #scores_china[j] = pd.Series(score)
    scores_china = pd.concat([scores_china, pd.Series(score)], axis=1)
    
    temp = pd.DataFrame()
    temp = pd.concat([temp, pd.Series(score)], axis=1)
    
    index = [j] * len(score)
    j += 1
    temp = pd.concat([temp, pd.Series(index)], axis=1)
    
    scores_china2 = pd.concat([scores_china2, temp], axis=0)
    
scores_china.columns = range(scores_china.shape[1])

#-----------------------------------------------------------------------------------------------

fileList = []

for p in paths:
    temp_str = str(p)
    if temp_str.find("WORLD") != -1:
        fileList.append(str(p))

scores_world = pd.DataFrame()

scores_world2 = pd.DataFrame()

j = 0

fileList.reverse()
for filename in fileList:
    df = pd.read_csv(filename, header = None)

    df.columns = ['Time', 'Title']

    df = df.dropna().reset_index()
    
    score = []

    for i in range(0,len(df)):
        title = df['Title'][i]
        vs = analyzer.polarity_scores(title)
        score.append(vs['compound'])
        
    #scores_world[j] = pd.Series(score)
    scores_world = pd.concat([scores_world, pd.Series(score)], axis=1)
    
    temp = pd.DataFrame()
    temp = pd.concat([temp, pd.Series(score)], axis=1)
    
    index = [j] * len(score)
    j += 1
    temp = pd.concat([temp, pd.Series(index)], axis=1)
    
    scores_world2 = pd.concat([scores_world2, temp], axis=0)

scores_world.columns = range(scores_world.shape[1])

# ----------------------------------------------------------
# scatter plot

scores_china2 = scores_china2.reset_index(drop=True)
scores_world2 = scores_world2.reset_index(drop=True)

scores_china2.columns = ['score','day']
scores_world2.columns = ['score','day']

# Modify this line to choose plot 'China' or 'World' column
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#scoreplot = scores_china2
scoreplot = scores_world2
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

scoreplot['c'] = abs(scoreplot['score'])

plt.scatter(x = scoreplot['day'], y = scoreplot['score'], s=1.5, c='dimgray', alpha=scoreplot['c'])

# Modify this line to choose plot 'China' or 'World' column
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#scoreplot = scores_china
scoreplot = scores_world
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

scoreplot_T = scoreplot.transpose()
index = [*range(0, scoreplot_T.shape[0])]

# average score
scoreplot_copy = scoreplot.copy()
scoreplot_copy_T = scoreplot_copy.transpose()
scoreplot_copy_T['avg'] = scoreplot_copy_T.mean(numeric_only = True, axis = 1)
scoreplot_copy_T = pd.concat([scoreplot_copy_T, pd.Series(index)], axis = 1)

scoreplot_copy_T.columns = [*scoreplot_copy_T.columns[:-1], 'T']

seaborn.lineplot(x = 'T', y = 'avg', data = scoreplot_copy_T, palette = "YlGnBu_d")
plt.scatter(x = scoreplot_copy_T['T'], y = scoreplot_copy_T['avg'], s = 3)

# ---------------------------------------
# average without zero values

scoreplot_TT = scoreplot.transpose()
means = []

for i in range(0, scoreplot_TT.shape[0]):
    r = scoreplot_TT.iloc[i]
    rr = np.array(r)
    mean = np.nanmean(rr[rr.nonzero()])
    means.append(mean)
scoreplot_TT = pd.concat([scoreplot_TT, pd.Series(means)], axis=1)
scoreplot_TT.columns = [*scoreplot_TT.columns[:-1], 'avg_nan']
scoreplot_TT = pd.concat([scoreplot_TT, pd.Series(index)], axis = 1)
scoreplot_TT.columns = [*scoreplot_TT.columns[:-1], 'T']

g = seaborn.lineplot(x = 'T', y = 'avg_nan', data = scoreplot_TT, palette = "YlGnBu_d")
p = plt.scatter(x = scoreplot_TT['T'], y = scoreplot_TT['avg_nan'], s = 3)


plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off

plt.axhline(0.0, color ='black', linestyle =":")
plt.xlabel("Day")
plt.ylabel("Sentiment Score")