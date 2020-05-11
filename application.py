import os
import requests
import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit
from loginrequired import login_required
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

""" function to secure a filename before storing it directly on the filesystem."""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/" , methods=["GET", "POST"])
@login_required
def index():

    if request.method == "GET":


        session.get('username')
        session.get('chanel')
        print(f"this is the chanels {chanels_list}")
        print(f"this is session chanels {chanels_list}")




        return render_template("index.html", username=session["username"],  users=users, chanel=session['chanel'], chanels_list=chanels_list, messages_dict=messages_dict, messages_list=messages_list)


    if request.method == "POST":
        if request.form.get("add_chanel"):

            chanel = request.form.get("new_chanel")
            for chanels in chanels_list:
                if chanels == chanel:
                    flash("chanel name already taken. chose another chanel name")
                    return redirect('/chanels')


            chanels_list.append(chanel)

            session["chanel"] = chanel

            """ add chanel to messages dict """

            #messages_dict[new_chanel]= []

            print(f"this is messages_dict {messages_dict}: ")

        if request.form.get("current_chanels"):

            chanel = request.form.get("current_chanels")

            session["chanel"] = chanel

            print(f"this is messages_dict {messages_dict}: ")



        return  redirect (url_for('chanel', username=session["username"], chanel=session["chanel"]))


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


    if request.method == "POST":



        if request.form.get("new_chanel"):

            chanel = request.form.get("new_chanel")


            for chanels in chanels_list:
                if chanels == chanel:
                    flash("chanel name already taken. chose another chanel name")
                    return redirect('/chanels')

            chanels_list.append(chanel)

            session["chanel"] = chanel

            """ add chanel to messages dict """

            #messages_dict[new_chanel]= []

            print(f"this is messages_dict {messages_dict}: ")

            return redirect(url_for('index', username=session["username"], chanel=chanel))

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



@socketio.on("submit chanel")
def add_chanel(data):
    #data is  { 'chanel': chanel} from socket.emit (submit chanel  { 'chanel': chanel})
    chanel = data["chanel"]


    chanels_list.append(chanel)

    print(f"this is the  chanel in submit chanel: {chanel}")

    emit("create chanel",  {'chanel': chanel},  broadcast=True)


""" route/code for ensuring no two channels have the same name"""
@app.route("/chanel_verify", methods=["POST"])
def chanel_verify():

    chanel = request.form.get("new_chanel")

    if len(chanels_list) > 0:

        print(f"this is chanel in chanel verify: {chanel}")

        for chanels in chanels_list:

            if chanel == chanels:


                return jsonify({"validate": False})

        chanels_list.append(chanel)
        return jsonify({'validate': True})

    else:
        chanels_list.append(chanel)
        return jsonify({'validate': True})


""" route for deleting chanels"""
@socketio.on("delete_channel")
def delete_channel(data):
    channel = data["channel"]

    print(f"this is the  channel to delete: {channel}")

    for item in chanels_list:

        if item == channel:
            chanels_list.remove(item)

    emit("channel_deleted", {'channel': channel}, broadcast=True)

    #return jsonify({'success': True})




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


    full_message = timestamp + ": " + session["username"] + ": " +  message +'\n'

    messages_list.append(full_message)


    #if messages list has over 100 messages remove message index 0; Note: just to keep this smaller for debuging

    if len(messages_list) > 100:
        messages_list.pop([0])

    print(f"this is messages_list in submit message after append:  {messages_list}:")


    print(f"this is messages_dict in submit message before addition:  {messages_dict}:")

    if chanel in messages_dict:

        print(f"this is last element in messages_list: {messages_list[:-1]}")
        messages_dict[chanel].append(messages_list[-1])

        """remove first message from list if chanel has over 100 messages"""
        if len(messages_dict[chanel]) > 100:
            messages_dict[chanel].pop(0)
    else:
        print("this else is happening")
        messages_dict[chanel] = [full_message]

    print(f"this is messages_dict in submit message after addition:  {messages_dict}: ")

    emit("send message",  { 'timestamp': timestamp, 'username': session["username"], 'message': message },  broadcast=True)


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
        print(f"this is messages_dict in createchanel {messages_dict}: ")

        return jsonify({"success": True, "new_chanel": new_chanel, "chanles": chanels})

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


"""
if __name__ == "__main__":
 port = int(os.environ.get("PORT", 8080))
 socketio.run(app, host="0.0.0.0", port=port)

"""
if __name__ == '__main__':


    socketio.run(app)
