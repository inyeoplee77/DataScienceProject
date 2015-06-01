import sys
reload(sys)
sys.setdefaultencoding('utf8')
x = []
y = []
_data = {}
max_loud = -50.0
min_loud = 0.0
music_db = file('Music_DB.txt','r')
movie_db = file('Movie_DB.txt','r')

#making features
for a in music_db:
    if (a.split(':')[1].strip()=='None'):
        continue
    if(a.split(':')[0]=='artist'):
        _data[a.split(':')[1].strip()]=1
    elif(a.split(':')[0]=='song_type'):
        song_type = a.split(':')[1].split(',')
        for b in song_type:
            _data[b.strip()]=0
    elif(a.split(':')[0]=='artist_terms'):
        art_term = a.split(':')[1].split(',')
        for b in art_term:
            _data[b.strip()]=0

for a in movie_db:
    if(a.split(':')[0]=='director'):
        director = a.split(':')[1].split(',')
        for b in director:
            _data[b.strip()]=0
    elif(a.split(':')[0]=='stars'):
        stars = a.split(':')[1].split(',')
        for b in stars:
            _data[b.strip()]=0
    elif(a.split(':')[0]=='genres'):
        genres = a.split(':')[1].split(',')
        for b in genres:
            _data[b.strip()]=0


#making features which need to be separated into 10 parts
for a in range(0,10):
    string = 'energy:'+str(a)
    _data[string]=0
    string = 'liveness:'+str(a)
    _data[string]=0
    string = 'loudness:'+str(a)
    _data[string]=0
    string = 'tempo:'+str(a)
    _data[string]=0
    string = 'speechiness:'+str(a)
    _data[string]=0
    string = 'acousticness:'+str(a)
    _data[string]=0
    string = 'danceability:'+str(a)
    _data[string]=0
    string = 'instrumentalness:'+str(a)
    _data[string]=0
    string = 'valeance:'+str(a)
    _data[string]=0
    string = 'song_hotttnesss:'+str(a)
    _data[string]=0
    string = 'vote:'+str(a)
    _data[string]=0
    string = 'rate:'+str(a)
    _data[string]=0

if '' in _data:
    del _data['']
if '\n' in _data:
    del _data['\n']
print len(_data)
#search element(movie, music) in list
title = ['Inception','See You Again','Thinking Out Loud','The Hobbit: An Unexpected Journey','Star Wars: Episode VI - Return of the Jedi','No Country for Old Men','Hozier','Sugar','Elastic Heart']
#format: title1 title2 title3 .... 
for a in title:
    _data = dict.fromkeys(_data, 0)
    music_db.close()
    movie_db.close()
    music_db = file('Music_DB.txt','r')
    movie_db = file('Movie_DB.txt','r')
    #if a is movie title
    for line in movie_db:
        if a == line.split(':')[1].strip():
            _line = movie_db.next()
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
                _line = movie_db.next()

    #if a is song title
    for line in music_db:
        if str(a) == line.split(':')[1].strip():
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
    x.append(_data)
#delete unnecessary features



#x will be the list of vector
#for a in x:
    #print [name for name, value in a.items() if value == 1]
    #print len(a)
f = open('test.txt','w') 
f.write(str(x[0]))