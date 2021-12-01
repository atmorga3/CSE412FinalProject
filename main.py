from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Access database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass@localhost/postgres'
db = SQLAlchemy(app)

# Get all tables
ban = db.Table('ban', db.metadata, autoload=True, autoload_with=db.engine)
champion = db.Table('champion', db.metadata, autoload=True, autoload_with=db.engine)
match = db.Table('match', db.metadata, autoload=True, autoload_with=db.engine)
player = db.Table('player', db.metadata, autoload=True, autoload_with=db.engine)
plays = db.Table('plays', db.metadata, autoload=True, autoload_with=db.engine)

# Execute a query and return results
def executeQuery(query):
    return db.session.execute(query)

# Get headers
def getBanHeader():
    return executeQuery('SELECT * FROM ban').keys()

def getChampionHeader():
    return executeQuery('SELECT * FROM champion').keys()

def getMatchHeader():
    return executeQuery('SELECT * FROM match').keys()

def getPlayerHeader():
    return executeQuery('SELECT * FROM player').keys()

def getPlaysHeader():
    return executeQuery('SELECT * FROM plays').keys()

# Get data
def getBanData():
    return db.session.query(ban).all()

def getChampionData():
    return db.session.query(champion).all()

def getMatchData():
    return db.session.query(match).all()

def getPlayerData():
    return db.session.query(player).all()

def getPlaysData():
    return db.session.query(plays).all()

# Headers and data to fill table
headings = list()
data = list()

@app.route('/')
def index():
    headings = getChampionHeader()
    data = getChampionData()
    return render_template('index.html', headings=headings, data=data)

if __name__ == '__main__':
    app.run()