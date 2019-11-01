from bs4 import BeautifulSoup
import requests
import csv

class Scraper(object):
    def __init__(self, url, headers, csvfile, tag_name):
        self.tag_name = tag_name
        self.target_url = url
        self.header_names = headers
        self.csvwriter = csv.writer(open(csvfile, 'w'))	
        self.csvwriter.writerow(self.header_names.keys())	
        self.getSoup()
        self.scrape()

    def getSoup(self):
        result = requests.get(self.target_url)
        self.soup = BeautifulSoup(result.content, 'lxml')
        
    def scrape(self):
		for listing in self.soup.find_all(self.tag_name):
			details = []
			for key, val in self.header_names.iteritems():
				try:
					details.append(listing.find(key).text[:200])
				except AttributeError:
					print("Failed to read field: " + key)
			self.csvwriter.writerow(details)	

    def containsString(self, text, keyword):
        if keyword in text:
            return True
        else: 
      	    return False
        
        
headers = {
    'mlsid': None,
    'mlsname': None,
    'datelisted': "2016",
    'streetaddress': None,
    'price': None,
    'bedrooms': None,
    'bathrooms': None,
    'appliances': None,
    'rooms': None,
    'description': " and "
}
csv_file_name = 'testData.csv'
scape_url = "http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml"
my_scraper  = Scraper(scape_url, headers, csv_file_name, "listing")




