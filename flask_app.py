from flask import Flask, render_template, redirect, flash, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "P@55w0rd";

app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="McCourt1029",
    password="Topher1029",
    hostname="McCourt1029.mysql.pythonanywhere-services.com",
    databasename="McCourt1029$users",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PersonForm(FlaskForm):
    given_name = StringField('Given Name', validators=[DataRequired()])
    family_name = StringField('Family Name', validators=[DataRequired()])
    profile_image = StringField('Profile Image', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MessageForm(FlaskForm):
    content = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Post')

user = {'username': 'McCourt'}

@app.route('/', methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def hello_world():
    title = None
    form = MessageForm()
    if form.validate_on_submit():
        flash.validate_on_submit(f'message {form.content}')
        #comment = Comment(content=request.form["comment"])
        #db.session.add(comment)
        #db.session.commit()
        return redirect('/')
    return render_template('index.html', user=user, title=title, form=form, comments=Comment.query.all())

@app.route('/mccourt')
def micro_blog():
    user = {'username': 'McCourt'}
    title = None
    posts_me = [
        {
            'author': user,
            'body': "I like pizza!"
        },
        {
            'author': user,
            'body': "What up my ni-"
        },
        {
            'author': user,
            'body': "What are you wearing?"
        },
    ]
    posts_other = [
        {
            'author': {'username': 'Kizito'},
            'body': "In chains?"
        },
        {
            'author': {'username': 'Bob'},
            'body': "Eat the pizza thot!"
        },
        {
            'author': {'username': 'Ryan'},
            'body': "Who is Ryan?"
        },
    ]
    return render_template('microblog.html', user=user, title=title, posts=posts_me, posts2=posts_other)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash(f"login requested for user {form.username.data}".format(form.username.data))
        flash(f"Remember me = {form.remember_me.data}".format(form.remember_me.data))
        return redirect("/index")
    return render_template("login.html", title="sign in", form=form)

@app.route('/person', methods=['GET', 'POST'])
def person():
    form=PersonForm()
    if form.validate_on_submit():
        flash(f"Name: {form.given_name.data} {form.family_name.data}".format(form.given_name.data, form.family_name.data))
        flash(f"Your profile image was linked at {form.profile_image.data}".format(form.profile_image.data))
        # No matter what I try it WILL NOT let me pass "form.profile_image.data" to the html template "profile_image.html", and use the same as I would in the flashed messages.
        return redirect("/profile_image")
    return render_template("person.html", title="person details", form=form)

@app.route('/profile_image', methods=['GET', 'POST'])
def profile_image():
    form=PersonForm()
    title = None
    return render_template('profile_image.html', title=title, form=form)
