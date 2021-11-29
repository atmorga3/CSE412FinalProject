from flask import Flask, render_template

app = Flask(__name__)

headings = ("h1", "h2", "h3")
data = (
    ("r1", "r1", "r1"),
    ("r2", "r2", "r2"),
    ("r3", "r3", "r3")
)

@app.route('/')
def index():
    return render_template('index.html', headings=headings, data=data)

if __name__ == '__main__':
    app.run()