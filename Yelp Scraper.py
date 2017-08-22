'''This is my Yelp.com Scraper'''

# Libraries needed -imports
import requests
from bs4 import BeautifulSoup
import json
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

# FUNC Getting page and making it Soup object
def making_soup(url):
    page = requests.get(url)
    global soup
    soup = BeautifulSoup(page.content, 'html.parser')

# Finding companies
def companies_search():
    global finding_data
    global page

    while finding_data == True and page <=10:
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

def getting_details():
    for page in companies_list:
        making_soup(page)
        global col
        info = soup.find(type="application/ld+json")
        # getting all attributes of the page
        for items in info.children:
            attr = json.loads(items)
            try:
                title=attr['name']
                print(title)
                worksheet.write (row, col, title)
                col += 1
            except:
                print ('This item is not available')
                worksheet.write (row, col, 'Not available')
                col += 1



# Script start
companies_search()
getting_details()
print('Companies found: '+ str(len(companies_list)))

# End of script
output_file.close ()
print ('\nAll done!')
end = time.time ()
print ("\nTotal time for running:")
print (end - start)
