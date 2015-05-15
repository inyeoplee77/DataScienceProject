singer = "maroon 5"
title = "this love"
def search_genre(singer, title):
    genre = d.search(title, artist=singer)
    if not d.search(title, artist=singer):
        print 'None'
        return -1
    else:
        genre = genre[0].genres
        print genre
        return genre
 
def search_album(singer, title):
    album = d.search(title, artist=singer,type='release',format='album')
    albums={}
    if not album:
        print 'No album'
        return -1
    else:
        for a in album:
            if a not in albums:
                albums[a.title] = 1
    for a in albums:
        print a
search_genre(singer,title)
search_album(singer,title)