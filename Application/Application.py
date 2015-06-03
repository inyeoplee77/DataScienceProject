from instagram.client import InstagramAPI
import requests
from BeautifulSoup import BeautifulSoup
import sys
import locale
import re
reload(sys)

sys.setdefaultencoding('utf8')
access_token='1085114028.582f029.208ffc1f880049b49b96db01f78e049b'
api=InstagramAPI(access_token=access_token)
client_id='582f02988f5b48baa669fedc9d51fb06'

#get tags data from files
tags_dic={}
music_tags=open('music_tag','r')

for line in music_tags:
	title='music_'+line.split('::')[0].strip()
	tags=line.split('::')[1].strip().split(' ')
	tags_dic[title]=tags

movie_tags=open('movie_tag','r')
for line in movie_tags:
	title='movie_'+line.split('::')[0].strip()
	tags=line.split('::')[1].strip().split(' ')
	tags_dic[title]=tags
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
	user_id='453076946'
	url_user='https://api.instagram.com/v1/users/'+user_id+'/media/recent/?client_id='+client_id
	print url_user
	user_tags=[]
	temp=[]
#	check_list=[]
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
			else :
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

from sklearn.svm import SVC
from sklearn.externals import joblib

clf = joblib.load('SVM.pkl')

