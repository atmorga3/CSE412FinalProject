import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="postgres", user='postgres', password='pass', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS project412")
#Preparing query to create a database
sql = '''CREATE database project412''';

#Creating a database
cursor.execute(sql)
print("Database created successfully........")
conn = psycopg2.connect(
   database="project412", user='postgres', password='pass', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

cursor.execute("DROP TABLE IF EXISTS Player CASCADE")
cursor.execute("DROP TABLE IF EXISTS Champion CASCADE")
cursor.execute("DROP TABLE IF EXISTS Match CASCADE")
cursor.execute("DROP TABLE IF EXISTS Plays CASCADE")
cursor.execute("DROP TABLE IF EXISTS Ban CASCADE")
cursor.execute("DROP TABLE IF EXISTS temp_lol_esports CASCADE")

#Creating table as per requirement
sql ='''
CREATE TABLE Player (
player_id    SERIAL PRIMARY KEY,
player_name  varchar(50) UNIQUE NOT NULL 
);

CREATE TABLE Champion (
champion_id   SERIAL PRIMARY KEY, 
champion_name varchar (50) UNIQUE NOT NULL 
);

CREATE TABLE Match (
match_id    varchar(250) NOT NULL PRIMARY KEY, 
game_length integer, 
date        timestamp 
);

CREATE TABLE Plays (
match_id    varchar(250) NOT NULL, 
player_id   integer NOT NULL, 
champion_id	integer NOT NULL, 
total_cs integer, 
kills    integer, 
deaths   integer, 
assists  integer, 
role     varchar(15), 
team     varchar(150), 
result   integer,
PRIMARY KEY (match_id, player_id, champion_id), 
FOREIGN KEY (match_id)
	REFERENCES Match(match_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (player_id)
	REFERENCES Player(player_id) ON DELETE NO ACTION ON UPDATE CASCADE,
FOREIGN KEY (champion_id)
	REFERENCES Champion(champion_id) ON DELETE NO ACTION ON UPDATE CASCADE 
);

CREATE TABLE Ban (
ban_id       SERIAL PRIMARY KEY,
match_id     varchar(250) NOT NULL, 
champion_id  integer NOT NULL,  
FOREIGN KEY (match_id)
	REFERENCES Match(match_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (champion_id)
	REFERENCES Champion(champion_id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE temp_lol_esports (
id         SERIAL PRIMARY KEY,
gameid     varchar(250), 
url        text, 
league     varchar(15),
year       integer, 
date       timestamp, 
game       integer, 
playerid   integer, 
side       varchar(30), 
position   varchar(15), 
player     varchar(50), 
team       varchar(150),
champion   varchar(50),
ban1       varchar(50), 
ban2       varchar(50), 
ban3       varchar(50), 
ban4       varchar(50), 
ban5       varchar(50), 
gamelength  integer, 
result      integer, 
kills       integer, 
deaths      integer, 
assists     integer, 
totalcs     integer
);
'''
cursor.execute(sql)
#Closing the connection
conn.close()