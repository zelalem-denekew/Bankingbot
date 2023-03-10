import re
from datetime import datetime
from flask import render_template, request, jsonify, session
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name):
    return render_template(
        "hello_there.html", 
        name = name, 
        date = datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

#chats = [] # initialize list of chats
@app.route("/chat", methods=['GET', 'POST'])
def chatbot():
    
    if 'chats' not in session:
        session['chats'] = []  # initialize list of chats in session

    if request.method == 'POST':
        question = request.form['question']
        response = get_response(question)
        session['chats'].append(Chat(question, 'question'))
        session['chats'].append(Chat(response, 'response'))
    return render_template('chatbot.html', chats=session['chats']) # pass chats list to template


def get_response(question):
    responses = {
        'What is your name?': 'My name is Chatbot',
        'What is the weather like today?': 'I am sorry, I am not programmed to provide weather forecasts',
        'What time is it?': 'I am sorry, I am not programmed to provide time information',
        'How are you?': 'I am doing well, thank you for asking!'
    }
    # Retrieve the response from the dictionary
    if question in responses:
        return responses[question]
    else:
        return 'I am sorry, I do not understand your question'

class Chat:
    def __init__(self, text, type):
        self.text = text
        self.type = type