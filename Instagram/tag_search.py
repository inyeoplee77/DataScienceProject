from instagram.client import InstagramAPI
import sys
import locale
import re
import urllib2
import requests
import re
reload(sys)

sys.setdefaultencoding('utf8')

api = InstagramAPI(client_id='334eb938576d4207b655a2911944f919', client_secret='f734f47818ae462f9150d4816114df17')

music = open('Music_DB.txt','r')
brand_db = open('finalBrandDB.txt','r')

music_tag = open('music_tag_new','w')
brand_tag = open('brand_tag_new','w')

regex = re.compile('[^a-zA-Z0-9]') #regualr expression for non-alphabets
music_duplicate = []
#music
def tag_search_music(title):
   title = line.split('title:')[1]
   title = title.split('-')[0]
   title = title.split('featuring')[0]
   title = title.split('feat.')[0]
   title = title.split('[')[0]
   title = title.split('(')[0]
   title = title.strip().lower()     
   title = regex.sub('',title)
   if title in music_duplicate:
      return None
   music_duplicate.append(title)
   tags = api.tag_search(title,count = 5)   
   return tags
   
def tag_search_brand(brand):
   brand = regex.sub('',line)
   tags = api.tag_search(brand,count = 5)
   return tags

for line in music:
   if 'title:' in line:
      tags = tag_search_music(line.strip())
      if tags is None:
         print 'duplicated'
         continue
      if not tags[0]:
         print 'No tag searched:',line
         continue
      print line.strip()
      music_tag.write(line.split('title:')[1].strip() + ' :: ')      
      for tag in tags[0]:
         music_tag.write(tag.name+' ')
      music_tag.write('\n')
#brand
for line in brand_db:
   if not line:
      continue
   tags = tag_search_brand(line)
   if not tags[0]:
      print 'No tag searched:',line
   print line.strip()
   brand_tag.write(line.strip()+' :: ')
   for tag in tags[0]:
      brand_tag.write(tag.name+' ')
   brand_tag.write('\n')