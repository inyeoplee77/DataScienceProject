from pyechonest import config
from pyechonest import artist
from pyechonest import song
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def uni(s):
	try:        
		s = HTMLParser.HTMLParser().unescape(s) 
	except Exception as e:
		print e
#   s = s.decode('string-escape')
	return s
config.ECHO_NEST_API_KEY="UUPUPB2C9FGMT1NSS"
result_file=open('Music.txt','w')
startpoint=0
maxpoint=1.0
last_maxpoint=0
song_artist={}
for i in range(20):
	
	if startpoint>900 :
		startpoint=0
		maxpoint=last_maxpoint
	print 'startpoint: '+str(startpoint)


	ss_results = song.search(song_max_hotttnesss=maxpoint,start=startpoint,buckets=['audio_summary','song_type','song_hotttnesss'],results=100,sort ='song_hotttnesss-desc')
	#print ss_results
	#print
	#print
	
	

	for songOne in ss_results:

		#remove duplicate 'song name-artist name'
		if songOne.title in song_artist.keys():
			if songOne.artist_name==song_artist[songOne.title]:
				continue

			
		wt='title: '+songOne.title+'\n'
		wt+='song_id: '+songOne.id+'\n'
		wt+='artist: '+songOne.artist_name+'\n'
		wt+='energy: '+str(songOne.audio_summary['energy'])+'\n'
		wt+='liveness: '+str(songOne.audio_summary['liveness'])+'\n'
		wt+='tempo: '+str(songOne.audio_summary['tempo'])+'\n'
		wt+='speechiness: '+str(songOne.audio_summary['speechiness'])+'\n'
		wt+='acousticness: '+str(songOne.audio_summary['acousticness'])+'\n'
		wt+='danceability: '+str(songOne.audio_summary['danceability'])+'\n'
		wt+='instrumentalness: '+str(songOne.audio_summary['instrumentalness'])+'\n'
		wt+='loudness: '+str(songOne.audio_summary['loudness'])+'\n'
		wt+='valence: '+str(songOne.audio_summary['valence'])+'\n'
		wt+='song_hotttnesss: '+str(songOne.song_hotttnesss)+'\n'
		wt+='song_type: '
		for i in songOne.song_type:
			wt+=i+','

		wt+='\n'
		wt=uni(wt)
		result_file.write(wt)
		song_artist[songOne.title]=songOne.artist_name
		last_maxpoint=songOne.song_hotttnesss

	startpoint+=100

print len(song_artist)
	#under- not valid code

'''
	#count access limitted
	artist_id=song.artist_id
	artist_terms=artist.Artist(artist_id).terms
	for i in artist_terms:
		print i['name']
		wt+=i['name']+','
	wt+='\n'
'''

'''
	artist_mood=artist.Artist(artist_id).list_terms('mood')
	for i in artist_mood:
		print i
		wt+=i+','
	wt+='\n'
	artist_style=artist.Artist(artist_id).list_terms('style')
	for i in artist_style:
		print i
		wt+=i+','
	wt+='\n'
'''




'''
ss_results_a =song.search(song_max_hotttnesss=1.0,song_min_hotttnesss=0.8,buckets=['audio_summary','song_type'],results=50,sort ='song_hotttnesss-desc')
#print
#print
ss_results_b =song.search(start = 75,song_max_hotttnesss=1.0,song_min_hotttnesss=0.8,buckets=['audio_summary','song_type'],results=25,sort ='song_hotttnesss-desc')
#print ss_results_b

ss_results_c = ss_results_a.extend(ss_results_b)
count = {}
for s in ss_results:
	count[s] = 0
count_a = {}
for s in ss_results_a:
	count_a[s] = 0

for s in count.keys():
	if s not in count_a.keys():
		print s
#for s in count:
#	print s
'''
#print ss_results[0].__dict__
'''
for i in ss_results[0].__dict__:
	if str(i) == 'cache':
		for j in ss_results[0].__dict__[i]:
			for k in ss_results[0].__dict__[i][j]:
				print str(k) + ': ',
				print ss_results[0].__dict__[i][j][k]
	else:		
		print str(i) + ': ',
		print ss_results[0].__dict__[i]
'''