import sys
reload(sys)
sys.setdefaultencoding('utf8')


music_db = file('Music_DB.txt','r')
movie_db = file('Movie_DB.txt','r')
for a in music_db:
    print a
    print music_db.next()