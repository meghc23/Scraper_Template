
import unittest, time, random
import urllib.request
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import pandas as pd

links = []
imgs = []
website = "https://www.(website_name).com"

rate = [i/10 for i in range(10)]
cnt = 0

quote = '"'
newline = '\n'
colon = ' : '


browser = webdriver.Firefox(executable_path="C:\\Users\\meghc\\.wdm\\drivers\\geckodriver\\win64\\v0.29.1\\geckodriver.exe")

browser.get("") # Website subpage link
content = browser.page_source
soup1 = BeautifulSoup(content, "html.parser")

for main in soup1.findAll('div', attrs = {'class' : 'product-item'}):
    name=main.find('a', href=True)
    if (name != ''):
        links.append((name.get('href')).strip())
    imgl = main.find('img', src=True)
    if (imgl != ''):
        imgs.append((imgl.get('src')).strip())


print("Got imgs : ", len(imgs))
print("Got links : ", len(links))

for link in links:
    
    #just for testing 10 links
    cnt = cnt + 1
    #if cnt > 3:
     #   break
    

    print("Fetching link..... : ", link)
    # time delay before we access the next page..
    time.sleep(random.choice(rate))

    link = website + link
    browser.get(link)
    linkcontent = browser.page_source
    soup = BeautifulSoup(linkcontent, "html.parser")

    pname = soup.find('h1', attrs = {'class' : 'product-name'})
    if not pname:
        print("Error no product name for link : ", link)
        continue

    modelnum = soup.find('p', attrs = {'class' : 'product-code'})
    if not modelnum:
        print("Error on model number for link : ", link)
        continue

    n = soup.find('div', attrs={'class' : 'product-price'})
    price = n.find('span')
    if not price:
        print("Error on price for link : ", link)
        continue


    # create a file with the model number - specific to this site the model num is 10 chars
    fname = modelnum.text.strip()[0:10]+".txt"
    ff = open(fname, mode='w', encoding="utf-8")
    ff.write("NAME : " + quote + pname.text.strip() + quote + newline)
    ff.write("MODEL : " + quote + modelnum.text.strip() + quote + newline)
    ff.write('Link :' + quote + link + quote + newline)
    ff.write("Image : " + quote + imgs[cnt-1] + quote + newline)
    urllib.request.urlretrieve(imgs[cnt-1], modelnum.text.strip() + '.jpg')
    ff.write("Price : " + quote + price.text.strip() + quote + newline)

    for sd in soup.findAll('section', attrs = {'id' : 'productspecifications'}):
        for m in sd.findAll('div', attrs = {'class' : 'specifications-list'}):
            g = m.find('h3')
            if not g:
                print("Error in group in link : ", link)
                continue

            ff.write("GROUP : " + quote + g.text.strip() + quote + newline )
            
            for ss in m.findAll('ul'):
                for tt in ss.findAll('li'):
 
                    answer=tt
                    if not answer:
                        print("Error P not found")
                        continue

                    answer = answer.text.strip()
                    answer = answer.replace("\t","")
                    answer = answer.replace("\n"," ")

                    ff.write(quote + answer + quote  + newline)


browser.close()
exit()
