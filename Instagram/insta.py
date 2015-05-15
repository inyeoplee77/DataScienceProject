from instagram.client import InstagramAPI
from unidecode import unidecode 
import sys
import locale
reload(sys)
sys.setdefaultencoding('utf8')
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8' )



access_token = '1085114028.334eb93.e4202257327a42fcbe2840b838ef4e55'
user_id = '1085114028'
api = InstagramAPI(access_token=access_token)

'''
tags = api.tag_search(q='#$%@!#',count = 10)
if not tags[0]:
   print 'None'
tags = tags[0]

media = api.tag_recent_media(tag_name = tags[0].name)
print media
max_tag_id = media[1].split('max_tag_id=')[1]
'''

def uni(s):
	loc = s.find('&#x')
	while loc != -1:
		u = s[loc:loc+6]
		t = s[loc+3:loc+5]
		s = s.replace(u,unichr(int(t,16)))
		loc = s.find('&#x')
	return s
   
count = 0   
out = open('DB.txt','w')
for i in range(1,10):
   f  = open('Movie/'+str(i)+'.txt','r')
   while True:
      title = f.readline()
      if not title:
         break
      title = title.split('title:',1)[1]
      
      title = unidecode(uni(title))
      f.readline()
      f.readline()
      votes = locale.atoi(f.readline().rstrip().split(':')[1])
      if votes < 1000:
         f.readline()
         f.readline()
         f.readline()
         continue
      out.write(title)             
      directors = f.readline().rstrip().split(':',1)[1].split(',')[:-1]
      for i in range(len(directors)):   
         directors[i] = unidecode(unicode(uni(directors[i]),'utf-8'))
         out.write(directors[i]+',')
      out.write('\n')
      stars = f.readline().rstrip().split(':',1)[1].split(',')[:-1]
      for i in range(len(stars)):          
         stars[i] = unidecode(unicode(uni(stars[i]),'utf-8'))
         out.write(stars[i]+',')
      genres = f.readline().rstrip().split(':',1)[1].split(',')[:-1]
      out.write('\n')
      for i in genres:
         out.write(i+',')
      out.write('\n')
      count += 1
print count
out.close()
'''   
   
users = {}

for line in f:
   if 'title' not in line:
      continue
   title = line.split('title:')[1]
   title = title.lower().replace(' ','')
   
   #remove special characters
   
   tags = api.tag_search(q=title,count = 10)
   if not tags[0]:
      continue
   tags = tags[0]
   media = api.tag_recent_media(tag_name = tags[0].name)
   max_tag_id = media[1].split('max_tag_id=')[1]
   
   for i in range(10):
      for m in media[0]:
         if not hasattr(m,'tags'):
            continue
         for tag in m.tags:
            if 'movie' in tag.name:
               print m.tags
               print m.user.id
               users[m.user.id] = m.get_standard_resolution_url()
      media = api.tag_recent_media(max_tag_id = max_tag_id,tag_name = tags[0].name)
      max_tag_id = media[1].split('max_tag_id=')[1]
for user in users.keys():
   u = api.user_recent_media(user_id = user)
'''