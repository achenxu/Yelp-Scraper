'''This is my Yelp.com Scraper'''

# Libraries needed
import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
import re
import time
print ('Libraries imported')

# Timer - shows how fast the script runs.
start = time.time()

#Output file
output_file = xlsxwriter.Workbook ('Yelp_Results.xlsx')
worksheet = output_file.add_worksheet ()

#Variables needed
row = 1
col = 0

# FUNC Getting page and making it Soup object
def making_soup(url):
    page = requests.get (url)
    global soup
    soup = BeautifulSoup (page.content, 'html.parser')

