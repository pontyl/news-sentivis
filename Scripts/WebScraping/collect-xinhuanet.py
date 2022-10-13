from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import csv

column = "world"

url = "https://english.news.cn/%s/index.htm"%(column.lower())

req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
links = []
for link in soup.find_all('a'):
   links.append(link.get('href'))

nplinks = np.array(links)
nplinks = nplinks.astype('<U200')
nplinks = nplinks[nplinks != np.array(None)]
nplinksUniques = np.unique(nplinks)
nplinksUniques2_1 = nplinksUniques[np.char.startswith(nplinksUniques, 'https')]
nplinksUniques2_2 = nplinksUniques[np.char.startswith(nplinksUniques, '../')]

nplinksUniques2_2_new = np.array([])
nplinksUniques2_2_new = nplinksUniques2_2_new.astype('<U200')
for url_to_modify in nplinksUniques2_2:
    url_to_modify = url_to_modify.replace('..','https://english.news.cn')
    nplinksUniques2_2_new = np.append(nplinksUniques2_2_new, url_to_modify)

nplinksUniques3 = np.concatenate((nplinksUniques2_1, nplinksUniques2_2_new))

print("Xinhuanet")
print(time.ctime())
print("Num of Headlines: " + str(len(nplinksUniques3)))

file_name = str(time.ctime())
file_name = file_name.replace(" ", "-")
file_name = file_name.replace(":", "_")

file_name = file_name + "-%s"%(column.upper())
file_name = file_name + ".csv"
file_name = "Xinhuanet-" + file_name

i = 0
for ArticleUrl in nplinksUniques3:
    try:
        req2 = requests.get(ArticleUrl)
        soup2 = BeautifulSoup(req2.content, "html.parser")
        
        divContent = soup2.find('div', {'class':"conTop"})
        h1Content = divContent.find('h1')
        title = h1Content.string
        
        spanContent = soup2.find('p', {'class':"time"})
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

for url_special in nplinksUniques3:
    if not np.char.startswith(url_special, 'https://english.news.cn/2'):
        req2 = requests.get(url_special)
        soup2 = BeautifulSoup(req2.content, "html.parser")
        
        divContent = soup2.find('h1', {'class':"Btitle"})
        title = divContent.string
        print(title)
        
        spanContent = soup2.find('i', {'class':"time"})
        publishTime = spanContent.string
        publishTime = publishTime.replace('\r','')
        publishTime = publishTime.replace('\n','')
        publishTime = publishTime.replace('  ','')
        print(publishTime)
        
        a = [publishTime, title]
        with open(file_name, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(a)

print("Done")