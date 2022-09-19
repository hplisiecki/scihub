
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import pandas as pd
import os


articles = pd.read_excel('Corrected.ScienceStatus.18.9.xlsx')

# drop duplicates
articles_unique = articles.drop_duplicates(subset=['article.id'])

articles_unique = articles_unique.dropna(subset=['citation'])

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

unavailable = []
for id in articles_unique['article.id']:
    # check if the file already exists
    if not os.path.isfile('articles/' + str(id) + '.txt'):
        print(id)
        try:
            text = convert_pdf_to_txt('articles/' + str(id) + '.pdf')
            new = ''
            for line in text.split('\n'):
                if len(line) < 2:
                    continue
                new += line + '\n'
            # save to file using utf-8
            with open('articles/' + str(id) + '.txt', 'w', encoding='utf-8') as f:
                f.write(new)
        except:
            print('unavailable')
            unavailable.append(id)

a = convert_pdf_to_txt('articles/' + str(id) + '.pdf')
# save new
with open('txt/1.txt', 'w') as f:
    f.write(new)