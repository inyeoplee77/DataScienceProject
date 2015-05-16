import ssl
from functools import wraps
def sslwrap(func):
	@wraps(func)
	def bar(*args, **kw):
		kw['ssl_version'] = ssl.PROTOCOL_TLSv1
		return func(*args, **kw)
	return bar
ssl.wrap_socket = sslwrap(ssl.wrap_socket)
import requests
from pattern import web
from BeautifulSoup import BeautifulSoup as bs
import discogs_client
import webbrowser
import re
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def uni(s):

	try:        
		s = HTMLParser.HTMLParser().unescape(s) 
	except Exception as e:
		print e
#   s = s.decode('string-escape')
	
	return s
def search_genre(singer, album):
	#genre = d.search(title, artist=singer)
	url = 'http://www.allmusic.com/search/albums/' + album + '%20' + singer
	i = 0
	for x in range(10):
		try:
			website_html = requests.get(url).text
			soup = bs(website_html)
		except requests.exceptions.RequestException as e:
			i+=1
			continue
		break
	if i>=9:
		return -1

	
	_genres={}
	for a in soup.findAll("div",{'class':"genres"}):
		for b in a.text.split(','):
			_genres[b] = 1
		break

	if _genres is not None:
		return _genres.keys()
	else:
		return -1

 
def search_album(singer, song):
	url = 'http://www.allmusic.com/search/song/' + singer + '%20' + song
	i=0
	for x in range(10) :
		try:
			website_html = requests.get(url).text
			soup = bs(website_html)
		except requests.exceptions.RequestException as e:
			i+=1
			continue
		break
	if i>=9:
		return -1

	
	compare = 0
	temp = []
	for line in soup.findAll("li",{'class':"song"}):
		
		for par in line.findAll("div"):
			if(par.get('class')=="title" and par.text.replace('\"','').lower()==song.lower()):
				compare += 1
				temp.append(par)
				continue
			if(par.get('class')=="performers" and par.find('a').contents[0].lower()==singer.lower()):
				compare += 1
				continue
		compare = 0
	if len(temp) != 0:
		for a in temp[0].findAll('a',href = True):
			return  search_album_name(a['href'])
	return -1

def search_album_name(url):
	if url == '':
		return -1
	i=0
	for x in range(10) :
		try:
			website_html = requests.get(url).text
			soup = bs(website_html) 
		except requests.exceptions.RequestException as e:
			i+=1
			continue
		break
	if i>=9:
		return -1

	albums = []
	for a in soup.findAll("td",{'class':"artist-album"}):
		if 'Various Artists' in a.find("span",{'itemprop':"name"}).text:
			continue
		for b in a.findAll("div",{'class':"title"}):
			albums.append(b.find('a').text)
	if len(albums)!=0:
		return albums
	else:
		return -1
			

result_file = open('ResultDB.txt','w')
input_file = open('MusicDB.txt','r')

while True:
	_title = input_file.readline()
	if not _title:
		break
	_title = _title.split('title:')[1].strip()
	_artist = input_file.readline().split('artist:')[1].split(',')[0].strip()
	result_file.write('title:'+_title+'\n')
	result_file.write('artist:'+_artist+'\n')

	_album = search_album(_artist,_title)
	if _album != -1:
		#print _album
		result_file.write('album: ')
		
		for a in _album:

			a=uni(a)
			result_file.write(a+',')
		
		result_file.write('\n')
		
		
		_genre = search_genre(_album[0],_title)
		if _genre !=-1:
		
			result_file.write('genre: ')
			
			for a in _genre:
				a=uni(a)
				result_file.write(a+',')
			result_file.write('\n')
			
	
   # result_file.write('\n')
input_file.close()
result_file.close()
