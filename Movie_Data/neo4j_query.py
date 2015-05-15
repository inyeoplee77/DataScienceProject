import sys
import locale

reload(sys)
sys.setdefaultencoding('utf8')
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8' )


db = open('Movie_DB.txt','r')

#from neo4jrestclient.client import GraphDatabase

#url = "http://localhost:7474/db/data/"

#gdb = GraphDatabase(url,username = 'neo4j',password = 'dldlsduq')


f = open('query.cql','w')


while True:
	title = db.readline()
	if not title:
		break
	title = title.rstrip().split(':',1)[1]
	year = int(db.readline().rstrip().split(':')[1][1:5])
	rating = float(db.readline().rstrip().split(':')[1])
	votes = locale.atoi(db.readline().rstrip().split(':')[1])
	directors = db.readline().rstrip().split(':',1)[1].split(',')[:-1]	
	stars = db.readline().rstrip().split(':',1)[1].split(',')[:-1]
	genres = db.readline().rstrip().split(':',1)[1].split(',')[:-1]
	
	for i in range(0,len(genres)):
		genres[i] = genres[i].replace("-","_")
	q = []
	q.append("CREATE (m:MOVIE")
	for genre in genres:
		q.append(":"+genre.upper())
	q.append("{title:\"" + title +"\",")
	q.append("year:" + str(year) + ",")
	q.append("rating:" + str(rating) + ",")
	q.append("votes:" + str(votes) + "}) ")
	for i in range(0,len(stars)):
		q.append("MERGE (s"+str(i)+":STAR {name:\"" + stars[i] + "\"}) ")
		q.append("CREATE (s"+str(i)+")-[:ACTED_IN]->(m) ")
	for i in range(0,len(directors)):
		q.append("MERGE (d"+str(i)+":DIRECTOR {name:\"" + directors[i] + "\"}) ")
		q.append("CREATE (d" +str(i)+")-[:FILMED]->(m) ")
	for i in range(0,len(stars)):
		for j in range(0,len(directors)):
			q.append("MERGE (s"+str(i)+")-[w"+str(i)+str(j)+":WORKED_WITH]-(d"+str(j)+") ON CREATE SET w"+str(i)+str(j)+".times = 1 ON MATCH SET w"+str(i)+str(j)+".times = w"+str(i)+str(j)+".times+1 ")
	q.append(";\n\n")
	f.write(''.join(q))
	#result = gdb.query(''.join(q),data_contents=True)
	print title
	
			