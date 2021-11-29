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

cursor.execute("DROP TABLE IF EXISTS Player")

#Creating table as per requirement
sql ='''CREATE TABLE Player (
player_id    SERIAL PRIMARY KEY,
player_name  varchar(50) UNIQUE NOT NULL 
);
'''
cursor.execute(sql)

#Closing the connection
conn.commit()
conn.close()