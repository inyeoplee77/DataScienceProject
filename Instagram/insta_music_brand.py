from instagram.client import InstagramAPI
import sys
import locale
import re
import urllib2
import requests


reload(sys)

sys.setdefaultencoding('utf8')

#access_token = '1085114028.334eb93.e4202257327a42fcbe2840b838ef4e55'
#user_id = '1085114028'
client_id = '334eb938576d4207b655a2911944f919'

api = InstagramAPI(client_id='334eb938576d4207b655a2911944f919', client_secret='f734f47818ae462f9150d4816114df17')
#api = InstagramAPI(access_token=access_token)

users = {}
music_tag = {}
brand_tag = {}
user_music = {}
user_brand = {}

music_tag_f = open('music_tag_new','r')
brand_tag_f = open('brand_tag_new','r')
user_db = open('user_movie_DB_test2.txt','r')
brand_db = open('finalBrandDB.txt','r')
training = open('training','w')

regex = re.compile('[^a-zA-Z0-9]') #regualr expression for non-alphabets

#users
for line in user_db:
   tmp = line.split('::')
   users[tmp[0].strip()] = tmp[1].strip()#.split(',')
for line in music_tag_f:
   if not line:
      break
   line = line.split(' :: ')
   music_tag[line[0]] = line[1].strip().split(' ')
for line in brand_tag_f:
   if not line:
      break
   line = line.split(' :: ')
   brand_tag[line[0]] = line[1].strip().split(' ')
 
music_tag_f.close()
brand_tag_f.close()

for user in users:
   
   result = requests.get("https://api.instagram.com/v1/users/"+user+"/media/recent/",params={'client_id':client_id}).json()
   user_music[user] = []
   user_brand[user] = []
   while True:
      data = result['data']
      #data contains a list of media
      #media contains a list of tags
      for medium in data:
         tags = medium['tags']
         #search for music tag
         for music in music_tag:             
            if ('music' in tags or 'listening' in tags or 'nowlisteningto' in tags or 'listeningto' in tags) and any(map(lambda v : v in music_tag[music],tags)):
               if music not in user_music[user]:
                  print tags, music, users[user]
                  user_music[user].append(music)
         #search for brand tag
         for brand in brand_tag:
            if any(map(lambda v : v in brand_tag[brand],tags)):
               if brand not in user_brand[user]:
                  print tags, brand, users[user]
                  user_brand[user].append(brand)
      #get all the media from user 
      next_url = result['pagination']
      if 'next_url' not in next_url:
         break       
      while True:
         try:
            next_url = next_url['next_url']
            result = requests.get(next_url).json()
         except Exception as e:
            time.sleep(10) 
            print '10 seconds break'
            print e
            continue
         break
   #generate training set 
   # x = movie list, music list (input) 
   # y = brand (answer)
   for b in user_brand[user]:
      if not b:
         continue 
      #for i in users[user]:
      training.write(users[user]+',')
      for i in user_music[user]:
         training.write(i+',')
      training.write(','+b+'\n')
      training.flush()
      print 'training sample added, ' + str(len(users[user]))+' movie added, '+ str(len(user_music[user]))+ ' music added, brand:', b
