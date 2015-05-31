from instagram.client import InstagramAPI
import requests
import sys
import locale
import re
import operator
reload(sys)

sys.setdefaultencoding('utf8')
access_token = '1085114028.582f029.208ffc1f880049b49b96db01f78e049b'

api = InstagramAPI(access_token=access_token)
users = {}

movies_f=open('Movie_DB.txt','r')
tags_f=open('Movie_tag.txt','w')
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
 
	#search movie title tags that have the most media
	tags_list = []
	tags_dic_count={}
	for title in titles:
		url='https://api.instagram.com/v1/tags/search?q='+title+'&access_token='+access_token
		for i in range(10):
			try:
				result=requests.get(url).json()
			except Exception as e:
				print e
				continue
			break
		if 'data' not in result:
			continue
		data=result['data']

		for datum in data:
			tags_dic_count[datum['name']]=datum['media_count']
			
	sorted_tags={}
#	print tags_dic_count
	sort_tags=sorted(tags_dic_count.items(),key=operator.itemgetter(1),reverse=True)
	
	cnt=0
	for key in sort_tags:
		if cnt<5:
			tags_list.append(key[0])
			cnt=cnt+1
		else:
			break
		'''
		tags = api.tag_search(q=title,count = 10)
		if not tags[0]:
			continue
		for t in tags[0]:
			if t.name not in tags_list:
				tags_list.append(t.name)
		'''
#	print tags_list
	return tags_list
   
for line in movies_f:
	if 'title' not in line:
		continue
	#print line.split('title:')[1]
	origin_title=line.split('title:')[1].strip()
	
	print origin_title
	tag_title=movie_tag(origin_title)
	tag=''
	for i in tag_title:
		tag+=i+' '

	tags_f.write(origin_title+'::'+tag+'\n')

movies_f.close()
tags_f.close()