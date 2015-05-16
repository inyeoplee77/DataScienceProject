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