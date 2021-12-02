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
    return executeQuery('SELECT * FROM ban, champion WHERE ban.champion_id = champion.champion_id').keys()

def getChampionHeader():
    return executeQuery('SELECT * FROM champion').keys()

def getMatchHeader():
    return executeQuery('SELECT * FROM match').keys()

def getPlayerHeader():
    return executeQuery('SELECT * FROM player').keys()

def getPlaysHeader():
    return executeQuery('SELECT plays.match_id, player.player_name, champion.champion_name, '
                        'plays.total_cs, plays.kills, plays.deaths, plays.assists, plays.role, '
                        'plays.team, plays.result, match.game_length, match.date '
                        'FROM plays, player, champion, match '
                        'WHERE plays.player_id = player.player_id '
                        'AND plays.champion_id = champion.champion_id '
                        'AND plays.match_id = match.match_id').keys()

# Get data
def getBanData():
    return db.session.query(ban, champion).join(champion).all()

def getChampionData():
    return db.session.query(champion).all()

def getMatchData():
    return db.session.query(match).all()

def getPlayerData():
    return db.session.query(player).all()

def getPlaysData():
    return db.session.query(plays, player, champion, match).join(player).join(champion).join(match).all()


# Search
def getChampion(search):
    champ = []
    totalCS = 0
    kills = 0
    deaths = 0
    assists = 0
    totalWins = 0
    totalBans = 0
    totalGames = 0
    avgCS = 0
    kda = 0
    winRate = 0
    data = getPlaysData()
    champ_id = 0
    champ_name = ""
    for i in data:
        if str(i.champion_id) == search or i.champion_name.lower() == search.lower():
            champ_id = i.champion_id
            champ_name = i.champion_name
            totalCS += i[3]
            kills += i[4]
            deaths += i[5]
            assists += i[6]
            totalGames += 1
            if i[9] == 1:
                totalWins += 1
    for i in getBanData():
        if str(i.champion_id) == search or i.champion_name.lower() == search.lower():
            totalBans += 1
    if totalGames > 0:
        avgCS = round(totalCS / totalGames, 2)
        kda = round((kills + assists) / deaths, 2)
        winRate = round(totalWins / totalGames, 2)
        banRate = round(totalBans / len(getMatchData()), 2)
        list = [champ_id, champ_name, avgCS, kda, winRate, banRate]
        champ.append(list)
    return champ

def getPlayer(search):
    player = []
    for i in getPlaysData():
        if str(i.player_id) == search or i.player_name.lower() == search.lower():
            list = [i.match_id, i.player_name, i.champion_name, i.total_cs, i.kills, i.deaths,
                    i.assists, i.role, i.team, i.result, i.game_length // 60, i.date]
            player.append(list)
    return player

def getMatch(search):
    match = []
    for i in getMatchData():
        if i.match_id == search:
            match.append(i)
    return match

def getPlays(search):
    plays = []
    list = []

    for i in getPlaysData():
        if i.match_id == search:
            print(i)
            list = [i.match_id, i.player_name, i.champion_name, i.total_cs, i.kills, i.deaths,
                    i.assists, i.role, i.team, i.result, i.game_length // 60, i.date]
            plays.append(list)
    return plays


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
            headings = ['champion_id', 'champion_name', 'average_cs', 'kda', 'average_win_rate', 'average_ban_rate']
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
            headings = getPlaysHeader()
            result = getPlayer(search)
            if len(result) == 0:
                headings = []
                data = []
                flash("No Result")
            else:
                data = result
                totalCS = 0
                kills = 0
                deaths = 0
                assists = 0
                totalWins = 0
                for i in data:
                    totalCS += i[3]
                    kills += i[4]
                    deaths += i[5]
                    assists += i[6]
                    if i[9] == 1:
                        totalWins += 1
                avgCS = round(totalCS / len(data), 2)
                kda = round((kills + assists) / deaths, 2)
                winRate = round(totalWins / len(data), 2)
                flash("Average Win Rate: " + str(winRate))
                flash("Average CS: " + str(avgCS))
                flash("Average KDA: " + str(kda))

    elif select == 'match':
        headings = getMatchHeader()
        if search == '':
            data = getMatchData()
        else:
            headings = getPlaysHeader()
            result = getPlays(search)
            if len(result) == 0:
                headings = []
                data = []
                flash("No Result")
            else:
                data = result

    return render_template('index.html', headings=headings, data=data)

if __name__ == '__main__':
    app.run(debug=True)