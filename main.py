import pandas as pd
import re
import mechanize


browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.addheaders = [('User-agent', 'Firefox')]
# import excel file in utf-8


from selenium import webdriver
from tqdm import tqdm
import time
options = webdriver.FirefoxOptions()


options.add_argument('--no-sandbox')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0')
driver = webdriver.Firefox(executable_path='D:/PycharmProjects/webdriver/geckodriver.exe' , options=options)


# If you have titles, you can get scihub pdf links using the loop below:

links = []
for number in tqdm(range(len(titles))):
    title = titles[number]
    proper = False
    while proper == False:
        try:
            browser.open('https://sci-hub.se')
            browser.select_form(nr=0)
            proper = True
        except:
            print('sleep')
            time.sleep(60)
    # use form
    browser['request'] = title
    response = browser.submit()
    links.append(browser.geturl())

# save the 'links' list
import pickle
with open('links.pkl', 'wb') as f:
    pickle.dump(links, f)

# load
with open('links.pkl', 'rb') as f:
    links = pickle.load(f)


# Then we count the number of links that failed
count = 0
for i in links:
    if i ==  'https://sci-hub.se/':
        count += 1
a = pd.DataFrame(links)
a.to_csv('links.csv', index=False)

# And use the scihub api to recover full pdfs
from scihub_api import SciHub
sh = SciHub()
for link, name in tqdm(zip(links, articles_unique['article.id'])):
    name = str(name) + '.pdf'
    result = sh.download(link, path = name, destination= 'articles/')






