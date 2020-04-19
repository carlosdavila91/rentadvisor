import grequests, json
import time, datetime, itertools

from utils import *
from bs4 import BeautifulSoup

"""
The process derived from this script is very time consuming
as the total number of pages to scrape in the forum is 5715.
Consider using a smaller number for developing.

To set the number of pages to scrape go to utils.py
"""

# Start timer
start_time = time.time()

with open('data/enalquiler/links.txt', 'r') as f:
    links = f.read().splitlines()

# Divide the list to improve performance
bins = 102
list = divide_list(links, bins)

for idx, l in enumerate(list):

    keys = ['user','user_category','from','question_category','question_body']
    dict = {k:[] for k in keys}

    # Get the responses
    resp = grequest_pipe(l)

    # Scrape!
    for r in resp:
        soup = BeautifulSoup(r.text, 'html.parser')
        temp = scrape_page(soup, dict)
        dict.update(temp)

    # Save to data frame
    dict_to_csv(dict, idx)

    pctge = (idx+1)/(len(list)+1) * 100
    print("Completed {}% of the process".format(round(pctge, 1)), end='\r')


elapsed = datetime.timedelta(seconds=time.time() - start_time)

print("--- {0} seconds ---".format(elapsed))
