import grequests, json
import time, datetime

from utils import *
from bs4 import BeautifulSoup

"""
The process derived from this script is very time consuming
as the total number of pages to scrape in the forum is 5715.
Consider using a smaller number for developing.

The list of URLs have the following format

url_list = [
    "https://www.enalquiler.com/comunidad_alquiler/preguntas_y_respuestas.html",
    "https://www.enalquiler.com/comunidad-alquiler/todas/2",
    "https://www.enalquiler.com/comunidad-alquiler/todas/3",
    ...
]

"""

# Start timer
start_time = time.time()

# Main forum page url
url_list =  ["https://www.enalquiler.com/comunidad_alquiler/preguntas_y_respuestas.html"]

# Get the url of each forum page
url = "https://www.enalquiler.com/comunidad-alquiler/todas/"

pages = 5715

for i in range(2, pages + 1):
    url_list.append(url + str(i))

links = get_question_links(url_list, pages)

elapsed = datetime.timedelta(seconds=time.time() - start_time)

print("--- {0} seconds ---".format(elapsed))

with open('data/enalquiler/links.txt', 'w') as f:
    for l in links:
        f.write("{}\n".format(l))
