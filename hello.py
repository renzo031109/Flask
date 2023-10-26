from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from webforms import LoginForm, UserForm, PasswordForm, NamerForm, PostForm, SearchForm
from flask_ckeditor import CKEditor

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#Create a Flask Instance
app = Flask(__name__)
#add CKEditor
ckeditor = CKEditor(app)
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

#Flask Migrate Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#Create Admin Page
@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 3:
        return render_template("admin.html")
    else:
        flash("Sorry this page is for admin only!")
        return redirect(url_for('dashboard'))

#Add Post Page
@app.route('/add_post', methods=['GET','POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, 
                     content=form.content.data,
                     poster_id=poster,
                     slug=form.slug.data,
                     )
        #Clear the form
        form.title.data = ''
        form.content.data = ''
       # form.author.data = ''
        form.slug.data =''

        #Add post data to database
        db.session.add(post)
        db.session.commit()

        #return a message
        flash("Blog POst submitted successfully")

    #Redirect to the webpage
    return render_template('add_post.html',form=form)



@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            #Hash the password!
            hashed_pw = generate_password_hash(form.password_hash.data,"sha256")
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.username.data = ''
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


#Create Dashboard Page
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.about_author = request.form['about_author']
        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template('dashboard.html',
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            flash("Error, Try again")
            return render_template('dashboard.html',
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template('dashboard.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
  #  return render_template('dashboard.html')

#Create Delete route
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id    
    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            #return a message
            flash("Blog post was deleted")

            #Grab all the post from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html",posts=posts)
        except:
            flash("There was a problem deleting post")
            #Grab all the post from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html",posts=posts)

    else:
        flash("You are not authorized to delete this post")
        #Grab all the post from the database
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html",posts=posts)



    
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
 

#Edit Post    
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
       # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update Database
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated")
        return redirect(url_for('post',id=post.id))
    
    if current_user.id == post.poster_id:
        #filled with existing data
        form.title.data = post.title
        # form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html',form=form)
    else:
        flash("You are not authorized to edit post") 
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html",posts=posts)

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


#Create Login Page
@app.route('/login', methods=['GET','POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            #Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfull!")
                return redirect(url_for('dashboard'))     
            else:
                flash("Wrong Password!")
        else:
            flash("That user doesnt exist")
    return render_template('login.html', form=form)

#Create Logout Page
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out" )
    return redirect(url_for('login'))


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


@app.route('/posts')
def posts():
    #Grab all the post from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html",posts=posts)
    

#View post individually
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html',post=post)
    

#Pass stuff to NavBar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

#Create Search Function 
@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        #Get data from submitted form
        post.searched = form.searched.data
        #query the database
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template("search.html", 
                               form=form,
                               searched=post.searched,
                               posts=posts)


#Update Database User Record
@app.route('/update/<int:id>', methods=['POST','GET'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
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
    

#Create a Blog Post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    #Foreign Key
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create User Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    about_author = db.Column(db.Text(500), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #Do some password stuff!
    password_hash = db.Column(db.String(128))
    #Users can have many posts
    posts = db.relationship('Posts', backref='poster')