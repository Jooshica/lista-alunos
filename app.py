from flask import Flask

app = Flask(__name__)

def home():
    return 'Hello web!'

app.run()