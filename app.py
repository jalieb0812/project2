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



@app.route("/" , methods=["GET", "POST"])
@login_required
def index():

    if request.method == "GET":

        session.get('username')
        print(f"this is the chanels {chanels_list}")



        return render_template("index.html", username=session["username"],  users=users, chanels_list=chanels_list, messages_dict=messages_dict, messages_list=messages_list)


    if request.method == "POST":
        if request.form.get("add_chanel"):

            chanel = request.form.get("add_chanel")

            chanels_list.append(chanel)

            session["chanel"] = chanel

            """ add chanel to messages dict """

            #messages_dict[new_chanel]= []

            print(f"this is messages_dict {messages_dict}: ")

        if request.form.get("current_chanels"):

            chanel = request.form.get("current_chanels")

            session["chanel"] = chanel

            print(f"this is messages_dict {messages_dict}: ")

        return  render_template('chanel.html', username=session["username"], chanel=chanel)


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
        users.append(username)

        try:
            session.get(session["chanel"])

            return redirect('/', username=session["username"], chanel=session["chanel"])

        except:

            return redirect("/chanels")



    if request.method=="GET":

        return render_template("sign_in.html")


@app.route("/chanels", methods = ["GET", "POST"])
def chanels():

    if request.method == "GET":

        return render_template ("chanels.html", chanels_list = chanels_list)



    if request.form.get("new_chanel"):

        chanel = request.form.get("new_chanel")

        chanels_list.append(chanel)

        session["chanel"] = chanel

        """ add chanel to messages dict """

        #messages_dict[new_chanel]= []

        print(f"this is messages_dict {messages_dict}: ")

    if request.form.get("current_chanels"):

        chanel = request.form.get("current_chanels")

        session["chanel"] = chanel

        print(f"this is messages_dict {messages_dict}: ")


    #session["messagesdict"]=messages_dict

    return redirect(url_for('index', username=session["username"], chanel=chanel))

    #return redirect(url_for('index', messages_dict=messages_dict, *request.args))


@app.route("/chanel/<chanel>", methods=["GET", "POST"])
def chanel(chanel):

    if request.method=="GET":

        session['chanel']=chanel

        return render_template("chanel.html", users=users, chanels_list=chanels_list,
                            messages_dict=messages_dict, messages_list=messages_list, chanel=session['chanel'])

    else:
        return redirect("/")


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



@socketio.on("submit message")
def message(data):

    message = data["message"]

    print(f"this is the  message: {message}")

    timestamp = datetime.datetime.now().strftime("Date: %Y-%m-%d Time: %H:%M:%S")

    username = session.get("username")


    #messagelist = []


    chanel= session["chanel"]

    #messages_dict[chanel] = []

    print(f"this is the chanel in submit message: {chanel}")


    full_message = timestamp + ": " + session["username"] + ": " +  message

    messages_list.append(full_message)

    print(f"this is messages_list in submit message after append:  {messages_list}: \n")



    """
    messagelist.append(full_message)

    messagedict["messages"]=messagelist

    messages_dict["chanel"]=messagedict["messages"].append()

    """

    print(f"this is messages_dict in submit message before addition:  {messages_dict}: \n")

    if chanel in messages_dict:

        print(f"this is last element in messages_list: {messages_list[:-1]}")
        messages_dict[chanel].append(messages_list[-1])
    else:
        print("this else is happening")
        messages_dict[chanel] = [full_message]

    #messages_dict[chanel] = timestamp + ": " + session["username"] + ": " +  message

    print(f"this is messages_dict in submit message after addition:  {messages_dict}: \n")

    #messages_list.append("chanel: " +  chanel  + ":" +  str(messages_dict))

    #messagedict = {"message": message, "username": session["username"]}
    #messagedict["message"] = message
    #messagedict["user_name"]= session["username"]

    #messages["message"].append(messagedict["message"])
    emit("send message",  { 'timestamp': timestamp, 'username': session["username"], 'message': message },  broadcast=True)


""" route for sending the stored messages """
@app.route("/messages", methods = ["GET"])
def messages():

    if len(chanels_list) > 0:
        chanel = request.form.get("chanel_select")
        #chanel = chanels_list[len(chanels_list) - 1]

        for key in messages_dict:
            if key == session["chanel"]:
                old_chats = messages_dict[key]

        print(f"here is the old chats: {old_chats}")

        print(messages_dict)

    #    print(f"this is messages list: {messages_list}")



        return str(old_chats)


    else:

        return redirect('/')








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

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == "__main__":
 port = int(os.environ.get("PORT", 8080))
 socketio.run(app, host="0.0.0.0", port=port)

"""
if __name__ == '__main__':


    socketio.run(app)
"""
