import flask as fk
import re
import logging
from replit import db
import datetime
import sqlite3


def write_form(
    error="",
    arts=""):
    
    return fk.render_template(
        'home.html',
        error=error,
        arts=arts,
)

app = fk.Flask(
    __name__,
    static_folder="stylesheets"
)

def get_arts():
    with sqlite3.connect("blogbosts.db") as con:
        cursor = con.cursor()
        s = cursor.execute("SELECT * FROM posts ORDER BY create_date DESC")

        # print([row for row])
        return(s)

@app.route('/', methods=["GET", "POST"])
def root():
    method = fk.request.method
    if method == "GET":
        with sqlite3.connect("blogbosts.db") as con:
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, create_date TEXT, subject TEXT, content TEXT)")
        return(write_form(error="", arts=get_arts()))
    elif method == "POST":
        title = fk.request.form['title']
        art = fk.request.form['art']
        error = ""
        if title == "" or art == "":
            error = "Need both a title and some artwork!"
        else:
            with sqlite3.connect("blogbosts.db") as con:
                cursor = con.cursor()
                now_date = datetime.datetime.now()
                new_art = (now_date, title, art, )
                cursor.execute("INSERT INTO posts(create_date, subject, content) VALUES (?, ?, ?)", new_art)
        return(write_form(error=error, arts=get_arts()))
            

@app.route('/welcome', methods=["GET", "POST"])
def welcome():
    username = fk.request.form['username']
    return(fk.render_template('welcome.html', username=username))
    
app.run(host='0.0.0.0', port='3000')