import discogs_client
import webbrowser
import re
d = discogs_client.Client('ExampleApplication/0.1')
d.set_consumer_key('VHNmnEdRkfVYBxOuFbYk','dlcnrcGYNOOXNZDkZtvkAcvRRdaetoGl')
webbrowser.open(d.get_authorize_url()[2])
token = raw_input()
d.get_access_token(token)
import requests
from pattern import web
from BeautifulSoup import BeautifulSoup as bs

def search_composer(singer, song):
    compare = 0
    url = 'http://www.allmusic.com/search/song/' + singer + '%20' + song
    website_html = requests.get(url).text
    soup = bs(website_html)
    check = 0
    for line in soup.findAll("li",{'class':"song"}):    
        for par in line.findAll("div"):
            if(par.get('class')=="title" and par.text.replace('\"','').lower()==song.lower()):
                compare += 1
                continue
            if(par.get('class')=="performers" and par.find('a').contents[0].lower()==singer.lower()):
                compare += 1
                continue
            if(compare==2 and par.get('class')=="composers"):
                composer = par.find('a').contents[0]
                check = 1
                return composer
                break
        if(compare==2):
            check=1
            return singer
        compare = 0
    if(check==0):
        return -1

def search_genre(singer, title):
    genre = d.search(title, artist=singer)
    _genres={}
    if not d.search(title, artist=singer):
        return -1
    else:
        genre = genre[0].genres
        for a in genre:
            if a not in _genres:
                _genres[a] = 1
        return _genres.keys()
 
def search_album(singer, song):
    url = 'http://www.allmusic.com/search/song/' + singer + '%20' + song
    website_html = requests.get(url).text
    soup = bs(website_html)
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
    website_html = requests.get(url).text
    albums = []
    soup = bs(website_html) 
    for a in soup.findAll("td",{'class':"artist-album"}):
        if 'Various Artists' in a.find("span",{'itemprop':"name"}).text:
            continue
        for b in a.findAll("div",{'class':"title"}):
            albums.append(b.find('a').text)
    if albums is not None:
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
    composer = search_composer(_artist,_title)
    if composer == -1:
        composer = _artist
    result_file.write('Composer: ' + composer + '\n')
    _genre = search_genre(_artist,_title)
    if _genre !=-1:
        result_file.write('Genre:')
        for a in _genre:
            result_file.write(str(a).encode('ascii','ignore').decode('ascii')+',')
        result_file.write('\n')
    _album = search_album(_artist,_title)
    if _album != -1:
        result_file.write('Album:')
        for a in _album:
            result_file.write(str(a).encode('ascii','ignore').decode('ascii')+',')
        result_file.write('\n')
input_file.close()
result_file.close()