import os
import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit



app = Flask(__name__)

app.config['ENV'] = 'development'

"""
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
"""

# Configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['DEBUG'] = True
app.config["SECRET_KEY"]= os.getenv("SECRET_KEY")

socketio = SocketIO(app)

Session(app)

"""username list"""
users=[]

""" chanels list """
chanels=[]

""" messages """
messages=[]



@app.route("/", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
def index():


    print(f"this is the chanels {chanels}")
    print(f"this is the users: {users}")

    return render_template("index.html", users=users, messages=messages, chanels=chanels)




@socketio.on("submit message")
def message(data):

    message = data["message"]
    print(f"this is the the message: {message}")
    messages.append( session["username"] + ": " +  message )
    #messagedict = {"message": message, "username": session["username"]}
    #messagedict["message"] = message
    #messagedict["user_name"]= session["username"]

    #messages["message"].append(messagedict["message"])
    emit("send message",  {'username': session["username"], 'message': message, 'chanel': session['chanel'] },  broadcast=True)


@app.route("/username", methods=["GET", "POST"])
def user():

    username = request.form.get("username")

    session["username"]=username

    users.append(username)


    if not username:
        return jsonify({"success": False})

    return render_template("index.html")

@app.route("/createchanel", methods=["GET", "POST"])
def addchanel():

    new_chanel = request.form.get("newchanel")

    session["chanel"]=new_chanel

    chanels.append(new_chanel)


    return redirect("index.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    socketio.run(app)
