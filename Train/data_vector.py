import sys
reload(sys)
sys.setdefaultencoding('utf8')
x = []
y = []
_data = {}
max_loud = -50.0
min_loud = 0.0
music_db = open('Music_DB.txt','r')
movie_db = open('Movie_DB.txt','r')

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
    elif(a.split(':')[0]=='loudness'):
        loudness = float(a.split(':')[1].strip())
        if(loudness > max_loud):
            max_loud = loudness
        if(loudness < min_loud):
            min_loud = loudness
print (max_loud-min_loud)/10.0
print min_loud
for a in movie_db:
    if(a.split(':')[0]=='director'):
        director = a.split(':')[1].split(',')
        for b in director:
            _data[b]=0
    elif(a.split(':')[0]=='stars'):
        stars = a.split(':')[1].split(',')
        for b in stars:
            _data[b]=0
    elif(a.split(':')[0]=='genres'):
        genres = a.split(':')[1].split(',')
        for b in genres:
            _data[b]=0
    
#making features which need to be separated into 10 parts
for a in range(0,9):
    string = 'energy:'+str(a)
    _data[string]=0
    string = 'liveness:'+str(a)
    _data[string]=0
    string = 'tempo:'+str(a)
    _data[string]=0
    string = 'speechiness:'+str(a)
    _data[string]=0
    string = 'acousticness:'+str(a)
    _data[string]=0
    string = 'danceability:'+str(a)
    _data[string]=0
    string = 'instrumantalness:'+str(a)
    _data[string]=0
    string = 'valence:'+str(a)
    _data[string]=0
    string = 'hotttnesss:'+str(a)
    _data[string]=0
    string = 'vote:'+str(a)
    _data[string]=0
    string = 'rate:'+str(a)
    _data[string]=0


#search element(movie, music) in list
samples_f = open('samples.txt','r')
sample = []
sample.append(samples_f.readline().strip())
tmp = samples_f.readline().split(',,')
sample.extend(tmp[0].split(','))
sample_answer = tmp[1].strip()
#print sample,sample_answer
#format: title1 title2 title3 .... 
for title in sample:
    _data = dict.fromkeys(_data, 0)
    music_db.close()
    movie_db.close()
    music_db = open('Music_DB.txt','r')
    movie_db = open('Movie_DB.txt','r')
    #if a is movie title
    while True:
        line = movie_db.readline()
        if not line:
            break
        
        if title == line.split(':')[1].strip():
            _line = movie_db.readline()
            while(_line.split(':')[0].strip()!='title'):
                if(_line.split(':')[0]=='rating'):
                    string = 'rate'+str(int(float(_line.split(':')[1].replace('\n',''))))
                    _data[string]=1
                elif(_line.split(':')[0]=='director'):
                    director = _line.split(':')[1].split(',')
                    for c in director:
                        _data[c]=1
                elif(_line.split(':')[0]=='stars'):
                    stars = _line.split(':')[1].split(',')
                    for c in stars:
                        _data[c]=1
                elif(_line.split(':')[0]=='genres'):
                    genres = _line.split(':')[1].split(',')
                    for c in genres:
                        _data[c]=1
                _line = movie_db.readline()

    #if a is song title
    while True:
        line = music_db.readline()
        if not line:
            break
        if title == line.split(':')[1].strip():
            _line = music_db.readline()
            while(_line.split(':')[0].strip()!='title'):
                if(_line.split(':')[0]=='artist'):
                    _data[_line.split(':')[1].strip()]=1
                elif(_line.split(':')[0]=='energy'):
                    ene = float(_line.split(':')[1].strip())
                    string = 'energy:'+(str)((int)(ene/0.1))
                    _data[string]=1
                elif(_line.split(':')[0]=='liveness'):
                    live = float(_line.split(':')[1].strip())
                    string = 'liveness:'+(str)((int)(live/0.1))
                    _data[string]=1
                elif(_line.split(':')[0]=='tempo'):
                    tempo = int(float(_line.split(':')[1].strip()))-65
                    tempo /= 15
                    string = 'tempo:'+str(tempo)
                    _data[string]=1
                elif(_line.split(':')[0]=='speechiness'):
                    a = float(_line.split(':')[1].strip())
                    string = 'speechiness:'+(str)((int)(a/0.1))
                    _data[string]=1
                elif(_line.split(':')[0]=='acousticness'):
                    a = float(_line.split(':')[1].strip())
                    string = 'acousticness:'+(str)((int)(a/0.1))
                    _data[string]=1
                elif(_line.split(':')[0]=='danceability'):
                    a = float(_line.split(':')[1].strip())
                    string = 'danceability:'+(str)((int)(a/0.1))
                    _data[string]=1
                elif(_line.split(':')[0]=='instrumentalness'):
                    a = float(_line.split(':')[1].strip())
                    string = 'instrumentalness:'+(str)((int)(a/0.1))
                    _data[string]=1
                elif(_line.split(':')[0]=='loudness'):
                    a = float(_line.split(':')[1].strip())+31
                    string = 'loudness:'+str((int)(a/3.0))
                    _data[string]=1
                elif(_line.split(':')[0]=='valence'):
                    a = float(_line.split(':')[1].strip())
                    string = 'valeance:'+(str)((int)(a/0.1))
                    _data[string]=1
                elif(_line.split(':')[0]=='song_hotttnesss'):
                    a = float(_line.split(':')[1].strip())-0.67
                    string = 'song_hotttnesss:'+(str)((int)(a/0.03))
                    _data[string]=1
                elif(_line.split(':')[0]=='song_type' or _line.split(':')[0]=='artist_terms'):
                    a = _line.split(':')[1].split(',')
                    for b in a:
                        _data[b.strip()]=1
                _line = music_db.readline()
    x.append(_data)

#delete unnecessary features
del _data['\n']
del _data['']
print x

#x will be the list of vector