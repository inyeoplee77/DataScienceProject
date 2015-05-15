from instagram.client import InstagramAPI
import sys
import locale
reload(sys)
sys.setdefaultencoding('utf8')

access_token = '1085114028.334eb93.e4202257327a42fcbe2840b838ef4e55'
user_id = '1085114028'
api = InstagramAPI(access_token=access_token)

users = {}

movies = open('Movie_DB.txt','r')

for line in movies:
   if 'title' not in line:
      continue
      
   #extract REAL title from the title - ex)Harry Potter and the Deathly Hallows -> Harry Potter
   title = line.split('title:')[1]
   title = title.lower().replace(' ','')
   
   title = title.split(':')[0]
   print title
   #remove special characters
   
   
   #search movie title tags
   '''
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