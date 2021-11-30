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

# Headers and data to fill table
headings = list()
data = list()

@app.route('/')
def index():
    headings = ("Champion ID", "Champion Name")
    results = db.session.query(champion).all()
    for i in results:
        data.append((i.champion_id, i.champion_name))
    return render_template('index.html', headings=headings, data=data)

if __name__ == '__main__':
    app.run()