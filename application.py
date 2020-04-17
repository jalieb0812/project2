import os
import requests
import datetime
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
chanels_list=[]

""" messages """
messages_dict=dict()



@app.route("/", methods=["GET", "POST"])
def index():

    #new_chanel = request.form.get("newchanel")

    #session["chanel"]=new_chanel
    #print (f" chanel in index is {new_chanel}")

    #chanels.append(new_chanel)

    print(f"this is the chanels {chanels_list}")
    print(f"this is the users: {users}")
    print(f"these are the messages: {messages_dict}")

    return render_template("index.html", users=users, messages_dict=messages_dict, chanels_list=chanels_list)


@app.route("/chanels", methods=["GET", "POST"])
def chanels():

    if request.method == "GET":

        return render_template("chanels.html", users=users, messages_dict=messages_dict, chanels_list=chanels_list)

    if request.method == "POST":
        redirect(url_for('/'))


@socketio.on("submit message")
def message(data):

    message = data["message"]

    print(f"this is the  message: {message}")

    timestamp = datetime.datetime.now().strftime("Date: %Y-%m-%d Time: %H:%M:%S")



    chanel= chanels_list[len(chanels_list) - 1]

    print(f"this is the chanel in submit message: {chanel}")


    messages_dict["new_chanel"].append( timestamp + ": " + session["username"] + ": " +  message )

    #messagedict = {"message": message, "username": session["username"]}
    #messagedict["message"] = message
    #messagedict["user_name"]= session["username"]

    #messages["message"].append(messagedict["message"])
    emit("send message",  { 'timestamp': timestamp, 'username': session["username"], 'message': message },  broadcast=True)


""" route for sending the stored messages """
@app.route("/messages")
def messages():

    if request.method == "GET":

        return messages_dict

""" route for generating username"""
@app.route("/username", methods=["POST"])
def user():


    username = request.form.get("username")

    #if user somehow failed to enter the username b/c my javascript failed
    if not username or username == '':
        return jsonify({"success": False})

    #if user succeded in entering a username
    else:

        session["username"]=username

        users.append(username)

        return jsonify({"success": True, "username": username})

@app.route("/createchanel", methods=["POST"])
def createchanel():


    new_chanel = request.form.get('new_chanel')


    if not new_chanel:
        return jsonify({"success": False})

    session["chanel"]=new_chanel

    print (f"chanel is {new_chanel}")

    #add chanel to chanel list
    chanels_list.append(new_chanel)

    """ add chanel to messages dict"""
    messages_dict["new_chanel"]=[]
    print(f"this is messages_dict {messages_dict}: ")

    return jsonify({"success": True, "new_chanel": new_chanel})




@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    socketio.run(app)
