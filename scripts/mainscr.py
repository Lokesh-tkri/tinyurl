from flask import Flask, escape, request, render_template, redirect
from hashlib import sha256
from pymysql import connect as con
from config import configs

app = Flask(__name__)

cfs = configs()

@app.route('/')
def hello():
    return render_template("mainpage.html")

@app.route('/urlpage',  methods = ['POST'])
def urlpage():
    url = request.form["furl"]
    hashcode = str(sha256(url.encode('utf-8')).hexdigest()[:8])
    db = con(cfs.machinename, cfs.username, cfs.password, cfs.dbase)
    cursor = db.cursor()
    sqlquery = f"insert into urls (oriurl, hashurl) values(%s,%s)"
    try:
        cursor.execute(sqlquery,(str(url), str(hashcode)))
        db.commit()
    except:
        db.rollback()
    db.close()
    return render_template(
                        "urlpage.html", 
                        urllink = f"http://localhost:56000/{hashcode}")

@app.route('/<urllink>')
def newpage(urllink = None):
    db = con(cfs.machinename, cfs.username, cfs.password, cfs.dbase)
    cursor = db.cursor()
    sqlquery = f"select oriurl from urls where hashurl = (%s)"
    try:
        cursor.execute(sqlquery,(str(urllink)))
        result = cursor.fetchall()
        db.close()
        return redirect(result[0][0])
    except:
        db.close()
        return render_template("errorpage.html")


if __name__ == "__main__":
    app.run(debug = True, port = 56000)