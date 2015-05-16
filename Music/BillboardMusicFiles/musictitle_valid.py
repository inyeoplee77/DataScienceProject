import requests
from BeautifulSoup import BeautifulSoup
import datetime
import re
import sys
import HTMLParser
reload(sys)


sys.setdefaultencoding('utf8')

urls= {}
week = 1000
idx = 0
date = datetime.date(2015,05,02)

def uni(s):
	s = s.replace('&amp;','&')
	s = s.replace('quot;','')
	loc = s.find('&#')
	while loc != -1:
		u = s[loc:loc+6]
		t = s[loc+2:loc+5]
		s = s.replace(u,unichr(int(t)))
		loc = s.find('&#')
	s = s.decode('string-escape')
	return s

def uni_list(l):
	for s in range(0,len(l)):
		l[s] = l[s].replace('quot;','')
		#l[s] = l[s].replace('&amp;','&')
		loc = l[s].find('&#')
		while loc != -1:
			u = l[s][loc:loc+6]
			t = l[s][loc+2:loc+5]
			l[s] = l[s].replace(u,unichr(int(t)))
			loc = l[s].find('&#')
	for a in range(0,len(l)):
		l[a] = l[a].decode('string-escape')
	return l

print "getting urls...\n"
for x in range(week):
	date -= datetime.timedelta(weeks=1)
	urls[idx] = 'http://www.billboard.com/charts/hot-100/'+date.isoformat()
	
	idx = idx + 1
	
f = open('MusicDB.txt','w')
number = 0

songlist=[]

import re
pattern = re.compile(r'&amp;|,|Featuring|Feat.')


print "scrapping web..."
#write_str=""
for i in range(week):
	print i
	try:
		scraps= BeautifulSoup(requests.get(urls[i]).content.decode('utf-8','ignore'))	
	except requests.exceptions.RequestException as e:
		print "request Exceptions"
		continue

	songs = scraps.findAll('div','row-title')
	for song in songs:
		title=song.find('h2').contents[0].strip()
		title=uni(title)
		tmp= song.find('a')
		if tmp is None:
			tmp=song.find('h3')
		artist=tmp.contents[0].strip()
		#one = [ title ]
		artist = pattern.split(artist)
		artist = uni_list(artist)
		if title not in songlist:
			f.write('title:'+str(title)+'\n')
			f.write('artist:')
			for a in range(len(artist)-1):
				f.write(str(artist[a])+',')
			f.write(str(artist[len(artist)-1]))
			f.write('\n')
			songlist.append(title)
f.close()