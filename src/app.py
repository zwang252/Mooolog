# Team Mooo - Brian Lee, Emily Lee, Thomas Lee, Joshua Weiner
# SoftDev1 pd6
# P00 -- The Art of Storytelling
# 2018-10-17

from flask import Flask, session, render_template, url_for, redirect, request, flash
from datetime import datetime
from util import authenticate, make_blog
import os
import sys
os.chdir(sys.path[0])

app = Flask(__name__)
app.secret_key=os.urandom(32)

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/register', methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return render_template("register.html")
    else:
        success, message = authenticate.register_user(
                request.form['username'],
                request.form['password'],
                request.form['re-enter password'])
        flash(message)
        if success:
            return render_template("/main.html")
        else:
            return redirect(url_for('reg'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get('loggedin') is None:
            return render_template("login.html")
        else:
            flash("You are already logged in!")
            return redirect(url_for('userpage', username=session.get('loggedin')))
    else:
        success, message = authenticate.login_user(
                request.form['username'],
                request.form['password'])
        flash(message)
        if success:
            session['loggedin']=request.form['username']
            return redirect(url_for('userpage', username=request.form['username']))
        else:
            return redirect(url_for('login'))

@app.route('/user/<username>')
def userpage(username):
    if authenticate.user_exists(username):
        user_id = make_blog.find_id(username)
        blogs = make_blog.get_titles(user_id)
        # print(blogs)
        return render_template("userpage.html", username=username, blogs=blogs)
    else:
        return "temp"

@app.route('/logout', methods=["GET", "POST"])
def logout():
    if 'loggedin' in session:
        session.pop('loggedin')
        flash("Successfully logged out.")
    else:
        flash("You are not logged in.")
    return redirect(url_for('main'))

@app.route('/create', methods=["GET", "POST"])
def create():
    if session.get('loggedin') is None:
        flash("You must be logged in to create a post")
        return redirect(url_for('main'))
    elif request.method=="GET":
        return render_template("create.html")
    else:
        time = str(datetime.now())
        print(request.form['title'])
        success, message = make_blog.create(
            request.form['title'],
            request.form['category'],
            session['loggedin'],
            time
        )
        flash(message)
        if success:
            return redirect(url_for('userpage', username=session['loggedin']))
        else:
            return redirect(url_for('create'))


if __name__ == "__main__":
    app.debug=True
    app.run()
