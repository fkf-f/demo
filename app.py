from flask import Flask
app = Flask(__name__)
# @app.route('/')
# def hello():
#   return 'Hello World!'
from markupsafe import escape

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'
