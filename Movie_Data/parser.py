import requests
from BeautifulSoup import BeautifulSoup
import re
import sys
reload(sys)


sys.setdefaultencoding('utf8')

urls = {}
scraps = {}

idx = 0
#80001
for x in range(1,82272,50):
	urls[idx] = 'http://www.imdb.com/search/title?at=0&release_date=1992,2014&sort=num_votes&start='+str(x)+'&title=*&title_type=feature,short&user_rating=6.0,10'
	scraps[idx] = BeautifulSoup(requests.get(urls[idx]).content.decode('utf-8','ignore')).find('table','results')
	print urls[idx]
	idx = idx + 1

f = open('Movie_DB.txt','w')
number = 0
staff = {}
for i in scraps:
	info_even = scraps[i].findAll('tr','even detailed')
	info_odd = scraps[i].findAll('tr','odd detailed')
	infos = info_odd + info_even

	for info in infos:
		
		votes = info.find('td','sort_col')
		
		

		info = info.find('td','title')
		
		staff = info.find('span','credit')
		rating = info.find('span','value')
		year = info.find('span','year_type')
		genres = info.find('span','genre')
		if staff is None or rating is None or votes is None or genres is None or year is None:
			continue

		staff = staff.getText()
		if 'Dir' not in staff or 'With' not in staff:
			continue

		year = year.contents[0]
		votes = votes.contents[0]
		rating = rating.contents[0]
		genres = genres.findAll('a')

		directors = staff[staff.find('Dir:')+4:staff.find('With:')].split(',')
		stars = staff[staff.find('With:')+5:].split(',')

		title = info.find('a').contents[0]
		

		f.write('title:'+title+'\n')
		f.write('year:'+year+'\n')
		f.write('rating:'+rating+'\n')
		f.write('votes:'+votes+'\n')
		
		f.write('director:')
		for d in directors:
			f.write(d+',')
		f.write('\n')

		f.write('stars:')
		for s in stars:
			f.write(s+',')
		f.write('\n')

		f.write('genres:')
		for g in genres:
			f.write(g.contents[0]+',')
		f.write('\n')