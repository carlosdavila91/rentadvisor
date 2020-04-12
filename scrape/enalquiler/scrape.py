import pandas as pd
import grequests, json
import time

from utils import *
from bs4 import BeautifulSoup
from collections import defaultdict

# Start timer
start_time = time.time()

# Main forum page url
url_list = ["https://www.enalquiler.com/comunidad_alquiler/preguntas_y_respuestas.html"]

# Get the url of each forum page
url = "https://www.enalquiler.com/comunidad-alquiler/todas/"

"""
DISCLAIMER! This process is very time consuming.
The total amount of pages in the forum page is 5715
Consider using a smallest number for developing
"""

pages = 5715

for i in range(2,pages):
    url_list.append(url + str(i))

links = get_question_links(url_list)

reqs = (grequests.get(link) for link in links)
resp = grequests.imap(reqs, grequests.Pool(10))

keys = ['user','user_category','question_body','question_category']
dict = {k:[] for k in keys}

for r in resp:
   soup = BeautifulSoup(r.text, 'html.parser')
   temp_dict = EnalquilerForumScrape(soup)
   for k in keys:
       dict[k].extend(temp_dict[k])

df = pd.DataFrame(
    {
        'User Name':dict['user'],
        'User Category':dict['user_category'],
        'Question Body':dict['question_body'],
        'Question Category':dict['question_category']
    }
)

df.to_csv('data/enalquiler/enalquiler.csv', index=False, encoding='utf-8')

print("--- {} seconds ---".format(time.time() - start_time))
