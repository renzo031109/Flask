from flask import Flask, render_template

#Create a Flask Instance
app = Flask(__name__)

#Create a route decorator
@app.route('/')
def index():
    #return "<h1> Hello Renan </h1>"
    first_name = "Renan"
    stuff = "<strong> Hello Guyss!!! </strong>"

    family = ["Renan", "Uriel", "Renan", "Rain",50]

    return render_template("index.html",
                           first_name=first_name,
                           stuff=stuff,
                           family=family)

@app.route('/user/<name>')
def user(name):
    return render_template("user.html",user_name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500 
