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
   titles = []
   titles_drop_the = []
   titles_drop_a = []
   #extract REAL title from the title - ex)Harry Potter and the Deathly Hallows -> Harry Potter
   
   title = line.split('title:')[1]
   title = title.lower().strip()
   
   titles.append(title)   
   if ':' in title:
      titles.extend(title.split(':'))
   if 'and the' in title:
      titles.extend(title.split('and the'))
      
   if 'the ' in title and 'and the' not in title:
      for title in titles:
         titles_drop_the.append(title.replace('the ',''))
      titles.extend(titles_drop_the)
   if 'a ' in title:
      for title in titles:
         titles_drop_a.append(title.replace('a ',''))
      titles.extend(titles_drop_a)
   print titles
   
   #remove special characters
   
   
   #search movie title tags that have the most media
   max_count = -1
   for title in titles:
      tags = api.tag_search(q=title,count = 10)
      if not tags[0]:
         continue
      tags = tags[0]
      count = tags[0].media_count
      if count > max_count:
         max_count = count
         max_tag = tags[0]
   
   media = api.tag_recent_media(tag_name = max_tag.name,)
   if media[1] is None:
      continue
   max_tag_id = media[1].split('max_tag_id=')[1]
   print max_count     
   #get ids of users who we want             
   for i in range(10):
      for m in media[0]:
         if not hasattr(m,'tags'):
            continue
         for tag in m.tags:
            if 'movie' in tag.name:
               users[m.user.id] = m.get_standard_resolution_url()
      media = api.tag_recent_media(max_tag_id = max_tag_id,tag_name = max_tag.name)
      if media[1] is None:
         break
      max_tag_id = media[1].split('max_tag_id=')[1]
for user in users.keys():
   u = api.user_recent_media(user_id = user)
