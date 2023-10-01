from flask import Flask, render_template

#Create a Flask Instance
app = Flask(__name__)

#Create a route decorator
@app.route('/')
def index():
    #return "<h1> Hello Renan </h1>"
    first_name = "Renan"
    return render_template("index.html",first_name=first_name)

@app.route('/user/<name>')
def user(name):
    return render_template("user.html",user_name=name)