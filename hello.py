from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from wtforms.widgets import TextArea

#Create a Flask Instance
app = Flask(__name__)

#Add Database
#Old database sqlite
# app.config['SQALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#new database sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Test1234@localhost/our_users'
#Secret Key
app.config['SECRET_KEY'] = "This is my secret key"
#Initialize the DB
db = SQLAlchemy(app)
#Migration of Database
migrate = Migrate(app,db)

#Create a Blog Post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    
#Create a Posts Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slugfield", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Add Post Page
@app.route('/add_post', methods=['GET','POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data, 
                     content=form.content.data,
                     author=form.author.data,
                     slug=form.slug.data,
                     )
        #Clear the form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data =''

        #Add post data to database
        db.session.add(post)
        db.session.commit()

        #return a message
        flash("Blog POst submitted successfully")

    #Redirect to the webpage
    return render_template('add_post.html',form=form)


#Jason
@app.route('/date')
def get_current_date():
    favorite_pizza = {
        "John": "Hawaiaan",
        "Renan": "Pepperoni",
        "Analyn": "Cheeze"
    }
    return favorite_pizza
    #return {"Date": date.today()}

#Update Database Record
@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            flash("Error, Try again")
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)

#on terminal type the following: incase of Application Context error
# >>>from app import db, app
# >>>from hello import db
# >>> with app.app_context():
# ... db.create_all() (this first press space button, next db.create_all())
# ... (this just press enter button)

#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Do some password stuff!
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    with app.app_context():
        db.create_all()

    #Create A String
    def __repr__(self):
        return '<Name %r>' % self.name
    
#Delete Data    
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted Successfully')

        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)
    except:
        flash("There was a problem deleting this record. Try again")

        return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)
 
#Create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Pasword Class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email", validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")




@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            #Hash the password!
            hashed_pw = generate_password_hash(form.password_hash.data,"sha256")
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data =''
        form.password_hash =''

        flash("user added successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)

#Create a route decorator
@app.route('/')
def index():
    #return "<h1> Hello Renan </h1>"
    first_name = "Renan"
    stuff = "<strong> Hello Guyss!!! </strong>"
    flash("Welcome to the jungle")

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

#Create Password test page
@app.route('/test_pw',methods=['GET','POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None 
    form = PasswordForm()

    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data   
        #Clear the form
        form.email.data = ''
        form.password_hash.data = ''  
        pw_to_check = Users.query.filter_by(email=email).first()  

        #Check hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)
        
    return render_template("test_pw.html",
                           email = email,
                           password = password,
                           pw_to_check = pw_to_check,
                           passed = passed,
                           form = form)

#Create Name Page
@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
        
    return render_template("name.html",
                           name = name,
                           form = form)