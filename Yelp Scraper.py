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

# Output file
output_file = xlsxwriter.Workbook ('Yelp_Results.xlsx')
worksheet = output_file.add_worksheet ()

# Variables needed
# Needed for excel
row = 1
col = 0

# Needed for pagination in YELP
page=0
global finding_data
finding_data = True

# List of copanies gathered
companies_list=[]
total_companies=0

# FUNC Getting page and making it Soup object
def making_soup(url):
    page = requests.get(url)
    global soup
    soup = BeautifulSoup(page.content, 'html.parser')

# Script start
while finding_data == True:
    finding_data = False
    making_soup('https://www.yelp.com/search?find_desc=Chiropractors&find_loc=415&start='+str(page))
    print('Going to ''https://www.yelp.com/search?find_desc=Chiropractors&find_loc=415&start='+str(page))
    page += 10
    for company_pages in soup.find_all('h3', class_="search-result-title"):
        for titles in company_pages(href=re.compile('/biz/')):
            companies_list.append('https://www.yelp.com'+str(titles['href']))
            finding_data = True

else:
    print('No more results available')

print ('Companies found: '+ str(companies_list))

output_file.close ()
print ('\nAll done!')
end = time.time ()
print ("\nTotal time for running:")
print (end - start)
