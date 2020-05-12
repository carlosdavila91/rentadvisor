# By Carlos Davila
import re, json, grequests
import pandas as pd

from bs4 import BeautifulSoup, NavigableString
from urllib.request import urlopen

# Yield successive n-sized chunks from list.
def divide_list(data, bins):
    bin_size = int(len(data)/bins)
    return [data[i:i+bin_size] for i in range(0, len(data), bin_size)]

def grequest_pipe(url_list):
    reqs = (grequests.get(url) for url in url_list)
    resp = grequests.imap(reqs, grequests.Pool(10))
    return resp


def get_question_links(url_list, pages):
    """
    Get all the question links in pages
    """
    reqs = grequest_pipe(url_list)

    links = []
    for idx, r in enumerate(resp):
        if idx % 15 == 0:
            print("Retrieving links in page {} of {}". format(idx, pages), end='\r')
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a', attrs={'class':'question-expand','href':True}):
            links.append(link.get('href').strip("\n| "))

    return links


def has_no_usuario(tag):
    """
    Helper function to filter href
    """
    return not re.compile('usuario').search(tag)


def scrape_page(soup, dict):

    # The class that contains the info that we want is "col-md-8"
    info = soup.find(class_="col-md-8")

    # Getting all question blocks
    question_block = soup.find_all('div', class_="question-block")

    for el in question_block:
        # pull-left: html branch with user information
        left_block = el.find('div', class_='pull-left')
        # Overflow: html branch with question content
        overflow = el.find('div', class_='overflow')

        try:
            u = left_block.find('p', class_='user-name')
            dict['user'].append(u.string)
        except:
            dict['user'].append(None)

        try:
            c = left_block.find('p', class_='user-category')
            dict['user_category'].append(c.string)
        except:
            dict['user_category'].append(None)

        try:
            d = overflow.find('li', text=re.compile('Hace'))
            dict['from'].append(d.string)
        except:
            dict['from'].append(None)

        try:
            qc = overflow.find('a', {'class':False,'href':has_no_usuario})
            dict['question_category'].append(qc.string)
        except:
            dict['question_category'].append(None)

        try:
            q = overflow.find('div',class_='question-body')
            dict['question_body'].append(q.get_text().strip("\n| "))
        except:
            dict['question_body'].append(None)

    return dict


def dict_to_csv(dict, idx):
    s1 = pd.Series(dict['user'], name='User Name')
    s2 = pd.Series(dict['user_category'], name='User Category')
    s3 = pd.Series(dict['from'], name='Date')
    s4 = pd.Series(dict['question_category'], name='Question Category')
    s5 = pd.Series(dict['question_body'], name='Question Body')
    df = pd.concat([s1,s2,s3,s4,s5], axis=1)

    if idx < 9:
        filename = 'data/enalquiler/enalquiler_0'+str(idx + 1)+'.csv'
    else:
        filename = 'data/enalquiler/enalquiler_'+str(idx + 1)+'.csv'

    df.to_csv(filename, index=False, encoding='utf-8')
