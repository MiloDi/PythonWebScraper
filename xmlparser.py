from bs4 import BeautifulSoup
import requests
import csv


class Scraper(object):
    def __init__(self, url, headers, csvfile, tag_name):
        self.tag_name = tag_name
        self.target_url = url
        self.header_names = headers
        self.csvwriter = csv.writer(open(csvfile, 'w'))
        self.csvwriter.writerow(self.header_names)
        self.getSoup()
        self.scrape()

    def getSoup(self):
        result = requests.get(self.target_url)
        self.soup = BeautifulSoup(result.content, 'lxml')

    def scrape(self):
		for listing in self.soup.find_all(self.tag_name):
			details = []
			for tag in self.header_names:
				try:
         			 details.append(listing.find(tag).text[:200])
				except AttributeError:
					print("Failed to read field: " + tag)
			combined = '\t'.join(details)
			if '2016' in combined:
    		    self.csvwriter.writerow(details)
			else:
				print(False)

    def containsString(self, text, keyword):
        if keyword in text:
            return True
        else: 
      	    return False
        
        
headers = [
    'mlsid',
    'mlsname',
    'datelisted',
    'streetaddress',
    'price',
    'bedrooms',
    'bathrooms',
    'appliances',
    'rooms',
    'description'
]
csv_file_name = 'testData.csv'
scape_url = "http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml"
my_scraper  = Scraper(scape_url, headers, csv_file_name, "listing")




