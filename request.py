import requests
from bs4 import BeautifulSoup
import urllib
import os

def retrieve_all_image(page,save_path):
    res = requests.get('http://www.lg.com'+page+'/view-all',headers={'Connection':'close'}).content
    soup = BeautifulSoup(res, 'html.parser', from_encoding='utf-8')
    tags = soup.find_all('a', class_ = "img-link")
    webDir = "http://www.lg.com"
    print(save_path)
    print("")
    for tag in tags:
        try:
            print(webDir + tag.span.img['data-original'])
            urllib.request.urlretrieve(webDir + tag.span.img['data-original'], save_path +"/"+tag['href'].split('/')[-1]+".jpg")
            print(tag['href'].split('/')[-1])
        except :
            continue

if not os.path.exists('./img'):
    os.mkdir('./img')

session = requests.Session()
session.trust_env = False
res = session.get('http://www.lg.com/tw/',headers={'Connection':'close'}).content
soup = BeautifulSoup(res, 'html.parser', from_encoding='utf-8')
sections = soup.find('div', class_ = "container five-column web").find_all('section',limit = 4)
webDir = "http://www.lg.com"
baseDir = "./img/"
catagory_names = []
webDirs = []
for section in sections:
        #print(section.find_all('a',class_ = "heading"))
        for nav in section.find_all('nav'):
            for li in nav.ul.find_all('li'):
                li_name = li.get_text().replace(':','')
                catagory_save = baseDir + li_name
                catagory_save = catagory_save.replace(' ','')
                #print(catagory_save)
                catagory_names.append(catagory_save)
                if not os.path.exists(catagory_save):
                    os.mkdir(catagory_save)
                #print(webDir+li.a['href']+"  retriving~")
                webDirs.append(li.a['href'])
                #retrieve_all_image(webDir+li.a['href'],catagory_save)

num = len(catagory_names)
try:
    for i in range(num):
        print(str(i/num*100)+'%')
        retrieve_all_image(webDirs[i],catagory_names[i])
except:
    print('web error')
