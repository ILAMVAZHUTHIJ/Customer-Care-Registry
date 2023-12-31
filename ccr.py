from flask import Flask, flash, redirect
from flask import url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '587480e285a7584cd755f6d6247ceb77'
app.config['SQLALCHEMY_'] = 'sqlite:////venv/site.db'

db = SQLAlchemy(app)

def test_connection(self):
    with app.app_context:
        from crr import db
        db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(120), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    ticket = db.relationship('Ticket', backref='author', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Ticket('{self.title}', '{self.date_posted}')"

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','Success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'Succcess')
            return redirect(url_for('index'))
        else:
            flash('Login was Unseccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login' , form=form)


if __name__ == "__main__":
    app.run(debug=True)