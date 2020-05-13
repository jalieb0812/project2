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
users_list=[]

""" channels list """
channels_list=[]

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
        session.get('channel')
        print(f"this is the channels {channels_list}")
        print(f"this is session channels {channels_list}")




        return render_template("index.html", username=session["username"],  users_list=users_list, channel=session['channel'],
                                channels_list=channels_list, messages_dict=messages_dict, messages_list=messages_list)


    if request.method == "POST":
        if request.form.get("add_channel"):

            channel = request.form.get("add_channel")
            for channels in channels_list:
                if channels == channel:
                    flash("channel name already taken. chose another channel name")
                    return redirect('/channels')


            channels_list.append(channel)

            session["channel"] = channel

            """ add channel to messages dict """

            #messages_dict[new_channel]= []

            print(f"this is messages_dict {messages_dict}: ")

        if request.form.get("current_channels"):

            channel = request.form.get("current_channels")

            session["channel"] = channel

            print(f"this is messages_dict {messages_dict}: ")



        return  redirect (url_for('channel', username=session["username"], channel=session["channel"]))


            #print(f"these are the messages: {messages_dict}")





    #new_channel = request.form.get("newchannel")

    #session["channel"]=new_channel
    #print (f" channel in index is {new_channel}")

    #channels.append(new_channel)



    #return render_template("index.html", username=session["username"],users=users,
                            #messages_dict=messages_dict, channels_list_=channels_list)

@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():

    session.clear()





    if request.method=="POST":

        print(f"these are the users {users_list}")

        username = str(request.form.get("username"))

        print(f"username is {username}")


        for name in users_list:
            if name == username:
                return redirect('/sign_in')


        session['username']= username
        users_list.append(username)

        try:
            session.get(session["channel"])

            return redirect('/', username=session["username"], channel=session["channel"])

        except:

            return redirect("/channels")


    if request.method=="GET":

        return render_template("sign_in.html")






@app.route("/channels", methods = ["GET", "POST"])
def channels():

    if request.method == "GET":

        return render_template ("channels.html", channels_list = channels_list)


    if request.method == "POST":


        if not request.form.get("add_channel") and not request.form.get("current_channels"):
            flash("Error: you must create a channel or choose a current one")
            return redirect('/channels')

        if request.form.get("add_channel"):

            channel = request.form.get("add_channel")





            for channels in channels_list:
                if channels == channel:
                    flash("Error: Channel name already taken. Please choose another channel name")
                    return redirect('/channels')

            channels_list.append(channel)

            session["channel"] = channel

            """ add channel to messages dict """

            #messages_dict[new_channel]= []

            print(f"this is messages_dict {messages_dict}: ")

            return redirect(url_for('index', username=session["username"], channel=channel))

        if request.form.get("current_channels"):

            channel = request.form.get("current_channels")

            session["channel"] = channel

            print(f"this is messages_dict {messages_dict}: ")


        #session["messagesdict"]=messages_dict

            return redirect(url_for('index', username=session["username"], channel=channel))

    #return redirect(url_for('index', messages_dict=messages_dict, *request.args))




@app.route("/channel/<channel>", methods=["GET", "POST"])
def channel(channel):

    if request.method=="GET":

        session['channel']=channel

        return render_template("channel.html", users_list=users_list, channels_list=channels_list,
                            messages_dict=messages_dict, messages_list=messages_list, channel=session['channel'])

    else:
        return redirect("/")




""" route/code chcking usernames"""
@app.route("/user_verify", methods=["POST"])
def user_verify():

    username = request.form.get("username")



    print(f"this is username in user verify: {username}")

    for name in users_list:
        if username == name:
            return jsonify({"validate": False})

        #users.append(username)
        return jsonify({'validate': True})

    else:
        #users.append(username)
        return jsonify({'validate': True})



@socketio.on("submit channel")
def add_channel(data):
    #data is  { 'channel': channel} from socket.emit (submit channel  { 'channel': channel})
    channel = data["channel"]


    channels_list.append(channel)

    print(f"this is the  channel in submit channel: {channel}")

    emit("create channel",  {'channel': channel},   broadcast=True)


""" route/code for ensuring no two channels have the same name"""
@app.route("/channel_verify", methods=["POST"])
def channel_verify():

    channel = request.form.get("new_channel")

    if len(channels_list) > 0:

        print(f"this is channel in channel verify: {channel}")

        for channels in channels_list:

            if channel == channels:


                return jsonify({"validate": False})

        channels_list.append(channel)
        return jsonify({'validate': True})

    else:
        channels_list.append(channel)
        return jsonify({'validate': True})


""" route for deleting channels"""
@socketio.on("delete_channel")
def delete_channel(data):
    channel = data["channel"]

    print(f"this is the  channel to delete: {channel}")

    print(f"this is session channel in delete: {session['channel']}")

    if channel == session["channel"]:
        emit("channel_deleted", {'channel': channel}, broadcast=True)

    else:


        for item in channels_list:

            if item == channel:
                channels_list.remove(item)

        emit("channel_deleted", {'channel': channel}, broadcast=True)

    #return jsonify({'success': True})




@socketio.on("submit message")
def message(data):

    message = data["message"]

    print(f"this is the  message: {message}")

    timestamp = datetime.datetime.now().strftime("Date: %Y-%m-%d Time: %H:%M:%S")

    username = session.get("username")


    #messagelist = []


    channel= session["channel"]

    #messages_dict[channel] = []

    print(f"this is the channel in submit message: {channel}")


    full_message = timestamp + ": " + session["username"] + ": " +  message +'\n'

    messages_list.append(full_message)


    #if messages list has over 100 messages remove message index 0; Note: just to keep this smaller for debuging

    if len(messages_list) > 100:
        messages_list.pop([0])

    print(f"this is messages_list in submit message after append:  {messages_list}:")


    print(f"this is messages_dict in submit message before addition:  {messages_dict}:")

    if channel in messages_dict:

        print(f"this is last element in messages_list: {messages_list[:-1]}")
        messages_dict[channel].append(messages_list[-1])

        """remove first message from list if channel has over 100 messages"""
        if len(messages_dict[channel]) > 100:
            messages_dict[channel].pop(0)
    else:
        print("this else is happening")
        messages_dict[channel] = [full_message]

    print(f"this is messages_dict in submit message after addition:  {messages_dict}: ")

    emit("send message",  { 'timestamp': timestamp, 'username': session["username"], 'message': message, 'channel': channel },  broadcast=True)


@app.route("/createchannel", methods=["GET", "POST"])
def createchannel():


    new_channel = request.form.get('new_channel')


    if request.method== "POST":

        new_channel = request.form.get('new_channel')


        if not new_channel:
            return jsonify({"success": False})

        session["channel"]=new_channel

        print (f"channel is {new_channel}")

        #add channel to channel list
        channels_list.append(new_channel)

        channels = channels_list

        """ add channel to messages dict"""
        messages_dict[new_channel]=[]
        print(f"this is messages_dict in createchannel {messages_dict}: ")

        return jsonify({"success": True, "new_channel": new_channel, "chanles": channels})

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
