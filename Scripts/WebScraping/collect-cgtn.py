from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import csv

column = "world"

url = "https://www.cgtn.com/%s"%(column.lower())

req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
links = []
for link in soup.find_all('a'):
   links.append(link.get('href'))

nplinks = np.array(links)
nplinks = nplinks.astype('<U200')
nplinks = nplinks[nplinks != np.array(None)]
nplinksUniques = np.unique(nplinks)
nplinksUniques2 = nplinksUniques[np.char.startswith(nplinksUniques, 'https://new')]
nplinksUniques3 = nplinksUniques2[np.char.endswith(nplinksUniques2, 'html')]

print("CGTN")
print(time.ctime())
print("Num of Headlines: " + str(len(nplinksUniques3)))

file_name = str(time.ctime())
file_name = file_name.replace(" ", "-")
file_name = file_name.replace(":", "_")

file_name = file_name + "-%s"%(column.upper())
file_name = file_name + ".csv"
file_name = "CGTN-" + file_name

i = 0
for ArticleUrl in nplinksUniques3:
    try:
        req2 = requests.get(ArticleUrl)
        soup2 = BeautifulSoup(req2.content, "html.parser")
        
        divContent = soup2.find('div', {'class':"news-title"})
        title = divContent.string
        
        spanContent = soup2.find('span', {'class':"date"})
        publishTime = spanContent.string
        publishTime = publishTime.replace('\n','')
        publishTime = publishTime.replace('  ','')
        
        a = [publishTime, title]
        with open(file_name, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(a)
            
        time.sleep(0.15)
        
        print(i)
        i += 1
    except:
        print("Invalid Link in " + str(i))
        i += 1
        pass

print("Done")