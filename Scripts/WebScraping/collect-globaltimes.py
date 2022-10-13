from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import csv

column = "china"

url = "https://www.globaltimes.cn/%s/index.html"%(column.lower())

req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
links = []
for link in soup.find_all('a'):
   links.append(link.get('href'))

nplinks = np.array(links)
nplinks = nplinks.astype('<U200')
nplinks = nplinks[nplinks != np.array(None)]
nplinksUniques = np.unique(nplinks)
nplinksUniques2 = nplinksUniques[np.char.startswith(nplinksUniques, 'http')]
nplinksUniques3 = nplinksUniques2[np.char.endswith(nplinksUniques2, 'html')]

print("GlobalTimes")
print(time.ctime())
print("Num of Headlines: " + str(len(nplinksUniques3)))

file_name = str(time.ctime())
file_name = file_name.replace(" ", "-")
file_name = file_name.replace(":", "_")

file_name = file_name + "-%s"%(column.upper())
file_name = file_name + ".csv"
file_name = "GlobalTimes-" + file_name

i = 0
for ArticleUrl in nplinksUniques3:
    try:
        req2 = requests.get(ArticleUrl)
        soup2 = BeautifulSoup(req2.content, "html.parser")
        
        divContent = soup2.find('div', {'class':"article_title"})
        title = divContent.string
        
        spanContent = soup2.find('span', {'class':"pub_time"})
        publishTime = spanContent.string
        
        a = [publishTime, title]
        with open(file_name, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(a)
            
        time.sleep(0.1)
        
        print(i)
        i += 1
    except:
        print("Invalid Link in " + str(i))
        i += 1
        pass

print("Done")