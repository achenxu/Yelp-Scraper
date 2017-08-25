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
output_file = xlsxwriter.Workbook('Yelp_Results.xlsx')
worksheet = output_file.add_worksheet()

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
        global row
        info = soup.find(type="application/ld+json")

        # Getting all attributes of the page
        for items in info.children:
            attr = json.loads(items)

            # Title
            try:
                col = 0
                title = attr['name']
                print(title)
                worksheet.write (row, col, title)

            except:
                print('This item is not available')
                worksheet.write(row, col, 'Not available')

            # Address
            try:
                col = 1
                address = attr['address']['streetAddress']+", "+attr['address']['addressLocality']+", "+attr['address']['addressRegion']+", "+attr['address']['postalCode']+", "+attr['address']['addressCountry']
                print(address)
                worksheet.write(row, col, str(address))

            except:
                print('This item is not available')
                worksheet.write(row, col, 'Not available')

            # Phone
            try:
                col = 2
                phone = attr['telephone']
                print(phone)
                worksheet.write(row, col, phone)

            except:
                print ('This item is not available')
                worksheet.write(row, col, 'Not available')

            # Type
            try:
                col = 3
                type = attr['@type']
                print(type)
                worksheet.write(row, col, type)

            except:
                print('This item is not available')
                worksheet.write(row, col, 'Not available')

            # Review count
            try:
                col = 4
                review_count = attr['aggregateRating']['reviewCount']
                print(review_count)
                worksheet.write (row, col, review_count)

            except:
                print('This item is not available')
                worksheet.write(row, col, 'Not available')

            # Rating value
            try:
                col = 5
                rating_value = attr['aggregateRating']['ratingValue']
                print(rating_value)
                worksheet.write(row, col, rating_value)

            except:
                print('This item is not available')
                worksheet.write(row, col, 'Not available')

            # Description
            try:
                col = 6
                description = soup.find(property="og:description")['content']
                print(description)
                worksheet.write(row, col, description)

            except:
                print('This item is not available')
                worksheet.write(row, col, 'Not available')

        row += 1



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
