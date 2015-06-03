#get popular Brand List
import requests
from BeautifulSoup import BeautifulSoup
import datetime
import re
import sys
import HTMLParser
reload(sys)

sys.setdefaultencoding('utf8')

f = open('Brand_DB.txt','w')

url='http://www.apparelsearch.com/wholesale_clothing/popular_brand_names_clothes.htm'
try:
	scraps= BeautifulSoup(requests.get(url).content.decode('utf-8','ignore'))
	
except requests.exceptions.RequestException as e:
	print 'error'
brands=scraps.findAll('b',style='background-color:transparent;color:#000000;font-weight:bold;')
for brand in brands:
	brand = brand.find('span')
	if brand is None:
		continue
	brand_name=brand.contents[0]
	print brand_name
	brand_name=HTMLParser.HTMLParser().unescape(brand_name)	
	f.write(brand_name+'\n')
f.close()

