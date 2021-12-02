from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "super secret key"

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

# Search
def getChampion(search):
    champ = []
    for i in getChampionData():
        if str(i.champion_id) == search or i.champion_name.lower() == search.lower():
            champ.append(i)
    return champ

def getPlayer(search):
    player = []
    for i in getPlayerData():
        if str(i.player_id) == search or i.player_name.lower() == search.lower():
            player.append(i)
    return player

def getMatch(search):
    match = []
    for i in getMatchData():
        if i.match_id == search:
            print(i)
            match.append(i)
    return match


# Headers and data to fill table
headings = list()
data = list()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    select = request.form.get('category')
    search = request.form.get('search')
    if select == 'champion':
        headings = getChampionHeader()
        if search == '':
            data = getChampionData()
        else:
            result = getChampion(search)
            if len(result) == 0:
                headings = []
                data = []
                flash("No Result")
            else:
                data = result

    elif select == 'player':
        headings = getPlayerHeader()
        if search == '':
            data = getPlayerData()
        else:
            result = getPlayer(search)
            if len(result) == 0:
                headings = []
                data = []
                flash("No Result")
            else:
                data = result

    elif select == 'match':
        headings = getMatchHeader()
        if search == '':
            data = getMatchData()
        else:
            result = getMatch(search)
            if len(result) == 0:
                headings = []
                data = []
                flash("No Result")
            else:
                data = result
    return render_template('index.html', headings=headings, data=data)

if __name__ == '__main__':
    app.run(debug=True)