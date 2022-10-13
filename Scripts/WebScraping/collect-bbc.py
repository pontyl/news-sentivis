from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import csv

column = "WORLD"

url = "https://www.bbc.co.uk/news/%s"%(column.lower())

req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")
links = []
for link in soup.find_all('a'):
   links.append(link.get('href'))

nplinks = np.array(links)
nplinks = nplinks.astype('<U200')
nplinks = nplinks[nplinks != np.array(None)]
nplinksUniques = np.unique(nplinks)
#suffix_string = "/news/" + column + "-"
nplinksUniques2 = nplinksUniques[np.char.startswith(nplinksUniques, "/news/uk-")]
nplinksUniques3 = nplinksUniques[np.char.startswith(nplinksUniques, "/news/world-")]
nplinksUniques4 = np.concatenate((nplinksUniques2, nplinksUniques3))

print("BBC")
print(time.ctime())
print("Num of Headlines: " + str(len(nplinksUniques4)))

file_name = str(time.ctime())
file_name = file_name.replace(" ", "-")
file_name = file_name.replace(":", "_")

file_name = file_name + "-%s"%(column.upper())
file_name = file_name + ".csv"
file_name = "BBC-" + file_name

for ArticleUrl in nplinksUniques4:
    req2 = requests.get('https://www.bbc.co.uk' + ArticleUrl)
    soup2 = BeautifulSoup(req2.content, "html.parser")
    
    headerContent = soup2.find('h1')
    title = headerContent.string
    
    spanContent = soup2.find('time')
    publishTime = spanContent['datetime']
    
    a = [publishTime, title]
    with open(file_name, 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(a)
    print(title)