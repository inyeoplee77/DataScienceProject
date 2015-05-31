from instagram.client import InstagramAPI
import sys
import locale
import re
reload(sys)

sys.setdefaultencoding('utf8')

access_token = '1085114028.334eb93.e4202257327a42fcbe2840b838ef4e55'
#user_id = '1085114028'


api = InstagramAPI(client_id='334eb938576d4207b655a2911944f919', client_secret='f734f47818ae462f9150d4816114df17')
api = InstagramAPI(access_token=access_token)

users = {}

music = open('Music_DB.txt','r')

user_db = open('user_movie_DB.txt','r')

regex = re.compile('[^a-zA-Z]') #regualr expression for non-alphabets

#users
for line in user_db:
   tmp = line.split(':')
   users[tmp[0]] = tmp[1]


for user in users:
   media, _next = api.user_recent_media(user)
   print media
   #from media, find the media with any music title tags
   #then build music-user DB
   #problem: can't get other users' media 
   '''
   for medium in media[0]:
      if not hasattr(medium,'tags'):
         continue
      for tag in medium.tags:
         print tag
   '''



