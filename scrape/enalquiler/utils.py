# By Carlos Davila
import re, json, grequests
from bs4 import BeautifulSoup
from urllib.request import urlopen

# with open('data/preg_completa.html', encoding="latin-1") as fp:
#     soup = BeautifulSoup(fp, "html.parser")

def EnalquilerForumScrape(soup):

    # The class that contains the info that we want is "col-md-8"
    info = soup.find(class_="col-md-8")

    # Getting all question blocks
    question_block = soup.find_all('div', class_="question-block")

    keys = ['user','user_category','question_body','question-category']
    dict = {k:[] for k in keys}

    def no_usuario(tag):
        return not re.compile('usuario').search(tag)

    dict = {k:[] for k in ['user','user_category','question_body','question_category']}

    for el in question_block:
        left_block = el.find('div', class_='pull-left')
        u = left_block.find('p', class_='user-name')
        c = left_block.find('p', class_='user-category')
        dict['user'].append(u.string)
        dict['user_category'].append(c.string)

        overflow = el.find('div', class_='overflow')
        q = overflow.find('div',class_='question-body')
        qc = overflow.find('a', {'class':False,'href':no_usuario})
        dict['question_body'].append(q.get_text().strip("\n| "))
        dict['question_category'].append(qc.string)

    return dict

# url_list = [
#     "https://www.enalquiler.com/comunidad_alquiler/preguntas_y_respuestas.html",
#     "https://www.enalquiler.com/comunidad-alquiler/todas/2"
# ]

def get_question_links(url_list):
    """
    Get all the question links in page
    """

    reqs = (grequests.get(url) for url in url_list)
    resp = grequests.imap(reqs, grequests.Pool(10))
    links = []

    for r in resp:
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a', attrs={'class':'question-expand','href':True}):
            links.append(link.get('href').strip("\n| "))

    return links
