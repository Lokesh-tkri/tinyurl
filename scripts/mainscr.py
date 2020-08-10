from flask import Flask, escape, request, render_template, redirect
from hashlib import sha256
from pymysql import connect as con
import pymysql as pys

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("mainpage.html")

@app.route('/urlpage',  methods = ['POST'])
def urlpage():
    url = request.form["furl"]
    hashcode = str(sha256(url.encode('utf-8')).hexdigest()[:8])
    db = con("localhost", "test", "mysql.567", "myperdb")
    cursor = db.cursor()
    sqlquery = f"insert into urls (oriurl, hashurl) values('{url}','{hashcode}')"
    try:
        cursor.execute(sqlquery)
        db.commit()
    except:
        db.rollback()
    db.close()
    return render_template(
                        "urlpage.html", 
                        urllink = f"http://localhost:56000/{hashcode}")

@app.route('/<urllink>')
def newpage(urllink = None):
    db = con("localhost", "test", "mysql.567", "myperdb")
    cursor = db.cursor()
    sqlquery = f"select oriurl from urls where hashurl = '{urllink}'"
    try:
        cursor.execute(sqlquery)
        result = cursor.fetchall()
        db.close()
        return redirect(result[0][0])
    except:
        db.close()
        return render_template("errorpage.html")


if __name__ == "__main__":
    app.run(debug = True, port = 56000)