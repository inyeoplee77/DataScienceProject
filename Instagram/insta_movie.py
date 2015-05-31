from instagram.client import InstagramAPI
import sys
import locale
import re
import time

reload(sys)

sys.setdefaultencoding('utf8')

access_token = '1085114028.334eb93.e4202257327a42fcbe2840b838ef4e55'
user_id = '1085114028'
api = InstagramAPI(access_token=access_token)

users = {}

movies = open('Movie_DB_processing.txt','r')

user_db = open('user_movie_DB_test3.txt','w')

regex = re.compile('[^a-zA-Z0-9]') #regualr expression for non-alphabets




def movie_tag(title):
   #extract keywords for searching tags from the title - ex)Harry Potter and the Deathly Hallows -> Harry Potter
   titles = []
   titles_drop_the = []
   titles_drop_a = []
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
   #remove special characters
   for i in range(len(titles)):
      titles[i] = regex.sub('',titles[i])
   #if necessary, comment return statement and uncomment below code to return tag list
   return titles
   
   '''
   #search movie title tags that have the most media
   tags_list = []
   for title in titles:
      tags = api.tag_search(q=title,count = 10)
      if not tags[0]:
         continue
      for t in tags[0]:
         if t.name not in tags_list:
            tags_list.append(t.name)
   return tags_list
   '''   
users = {}   
for line in movies:
   if 'title' not in line:
      continue
   title_original = line.split('title:')[1].strip()
   titles = movie_tag(line.split('title:')[1].strip())
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
   count = 0
   while True:
      try:
         media = api.tag_recent_media(tag_name = max_tag.name)
         if media[1] is None or max_count == -1:
            continue
         max_tag_id = media[1].split('max_tag_id=')[1]     
         #get ids of users who we want              
         while True:
            for m in media[0]:
               if not hasattr(m,'tags'):
                  continue
               for tag in m.tags:
                  if 'movie' in tag.name:
                     if m.user.id in users.keys():
                        if title_original not in users[m.user.id]:
                           users[m.user.id].append(title_original)
                           user_db.write(str(m.user.id) + '::' + title_original+'\n')
                           count += 1
                           print m.user.id + '  ' + title_original
                     else:
                        users[m.user.id] = []
                        users[m.user.id].append(title_original)
                        user_db.write(str(m.user.id)+'::'+title_original+'\n')
                        count +=1
                        print m.user.id + '  ' + title_original
            media = api.tag_recent_media(max_tag_id = max_tag_id,tag_name = max_tag.name)
            if media[1] is None or count > 50:
               break
            max_tag_id = media[1].split('max_tag_id=')[1]         
      except Exception as e:
         time.sleep(10)
         print '10 seconds break'
         print e
         continue
      break
   user_db.flush()
for key in users:
   user_db.write(key + '::' + users[key] + '\n')        
user_db.close()