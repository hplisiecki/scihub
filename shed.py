DOI_REGEX = "doi.+(10\\.\d{4,6}/[^\"'&<% \t\n\r\f\v]+)"


def google_title_to_doi(title):

    try:
        return find_doi(str(sourcecode))
    except:
        pass

def find_doi(sourcecode):
    '''
    Look for a Digital Object Identifier (DOI) in the sourcecode
    of an HTML page.
    @param sourcecode: the sourcecode as a string.
    '''
    return re.findall(DOI_REGEX, sourcecode, re.I)[0]


def google_title_to_doi(title):
    browser.open("http://scholar.google.com/")
    assert browser.viewing_html()
    browser.select_form(nr=1)
    browser["q"] = 'intitle:"{0}"'.format(title.strip())
    response = browser.submit()
    browser.follow_link(text=title.strip())
    sourcecode = browser.response().get_data()
    try:
        return find_doi(sourcecode)
    except:
        pass

browser.open('https://sci-hub.se')
browser.select_form(nr=0)
# use form
browser['request'] = 'When forgiving enhances psychological well-being: the role of interpersonal commitment.'
browser.submit()
# get result url
sourcecode = browser.page_source
sourcecode = browser.response().get_data()


br["user[username]"] = "username"



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


