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