import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = "randomstring123"
messages = []

def add_messages(username, message):
    """ add messages to messages list"""
    now = datetime.now().strftime("%H:%M:%S")
    messages.append("({}) {}: {}".format(now, username, message))
    messages_dict = {"timestamp": now, "from": username,"message":message}
    messages.append(messages_dict)

def get_all_messages():
    """Get all the messages and separete the with </br> tag"""
    return "<br>".join(messages)

@app.route("/", methods = ["GET","POST"])
def index():
    """Main page with instructions"""

    if request.method == "POST":
        session["username"] = request.form["username"]

    if "username" in session:
        return redirect(session["username"])

    return render_template("index.html")

@app.route('/<username>', methods = ["GET","POST"])
def user(username):
    """Display chat messages"""
    """return "<h1>Welcome, {0}</h1>{1}".format(username, messages)"""
    if request.method == "POST":
        username=session["username"]
        message = request.form["message"]
        add_messages(username, message)
    """ if comment out line 41 the message typed will come again and repeart forever"""
    return redirect(session["username"])
    
    return render_template("chat.html", username = username, chat_messages = messages)

@app.route('/<username>/<message>')
def send_message(username, message):
    """Create a new message and redirect back to the chat page"""
    add_messages(username,message)
    return redirect("/" + username)

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')),debug=True)