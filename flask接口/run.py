from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Home</h1>'
if __name__ == 'main':
    app.run()