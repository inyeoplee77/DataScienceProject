from instagram.client import InstagramAPI
import sys
import locale
import re
reload(sys)

sys.setdefaultencoding('utf8')

access_token = '1085114028.334eb93.e4202257327a42fcbe2840b838ef4e55'
user_id = '1085114028'
api = InstagramAPI(access_token=access_token)

users = {}

movies = open('Movie_DB.txt','r')

user_db = open('user_movie_DB.txt','w')

regex = re.compile('[^a-zA-Z]') #regualr expression for non-alphabets


for line in movies:
   if 'title' not in line:
      continue
   titles = []
   titles_drop_the = []
   titles_drop_a = []
   #extract keywords for searching tags from the title - ex)Harry Potter and the Deathly Hallows -> Harry Potter
   
   title = line.split('title:')[1]
   title_original = title.strip()
   title = title.lower().strip()
   
   titles.append(title)   
   if ':' in title:
      titles.extend(title.split(':'))
   if 'and the' in title:
      titles.extend(title.split('and the'))
      
   if title.find('the ') == 0 and 'and the' not in title:
      for title in titles:
         titles_drop_the.append(title.replace('the ',''))
      titles.extend(titles_drop_the)
   if title.find('a ') == 0:
      for title in titles:
         titles_drop_a.append(title.replace('a ',''))
      titles.extend(titles_drop_a)
   print title_original
   #remove special characters
   for i in range(len(titles)):
      titles[i] = regex.sub('',titles[i])
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
   users = {} #to avoid duplication, initialize users dictionary for every movie title
   for j in range(10):
      try:
         media = api.tag_recent_media(tag_name = max_tag.name,)
         if media[1] is None or max_count == -1:
            continue
         max_tag_id = media[1].split('max_tag_id=')[1]
         print max_count     
         #get ids of users who we want
         num = 10 # number of iterations (= number of media)              
         for i in range(num):
            for m in media[0]:
               if not hasattr(m,'tags'):
                  continue
               for tag in m.tags:
                  if 'movie' in tag.name:
                     user[m.user.id] = title_original
            media = api.tag_recent_media(max_tag_id = max_tag_id,tag_name = max_tag.name)
            if media[1] is None:
               break
            max_tag_id = media[1].split('max_tag_id=')[1]         
      except Exception as e:
         print e
         continue
      break
   for key in users.keys():
      user_db.write(str(key) + '::' + users[key] + '\n')        
user_db.close()