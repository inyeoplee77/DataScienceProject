from instagram.client import InstagramAPI
import requests
from BeautifulSoup import BeautifulSoup
import sys
import locale
import re
import pickle
import numpy as np
reload(sys)

sys.setdefaultencoding('utf8')
access_token='1085114028.582f029.208ffc1f880049b49b96db01f78e049b'
api=InstagramAPI(access_token=access_token)
client_id='582f02988f5b48baa669fedc9d51fb06'

#get tags data from files
tags_dic={}
music_tags=open('music_tag','r')

for line in music_tags:
	title=line.split('::')[0].strip()
	tags=line.split('::')[1].strip().split(' ')
	tags_dic[title]=tags

movie_tags=open('movie_tag','r')
for line in movie_tags:
	title='movie_'+line.split('::')[0].strip()
	tags=line.split('::')[1].strip().split(' ')
	tags_dic[title]=tags
	
	
	
from sklearn.svm import SVC
from sklearn.externals import joblib
clf = joblib.load('SVM.pkl')	
_data = pickle.load(open('vector.p','rb'))
y = pickle.load(open('y_vector','rb'))
y = y.keys()
while True:
	username=raw_input('What is your instagram UserName? :')
	if username=='q':
		break
	#get user id from username
	url='https://api.instagram.com/v1/users/search?q='+username+'&client_id='+client_id
	result=requests.get(url).json()
	data=result['data']

	for datum in data:
		if datum['username']==username:
			print datum['username']
			user_id=datum['id']
			print user_id
			break

	#get contents from user
	#temp id
	#user_id='453076946'
	url_user='https://api.instagram.com/v1/users/'+user_id+'/media/recent/?client_id='+client_id
	#print url_user
	user_tags=[]
	temp=[]
	check_list=['listening','music','listeningto','nowlisteningto']
	result_user=requests.get(url_user).json()
	while True:
		if 'data' not in result_user:
			next_url=result_user['pagination']
			next_url=next_url['next_url']
			result_user=requests.get(next_url).json()		
			continue
		data_user=result_user['data']
		
		for i in data_user:			
			if any(map(lambda v:v in check_list,i['tags'])):
				#print i['tags']
				for j in i['tags']:
					if j not in user_tags:
						user_tags.append(j)
				#if i['tags'] not in user_tags:
				#	user_tags.append(i['tags'])
			else:
				for k in i['tags']:
					if 'movie' in k:
						for l in i['tags']:
							if l not in user_tags:
								user_tags.append(l)
						break
		next_url=result_user['pagination']
		if 'next_url' not in next_url:
			break
		next_url=next_url['next_url']
		result_user=requests.get(next_url).json()
	

	
	#find valid contents from tags
	valid_tag=[]
	
	for user_tag_item in user_tags:
		is_found=0
		for title, tags in tags_dic.iteritems():
			if is_found==1:
				break
			for tag_item in tags:
				if user_tag_item==tag_item:
					if title not in valid_tag:
						valid_tag.append(title)
						is_found=1
						break
	print valid_tag
	for sample in valid_tag:
		_data = dict.fromkeys(_data,0)
		for a in sample:
			music_db = file('Music_DB.txt','r')
			movie_db = file('Movie_DB.txt','r')
			if 'movie_' in a:
			    a = a.split('movie_')[1]
			    for line in movie_db:
			        if 'title' in line and  a == line.split('title:')[1].strip():
			            _line = movie_db.next()
			        else:
			            continue
			        while(_line.split(':')[0].strip()!='title'):
			            if(_line.split(':')[0]=='rating'):
			                string = 'rate:'+str(int(float(_line.split(':')[1].replace('\n',''))))
			                if string.strip() in _data:
			                    _data[string.strip()]=1
			            elif(_line.split(':')[0]=='director'):
			                director = _line.split(':')[1].split(',')
			                for c in director:
			                    if c.strip() in _data:
			                        _data[c.strip()]=1
			            elif(_line.split(':')[0]=='stars'):
			                stars = _line.split(':')[1].split(',')
			                for c in stars:
			                    if c.strip() in _data:
			                        _data[c.strip()]=1
			            elif(_line.split(':')[0]=='genres'):
			                genres = _line.split(':')[1].split(',')
			                for c in genres:
			                    if c.strip() in _data:
			                        _data[c.strip()]=1
			            #votes: 5103 ~ 1419284
			            elif _line.split(':')[0] == 'votes' :
			                votes = float(_line.split(':')[1].replace(',',''))
			                votes = votes - 5103
			                votes = int(votes/141418)
			                #print votes
			                string = 'votes:' + str(votes)
			               #if string.strip() in _data:
			                _data[string.strip()] = 1
			            _line = movie_db.next()
			#if a is song title
			else:
			    for line in music_db:
			        if 'title' in line and str(a) == line.split('title:')[1].strip():
			            _line = music_db.next()
			            while(_line.split(':')[0].strip()!='title'):
			                if(_line.split(':')[0]=='artist'):
			                    string = _line.split(':')[1].strip()
			                    if string in _data:
			                        _data[string]=1
			                elif(_line.split(':')[0]=='energy'):
			                    ene = float(_line.split(':')[1].strip())
			                    string = 'energy:'+(str)((int)(ene/0.1))
			                    if string in _data:
			                        _data[string]=1
			                elif(_line.split(':')[0]=='liveness'):
			                    live = float(_line.split(':')[1].strip())
			                    string = 'liveness:'+(str)((int)(live/0.1))
			                    if string in _data:
			                        _data[string]=1
			                elif(_line.split(':')[0]=='tempo'):
			                    tempo = int(float(_line.split(':')[1].strip()))-65
			                    tempo /= 15
			                    string = 'tempo:'+str(tempo)
			                    if string in _data:
			                        _data[string]=1
			                elif(_line.split(':')[0]=='speechiness'):
			                    a = float(_line.split(':')[1].strip())
			                    string = 'speechiness:'+(str)((int)(a/0.1))
			                    if string in _data:
			                        _data[string]=1
			                elif(_line.split(':')[0]=='acousticness'):
			                    a = float(_line.split(':')[1].strip())
			                    string = 'acousticness:'+(str)((int)(a/0.1))
			                    if string in _data:
			                        _data[string]=1
			                elif(_line.split(':')[0]=='danceability'):
			                    a = float(_line.split(':')[1].strip())
			                    string = 'danceability:'+(str)((int)(a/0.1))
			                    if string in _data:
			                        _data[string]=1
			                elif(_line.split(':')[0]=='instrumentalness'):
			                    a = float(_line.split(':')[1].strip())
			                    string = 'instrumentalness:'+(str)((int)(a/0.1))
			                    if string in _data:
			                        _data[string]=1
			                elif(_line.split(':')[0]=='loudness'):
			                    a = float(_line.split(':')[1].strip())+31
			                    string = 'loudness:'+str((int)(a/3.0))
			                    if string in _data:
			                        _data[string]=1
			                elif(_line.split(':')[0]=='valence'):
			                    a = float(_line.split(':')[1].strip())
			                    string = 'valeance:'+(str)((int)(a/0.1))
			                    if string in _data:
			                        _data[string]=1
			                elif(_line.split(':')[0]=='song_hotttnesss'):
			                    a = float(_line.split(':')[1].strip())-0.67
			                    string = 'song_hotttnesss:'+(str)((int)(a/0.03))
			                    if string in _data:
			                        _data[string]=1
			                elif(_line.split(':')[0]=='song_type' or _line.split(':')[0]=='artist_terms'):
			                    a = _line.split(':')[1].split(',')
			                    for b in a:
			                        if b.strip() in _data:
			                            _data[b.strip()]=1
			                _line = music_db.next()
		if '\n' in _data:
		    del _data['\n']
		if '' in _data:
		    del _data['']
	x = np.array([_data.values()])
	y_index = clf.predict(x)
	print y[y_index[0]]