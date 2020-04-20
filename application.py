import os
import requests
import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit
from loginrequired import login_required



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
messages_dict={}

messages_list=[]



@app.route("/", methods=["GET", "POST"])
@login_required
def index():

        session.get('username')
        print(f"this is the chanels {chanels_list}")

        return render_template("index.html",  users=users, chanels_list=chanels_list, messages_dict=messages_dict, messages_list=messages_list)


            #print(f"these are the messages: {messages_dict}")





    #new_chanel = request.form.get("newchanel")

    #session["chanel"]=new_chanel
    #print (f" chanel in index is {new_chanel}")

    #chanels.append(new_chanel)



    #return render_template("index.html", username=session["username"],users=users,
                            #messages_dict=messages_dict, chanels_list_=chanels_list)

@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():


    session.clear()



    if request.method=="POST":



        username = request.form.get("username")

        print(f"username is {username}")

        session['username']= username



        return redirect('/')

    if request.method=="GET":

        return render_template("sign_in.html")


""" route for generating username"""
@app.route("/username", methods=["POST"])
def user():



    # Forget any user_id
    session.clear()


    username = request.form.get("username")

    #if user somehow failed to enter the username b/c my javascript failed


    session["username"]=username

    users.append(username)


    return jsonify({"success": True, "username": username})

@app.route("/createchanel", methods=["GET", "POST"])
def createchanel():


    new_chanel = request.form.get('new_chanel')


    if request.method== "POST":

        new_chanel = request.form.get('new_chanel')


        if not new_chanel:
            return jsonify({"success": False})

        session["chanel"]=new_chanel

        print (f"chanel is {new_chanel}")

        #add chanel to chanel list
        chanels_list.append(new_chanel)

        chanels = chanels_list

        """ add chanel to messages dict"""
        messages_dict[new_chanel]=[]
        print(f"this is messages_dict {messages_dict}: ")

        return jsonify({"success": True, "new_chanel": new_chanel, "chanles": chanels})


@socketio.on("submit message")
def message(data):

    message = data["message"]

    print(f"this is the  message: {message}")

    timestamp = datetime.datetime.now().strftime("Date: %Y-%m-%d Time: %H:%M:%S")


    messagelist = []

    messagesdict = {}

    chanel= session["chanel"]

    print(f"this is the chanel in submit message: {chanel}")



    full_message = timestamp + ": " + session["username"] + ": " +  message

    """
    messagelist.append(full_message)

    messagedict["messages"]=messagelist

    messages_dict["chanel"]=messagedict["messages"].append()

    """


    messages_dict[chanel].append(timestamp + ": " + session["username"] + ": " +  message)

    messages_list.append("chanel: " +  chanel  + ":" +  str(messages_dict))

    print(f"this is messages_dict {messages_dict}: ")



    #messagedict = {"message": message, "username": session["username"]}
    #messagedict["message"] = message
    #messagedict["user_name"]= session["username"]

    #messages["message"].append(messagedict["message"])
    emit("send message",  { 'timestamp': timestamp, 'username': session["username"], 'message': message },  broadcast=True)


""" route for sending the stored messages """
@app.route("/messages", methods = ["POST"])
def messages():
    if len(chanels_list) > 0:
        chanel = request.form.get("chanel_select")
        #chanel = chanels_list[len(chanels_list) - 1]

        for key in messages_dict:
            if key == session["chanel"]:
                old_chats = messages_dict[key]

        print(f"here is the old chats: {old_chats}")

        print(messages_dict)

        print(f"this is messages list: {messages_list}")



        return str(old_chats)





    return redirect("/chanels/" + new_chanel)


@app.route("/chanels/<chanel>", methods=["GET", "POST"])
def enter_chanel(chanel):

    if request.method=="GET":
        chanel=request.form.get("select_chanel")
        #chanel = session["chanel"]
        chanel_message_list = messages_dict["4"]
        return render_template("chanels.html", users=users, chanels_list=chanels_list, chanel_message_list=chanel_message_list,
                            messages_dict=messages_dict, messages_list=messages_list, chanel=session['chanel'])

    else:
        return redirect("/")





@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    socketio.run(app)
