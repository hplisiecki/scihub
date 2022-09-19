import pandas as pd
import re
import mechanize


browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.addheaders = [('User-agent', 'Firefox')]
# import excel file in utf-8
articles = pd.read_excel('Corrected.ScienceStatus.18.9.xlsx')

# drop duplicates
articles_unique = articles.drop_duplicates(subset=['article.id'])



journals = ['Journal of personality and social psychology', 'Journal of Personality and Social Psychology', 'Journal of personality and Social Psychology', 'Psychological science', 'Psychological Science', 'Personality and Social Psychology Bulletin','Personality and social psychology bulletin' , 'Personality and social psychology Bulletin', "Journal of experimental social psychology", "Journal of Experimental Social Psychology"]

# drop nans from article_unique['citation']
articles_unique = articles_unique.dropna(subset=['citation'])
titles = []
for text in articles_unique['citation']:
    pres = False
    for i in journals:
        if i in text:
            pres = True
            # find text before "i"
            a = re.findall(fr'\).*?{i}', text)
            a = a[0].split('.')
            a.pop()
            a.pop(0)
            a = ' '.join(a)
            a = a.lstrip().rstrip() + '.'
            titles.append(a)
    if pres == False:
        # count in text
        if text.count('(') == 1:
            a = text.split(').')
            a = a[1]
            a = a.lstrip().rstrip()
            titles.append(a)
        elif text.count('(') == 2:
            # find text after ').' and before '('
            a = re.findall(r'\).*?\(', text)[0]
            a.replace(').', '')
            a = a.split('.')
            a = a[1]
            a = a.replace('(', '')
            a = a.lstrip().rstrip()
            a = a + '.'
            titles.append(a)




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






