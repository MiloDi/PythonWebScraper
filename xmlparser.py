from bs4 import BeautifulSoup
import requests
import csv


class Scraper(object):
    def __init__(self, url, headers, csvfile, tag_name):
        self.tag_name = tag_name
        self.target_url = url
        self.header_names = headers
        self.filename = csvfile
        self.data = []
        self.csvwriter = csv.writer(open(self.filename, 'w'))
        self.csvwriter.writerow(self.header_names)
        self.getSoup()
        self.scrape()
        self.sortAndWrite()

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
                self.data.append(details)

    def sortAndWrite(self):
		index = self.header_names.index('datelisted')
		filedata = sorted(self.data, key=lambda row: (row[index]), reverse=True)
		for line in filedata:
			self.csvwriter.writerow(line)
               

    def containsString(self, text, keyword):
        if keyword in text:
            return True
        else:
            return False


if __name__ == '__main__':
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
	scrape_url = "http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml"
	my_scraper = Scraper(scrape_url, headers, csv_file_name, "listing")

